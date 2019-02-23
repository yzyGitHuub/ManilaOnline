# -*- coding: utf-8 -*-
# (c) 2019 ManilaOnline 项目组.保留所有权利.
#
# 本文件用以实现 Manila 项目的客户端通信子模块
#
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
# 由 ManilaOnline 项目组创建于    2018/12/15
# 由项目组成员 YZY, DQ 最近一次更新于 2019/1/19

from ManilaClientMSG import ManilaMSG
import socket
import datetime
import time

HOST = '39.106.10.117'  # Manila服务器主机
PORT = 7110  # 服务器主机接受响应的端口
defaultID = 0  # 本地用户 ID, 0 用户为公共匿名账户
defaultNAME = 'Anonymous'  # 本地用户昵称, Anonymous 为公共匿名账户
defaultPWD = '000'  # 本地用户密码, 000 为公共匿名账户登录密码


def get_time():
    present_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    return present_time


# 客户端消息对象
class ClientMSG:
    def __init__(self):
        # 初始化一个客户端消息发送体
        # 初始状态的时候都是用群星账号登录
        self.usrNAME = defaultNAME
        self.usrPWD = defaultPWD
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(2)

    def connect(self, name, pwd):
        try:
            self.usrNAME = name
            self.usrPWD = pwd
            # 尝试连接远程服务器
            self.client_socket.connect((HOST, PORT))
            # 登录请求格式为
            # $REQUEST=LOAD&NAME=***&PWD=***$
            login_message = bytes(
                '$REQUEST=LOGIN&NAME=' + self.usrNAME + '&PWD=' + self.usrPWD + '&TIME=' + get_time() + ';',
                encoding='utf-8')
            self.client_socket.sendall(login_message)
            print('Connection Request has been sent.')
        except Exception:
            print('Unable to connect because of %s' % Exception)

    def send(self, msg):
        data = ('$' + msg + '&TIME=' + get_time()).encoding(encoding='utf-8')
        print(get_time() + ' send message:' + data)
        self.client_socket.sendall(bytes(data))

    def read(self):
        data = self.client_socket.recv(4096)
        if not data:
            print(get_time()+'No data has been received.')
            return '$'
        else:
            msg = data.decode()
            print(get_time() + ' get msg:' + msg)
            return msg

    def quit(self):
        self.send('REQUEST=LOGOFF')


if __name__ == '__main__':
    print("This is the module of client.")
    chat_client_obj = ClientMSG()
    chat_client_obj.connect('Anonymous', '000')
    while True:
        print(chat_client_obj.read())
        time.sleep(2)
