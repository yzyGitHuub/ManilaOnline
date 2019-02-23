# -*- coding: utf-8 -*-
# Created by: DQ
# 本文件用以实现 Manila 项目的客户端消息类
#
# 本游戏的消息仿照wms协议制定
# 请求包括 LOGIN, LOGOFF, TESTCONNECT
# 参数包括但不限于 ID, NAME, PWD
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
# 由项目组成员 JT 最近一次更新于 2019/1/20
import re


class ManilaMSG:
    def __init__(self, recv_msg_decode):
        self.body = {}
        temp = re.split('[&=]', recv_msg_decode[1:])
        for i in range(len(temp) // 2):
            temp[i * 2] = temp[i * 2 + 1]
