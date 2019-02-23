# -*- coding: utf-8 -*-
# Created by: YZY
# 本文件用以实现 Manila 项目的服务器端游戏对象类
#
# 每个游戏玩家包括
# Name, PWD, flag, socket, id, mail, honor
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
# 由项目组成员 YZY 最近一次更新于 2019/1/20

import pymysql

mysql_host = '39.106.10.117'
#mysql_usr = 'root'
#mysql_pwd = 'manilaPASSWORD'
mysql_usr = 'manilaRemote'
mysql_pwd = 'remotePASSWORD'
mysql_db = 'manila'


class ManilaPlayer:
    def __init__(self, Name, PWD, sock):
        self.Name = Name
        self.PWD = PWD
        self.flag = 'OFF'
        self.socket = None
        db = pymysql.connect(mysql_host, mysql_usr, mysql_pwd, mysql_db)  # 连接数据库
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        sql_command = r"SELECT * FROM manila.userinfo where user_name = '" + self.Name + r"' and user_pwd = '" + self.PWD + r"';"
        print(sql_command)
        cursor.execute(sql_command)  # 使用 execute()  方法执行 SQL 查询
        data = cursor.fetchone()  # 使用 fetchone() 方法获取单条数据.
        if len(data) != 0:
            self.flag = 'ON'
            self.socket = sock
            self.id = data[0]
            self.mail = data[2]
            self.honor = data[4]
            self.available = True
        else:
            self.flag = 'NONE'
        # 关闭数据库连接
        db.close()

