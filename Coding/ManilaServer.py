# -*- coding: utf-8 -*-
# Created by: YZY
#
# 本文件用以实现 Manila 项目的服务器端控制模块
#
# 对于一个控制模块，其占用一个唯一的端口 7000
# 用户的登录是通过此端口来进行交互，控制模块只负责分发端口
# 不同端口进行的对局使用多线程来实现
# 对局开始后主线程将用户的 socket 传给 Gaming 以后就删除此套接字
# 用户结束对局以后需要重新登录
# 更多信息见Manila详细设计2.0文档
#
#
#  * ━━━━━━神兽出没━━━━━━
#  *       ┏┓      ┏┓
#  *     ┏┛┻━━━┛┻┓
#  *     ┃              ┃
#  *     ┃      ━      ┃
#  *     ┃  ┳┛  ┗┳  ┃
#  *     ┃              ┃
#  *     ┃      ┻      ┃
#  *     ┃              ┃
#  *     ┗━┓      ┏━┛Code is far away from bug with the animal protecting
#  *         ┃      ┃    神兽保佑,代码无bug
#  *         ┃      ┃
#  *         ┃      ┗━━━┓
#  *         ┃               ┣┓
#  *         ┃               ┏┛
#  *         ┗┓┓┏━┳┓┏┛
#  *           ┃┫┫  ┃┫┫
#  *           ┗┻┛  ┗┻┛
# 由 ManilaOnline 项目组创建于    2019/1/15
# 由项目组成员 YZY, JT, DQ 最近一次更新于 2019/1/23

from ManilaServerGaming import ManilaGame
from ManilaServerMSG import ManilaMSG
from ManilaServerPlayer import ManilaPlayer
import socket
import select
import re
import threading
import gc
import time
import pymysql

mysql_host = '39.106.10.117'
# mysql_usr = 'root'
# mysql_pwd = 'manilaPASSWORD'
mysql_usr = 'manilaRemote'
mysql_pwd = 'remotePASSWORD'
mysql_db = 'manila'
available_port = list(range(100))

class ManilaServer:
    def __init__(self):
        self.PORT = '7000'  # 为Manila服务器控制进程分配端口用以监听用户登录消息
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立 TCP Socket套接字
        # 将套接字绑定到地址
        # 在AF_INET下,以元组（host,port）的形式表示地址 s.bind(adress)
        self.serverSocket.bind(('', self.PORT))
        # s.listen(backlog)
        # 开始监听TCP传入连接，backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量，该值至少为1，大部分应用程序设为5就可以了。
        self.serverSocket.listen(5)
        self.USER_MAP = {}  # 已登陆空闲用户 socket session 字典 id : player
        self.socketsMap = {}  # 已登陆空闲用户 socket session 字典 id : socket
        self.idMap = {}  # 已登陆空闲用户 socket session 字典 socket : id
        self.CONNECTION_LIST = []  # 当前已经登录进的空闲用户的套接字，主要用途是给 socket 监听
        self.CONNECTION_LIST.append(self.serverSocket)
        self.ONLINE_LIST = []  # 等待匹配的 ID 号码
        self.GAMING_MAP = {}  # 成员为正在进行的对局ID : 对局
        self.GameCount = 0
        print("ManilaServer started.")

    def broadcast(self, local_id, message):  # 广播来自 local_id 的消息
        message_send = '$SPEAKER=%s&MSG=%s' % (local_id, message)
        for sock in self.CONNECTION_LIST:
            if sock == self.serverSocket:
                continue
            else:
                try:
                    sock.send(message_send.encode(encoding='utf-8'))
                except Exception:
                    print(Exception)
                    sock.close()
                    offline_id = self.idMap[sock]
                    del self.idMap[sock]
                    del self.socketsMap[offline_id]
                    self.CONNECTION_LIST.remove(sock)
                    self.broadcast(offline_id, 'OFFLINE')
                    continue

    def p2psend(self, remote_id, message):
        remote_socket = self.socketsMap[remote_id]
        message_send = '$SPEAKER=HOST&MSG=' + message
        try:
            remote_socket.sendall(message_send)
        except Exception:
            print(Exception)
            remote_socket.close()
            del self.idMap[remote_socket]
            del self.socketsMap[remote_id]
            self.CONNECTION_LIST.remove(remote_socket)
            self.broadcast(remote_id, 'OFFLINE')
            del remote_socket

    def login(self, sock, recv_msg_decode):
        temp = re.split('[&=]', recv_msg_decode)
        for i in range(len(temp) // 2):
            if temp[i * 2] == 'NAME' and temp[i * 2 + 1] != '':
                NAME = temp[i * 2 + 1]
            elif temp[i * 2] == 'PWD' and temp[i * 2 + 1] != '':
                PWD = temp[i * 2 + 1]
            else:
                break
        try:
            new_log = ManilaPlayer(NAME, PWD, sock)
            if new_log.flag == 'Found':
                self.broadcast(new_log.Name, 'LOGIN')
                self.idMap[sock] = new_log.id
                self.socketsMap[new_log.id] = sock
                self.USER_MAP[new_log.id] = new_log
                self.p2psend(new_log.id, 'LOGINACCEPT&ID=' + new_log.id + '&HONOR=' + new_log.honor + '&MAIL=' + new_log.mail)
            else:
                sock.send('$SPEAKER=HOST&MSG=LOGINREJECTED')
        except:
            pass

    def logoff(self, sock, recv_msg_decode):
        temp = re.split('[&=]', recv_msg_decode)
        for i in range(len(temp) // 2):
            if temp[i * 2] == 'ID' and temp[i * 2 + 1] != '':
                self.broadcast(temp[i * 2 + 1], 'LOGOFF')
                del self.idMap[sock]
                del self.socketsMap[temp[i * 2 + 1]]
                del self.USER_MAP[temp[i * 2 + 1]]
                gc.collect()
                break
            else:
                continue

    def recv_msg(self, sock):
        recv_msg_decode = sock.recv(100).decode()
        recv_msg = ManilaMSG(recv_msg_decode)
        try:
            if recv_msg.body['REQUEST'] == 'ONLINE':
                self.ONLINE_LIST.append(recv_msg)
            elif recv_msg.body['REQUEST'] == 'LOGIN':
                if recv_msg.body['ID'] not in set(self.socketsMap):
                    self.login(sock, recv_msg_decode)
            elif recv_msg.body['REQUEST'] == 'LOGOFF':
                self.logoff(sock, recv_msg_decode)
            elif recv_msg.body['REQUEST'] == 'TESTCONNECT':
                pass
            else:
                print("Someone tried to connect without treaty")
                print(recv_msg_decode)
        except:
            pass

    def new_gaming(self):
        players = {}
        port = available_port.pop() + 7100
        for i in [3, 2, 1, 0]:
            players[self.ONLINE_LIST[i]] = self.socketsMap[self.ONLINE_LIST[i]]
            self.p2psend(self.idMap[self.socketsMap[self.ONLINE_LIST[i]]], 'ONLINEACCEPT&PORT=' + str(port))
            del self.socketsMap[self.ONLINE_LIST[i]]
            del self.idMap[self.socketsMap[self.ONLINE_LIST[i]]]
            del self.ONLINE_LIST[i]
        newGame = ManilaGame(self.GameCount, port, players)
        self.GAMING_MAP[newGame.ID] = newGame
        self.GameCount += 1
        return newGame.ID

    def socet_handle(self):
        while 1:
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])
            for sock in read_sockets:
                # New connection
                if sock == self.serverSocket:  # 用户通过主socket（即服务器开始创建的 socket，一直处于监听状态）来登录
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = self.serverSocket.accept()
                    recv_msg_decode = sockfd.recv(100).decode()
                    if recv_msg_decode.upper().find('REQUEST=LOGIN') != -1:
                        self.login(sockfd, recv_msg_decode)
                    else:
                        print("Someone tried to connect without treaty")
                        print(recv_msg_decode)
                else:
                    self.recv_msg(sock)
            for remote_id in set(self.socketsMap):
                self.p2psend(remote_id, 'TESTCONNECT')
            threads = []
            if len(self.ONLINE_LIST) >= 4:
                for i in range(len(self.ONLINE_LIST) // 4):
                    new_game_id = self.new_gaming()
                    t = threading.Thread(target=self.GAMING_MAP[new_game_id].Start)
                    threads.append(t)
            for t in threads:
                t.setDaemon(True)
                t.start()

