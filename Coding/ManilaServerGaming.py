# -*- coding: utf-8 -*-
# (c) 2019 ManilaOnline 项目组.保留所有权利.
#
# 本文件用以实现 Manila 项目的服务器端对局子模块
#
# 对于一个对局子模块，其占用一个唯一且独立的端口
# 每个子模块包括四个对局对象，如果玩家人数不足，则用机器玩家自动补足
# 初始化一场对局需要一个指定的端口号，对于马尼拉系统的服务器来说，这些可用的端口号是 7000 - 7999
# 初始化以后需要进行 fill() 操作使机器人来填充这个位置,暂时不支持
# 更多信息见Manila详细设计2.0文档
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
# 由项目组成员 YZY 最近一次更新于 2019/1/22

from ManilaServerMSG import ManilaMSG
from ManilaServerPlayer import ManilaPlayer
import select
import socket
import gc
import re
import pymysql
import datetime
import time

mysql_host = '39.106.10.117'
# mysql_usr = 'root'
# mysql_pwd = 'manilaPASSWORD'
mysql_usr = 'manilaRemote'
mysql_pwd = 'remotePASSWORD'
mysql_db = 'manila'


class ManilaGame:
    def __init__(self, game_id, port, players):  # players 是 socket session字典 id : socket
        self.ID = game_id
        self.PORT = port  # 为当前对局分配端口用以消息传输
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 建立 TCP Socket套接字
        # 将套接字绑定到地址
        # 在AF_INET下,以元组（host,port）的形式表示地址 s.bind(adress)
        self.serverSocket.bind(('', self.PORT))
        # s.listen(backlog)
        # 开始监听TCP传入连接，backlog 指定在拒绝连接之前，操作系统可以挂起的最大连接数量，该值至少为1，大部分应用程序设为5就可以了。
        self.serverSocket.listen(5)
        self.CONNECTION_LIST = []  # 消息链接池, 至少包括四个玩家(包括机器玩家)
        self.CONNECTION_LIST.append(self.serverSocket)
        self.user_count = 0
        self.user_in = players
        self.watch = {}
        print("Game ID: " + self.ID + " started.")
        print("server is ready.")
        file_path = 'manila_game' + self.ID + '.txt'
        f = open(file_path, "a")
        f.write('Game ID:' + self.ID + 'started.\n')
        f.close()
        for key, value in players.items():
            self.user_count += 1
            self.CONNECTION_LIST.append(value)
            self.p2psend(key, 'GAMESTART')

    def __del__(self):
        self.serverSocket.shutdown(2)  # 立即关闭此套接字的接收发送消息功能
        self.serverSocket.close()  # 关闭此套接字
        self.CONNECTION_LIST = []
        gc.collect()

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
                new_log.available = True
                if new_log.id in set(self.user_in):
                    self.user_in[new_log.id] = new_log
                    self.broadcast(new_log.id,
                                   'LOGIN&NAME=' + new_log.Name + '&ID=' + new_log.id + '&HONOR=' + new_log.honor + '&MAIL=' + new_log.mail)
                else:
                    self.watch[new_log.id] = new_log
                    self.broadcast(new_log.id,
                                   'WATCH&NAME=' + new_log.Name + '&ID=' + new_log.id + '&HONOR=' + new_log.honor + '&MAIL=' + new_log.mail)
                self.p2psend(new_log.id,
                             'LOGINACCEPT&ID=' + new_log.id + '&HONOR=' + new_log.honor + '&MAIL=' + new_log.mail)
            else:
                sock.send('$SPEAKER=HOST&MSG=LOGINREJECTED')
        except:
            pass

    def broadcast(self, local_id, message):  # 广播来自 local_id 的消息
        message_send = '$SPEAKER=%s&MSG=%s' % (local_id, message)
        file_path = 'manila_game' + self.ID + '.txt'
        f = open(file_path, "a")
        f.write(message_send + '\n')
        f.close()
        for play in self.user_in:
            if play.available is True:
                try:
                    play.socket.send(message_send.encode(encoding='utf-8'))
                except Exception:
                    print(Exception)
                    play.available = False
                    self.broadcast(play.id, 'ERROR')
                    continue

    def p2psend(self, remote_id, message):
        if self.user_in[remote_id].available is False:
            return
        remote_socket = self.user_in[remote_id].socket
        message_send = '$SPEAKER=HOST&MSG=' + message
        try:
            remote_socket.sendall(message_send)
        except Exception:
            print(Exception)
            remote_socket.close()
            self.user_in[remote_id].available = False
            self.broadcast(remote_id, 'ERROR')

    def recv_msg(self, player):
        sock = player.socket
        recv_msg_decode = sock.recv(100).decode()
        recv_msg = ManilaMSG(recv_msg_decode)
        try:
            if recv_msg.body['REQUEST'] == 'TESTCONNECT':
                pass
            else:
                self.broadcast(player.id, recv_msg_decode)
        except:
            pass

    def Start(self, args):
        while 1:
            # Get the list sockets which are ready to be read through select
            read_sockets, write_sockets, error_sockets = select.select(self.CONNECTION_LIST, [], [])
            for sock in read_sockets:
                # New connection
                if sock == self.serverSocket:  # 用户通过主socket（即服务器开始创建的 socket，一直处于监听状态）来登录
                    # Handle the case in which there is a new connection recieved through server_socket
                    sockfd, addr = self.serverSocket.accept()
                    recv_msg_decode = sockfd.recv(100).decode()
                    if recv_msg_decode.upper().find('REQUEST=TESTCONNECT') != -1:
                        self.p2psend(sockfd, 'RESPONSE=TESTCONNECT')
                    if recv_msg_decode.upper().find('REQUEST=ONLINE') != -1:
                        #  某人打算进入此对局
                        self.login(sockfd, recv_msg_decode)
                    else:
                        print("Someone tried to connect without treaty")
                        print(recv_msg_decode)
                else:
                    self.recv_msg(sock)
