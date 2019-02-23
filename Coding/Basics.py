# Basic.py
# Author: Nithouson
# Date: 2018/12/16
# Last Edit: 2018/12/21
# Class Player&Board ,Common const info

import random
from time import *

Stockprice=[0,5,10,20,30] # 股票价格
# 四种货物（1-4表示，下同。船只与所载货物编号相同，没有单独的编号）
GOOD_CIST=1 # 肉苁蓉
GOOD_SILK=2 # 丝绸
GOOD_GINS=3 # 人参
GOOD_JADE=4 # 玉石
GOOD_GAIN=[0,24,30,18,36]
# 位置表
POS_COST=[-1 for i in range(100)]
POS_GAIN=[-1 for j in range(100)]
# 11-44：船上位置(十位数代表货物，个位数从前往后)
POS_COST[11]=2
POS_COST[12]=3
POS_COST[13]=4
POS_COST[21]=3
POS_COST[22]=4
POS_COST[23]=5
POS_COST[31]=1
POS_COST[32]=2
POS_COST[33]=3
POS_COST[41]=3
POS_COST[42]=4
POS_COST[43]=5
POS_COST[44]=5
# 51-53 码头；61-63 修理厂
POS_COST[51]=POS_COST[61]=4
POS_GAIN[51]=POS_GAIN[61]=6
POS_COST[52]=POS_COST[62]=3
POS_GAIN[52]=POS_GAIN[62]=8
POS_COST[53]=POS_COST[63]=2
POS_GAIN[53]=POS_GAIN[63]=12
# 71-72 领航
POS_COST[71]=2 # 小领航
POS_COST[72]=5 # 大领航
# 81-82 海盗
POS_COST[81]=POS_COST[82]=5 # 81为海盗船长，82为海盗船员
# 91 保险公司
POS_COST[91]=0
POS_GAIN[91]=10

class Player:
    def __init__(self,name="default"):
        self.name=name
        self.turn=-1
        self.board=None
        # 玩家名，一个字符串
        return
    def bid(self,Curprice=0):
        # Curprice:当前报价
        return (-1,0) # -1代表退出竞拍，0代表不抵押股票
    def master(self):
        return random.choice([(3,3,3,-1,0,0),(3,3,-1,3,0,0),(3,-1,3,3,0,0),(-1,3,3,3,0,0)])
        # 前三种货物装船，起点为3;不购买股票，不抵押股票
    def place_retinue(self):
        return (0,0) # 0代表不放置随从（空位置，0代表不抵押股票
    def move_boat(self,type):
        # type为1：小领航，type为2：大领航
        return (0,0,0,0) # 所有船只不移动
    def pirateII(self,type,captain_pos=-1):
        # type为1：海盗船长，此时captain_pos为空
        # type为2：海盗船员，此时captain_pos为船长登船位置
        return 0 # 不登船
    def pirateIII(self,type,captain_boat=-1,captain_choice=5):
        # type为1：海盗船长，此时后两个参数无意义
        # type为2：海盗船员，此时captain_boat为船长所选船的货物类型（1-4）
        # captain_choice为该船的去向（5代表港口，6代表修理厂）
        return (0,5) # 第一个返回值为所选船的货物类型，第二个返回值为船的去向

class Board:
    def __init__(self,players):
        self.players= players
        for p in range(4):
            players[p].turn=p
            players[p].board=self
        # 棋盘状态
        # 与货物有关的列表为了可以1,2,3,4直接引用，长度为5，下同
        self.stockprice=[-1,0,0,0,0]
        self.stockremain=[-1,5,5,5,5]
        self.pos_state=[-1 for k in range(100)]
        # -1：空；0-3：被该玩家占据；6：当前不可用；9：永久不可用
        for pos in range(100):
            if POS_COST[pos]==-1:
                self.pos_state[pos]=9
        self.boat_pos=[-1,-1,-1,-1,-1]
        # 0-13 棋盘位置；51-53 港口；61-63 修理厂
        self.dice = [-1, -1, -1, -1, -1]
        # 玩家状态
        # 与玩家对应的列表长度为4，玩家用0-3标识，下同
        self.stocknum=[[-1,0,0,0,0] for i in range(4)]
        self.curmoney=[30,30,30,30]
        self.curtotal=[30,30,30,30]
        self.bidprice=[0,0,0,0] # 修订规则：总督起拍价格为0元
        # 根据西方经济学理论，取消价格控制可以带来更有效的市场结果:)
        self.stockpledge=[0,0,0,0]
        self.curmaster=-1
        self.curround=0
        self.curstage=0
        self.harbour_boats = 0
        self.repair_boats = 0
        return
    def game_process(self):
        # 建立log文件
        log=open(strftime("%Y%m%d_%H%M%S", localtime())+".log","w")
        log.write("Player1:"+self.players[0].name+"\n")
        log.write("Player2:" + self.players[1].name + "\n")
        log.write("Player3:" + self.players[2].name + "\n")
        log.write("Player4:" + self.players[3].name + "\n")
        log.write(strftime("%H:%M:%S", localtime())+" Manila begins\n")
        # 发放原始股票
        for p in range(4):
            for loop in range(2):
                s=0
                while self.stockremain[s]<=2:
                    s=random.randint(1,4)
                self.stocknum[p][s]+=1
                self.stockremain[s]-=1
                log.write(strftime("%H:%M:%S", localtime()) \
                    +" Assign stock "+str(s)+" to player"+str(p+1)+"\n")
        while(self.stockprice[1]<30 and self.stockprice[2]<30
            and self.stockprice[3]<30 and self.stockprice[4]<30):

            # 新一轮游戏，初始化
            for pos in range(100):
                if  not self.pos_state[pos]==9:
                    self.pos_state[pos]=-1
            self.pos_state[82]=6 # 无海盗船长时不能当海盗船员
            self.boat_pos=[-1,-1,-1,-1,-1]
            self.bidprice = [0,0,0,0]
            self.curround += 1
            log.write(strftime("%H:%M:%S", localtime()) + " Start of Round " + str(self.curround) + "\n")
            self.curstage = 0
            self.harbour_boats = 0
            self.repair_boats = 0
            # 竞选总督
            curprice=-1
            if self.curround>1:
                p=self.curmaster
            else:
                p=0
            self.curmaster = -1
            while self.bidprice.count(-1)<3:
                # 这一条件意味着如果前三个人不竞选，第四位玩家自动成为总督
                if not self.bidprice[p]==-1:
                    (self.bidprice[p],pledge)=self.players[p].bid(curprice)
                    # 处理股票抵押
                    # 要求竞选时报价不超过手中现金，如果钱不够，只有抵押了股票才有报价的权力
                    # 即使没有竞选成功，股票也已经抵押了。
                    if pledge>0:
                        if pledge>self.stocknum[p][1]+self.stocknum[p][2]+self.stocknum[p][3]+\
                                self.stocknum[p][4]-self.stockpledge[p]:
                            raise Exception("Invalid pledge")
                        else:
                            self.stockpledge[p]+=pledge
                            self.curmoney[p]+=10*pledge
                            log.write(strftime("%H:%M:%S", localtime())\
                                +" Player"+str(p+1)+" pledges "+str(pledge)+" stocks\n")
                    # 处理竞价
                    if self.bidprice[p]>self.curmoney[p]:
                        raise Exception("Invalid bid:Lack of money")
                    if self.bidprice[p]>curprice:
                        curprice=self.bidprice[p]
                    elif not self.bidprice[p]==-1:
                        raise Exception("Invalid bid")
                p=(p+1)%4
            # 总督行使职权
            for p in range(4):
                if self.bidprice[p]>=0:
                    self.curmaster=p
                    self.curmoney[p]-=max(curprice,0)
                    log.write(strftime("%H:%M:%S", localtime()) \
                        + " Player" + str(p + 1) + " becomes the master at a pr"\
                        +"ice of " + str(max(curprice,0))+"\n")
            (self.boat_pos[1],self.boat_pos[2],self.boat_pos[3],self.boat_pos[4],\
             stocktype,pledge)=self.players[self.curmaster].master()
            # 处理抵押股票
            if pledge > 0:
                if pledge > self.stocknum[self.curmaster][1] + self.stocknum[self.curmaster][2]+\
                        self.stocknum[self.curmaster][3] + self.stocknum[self.curmaster][4]-\
                        self.stockpledge[self.curmaster]:
                    raise Exception("Invalid pledge")
                else:
                    self.stockpledge[self.curmaster] += pledge
                    self.curmoney[self.curmaster] += 10 * pledge
                    log.write(strftime("%H:%M:%S", localtime()) \
                     + " Player" + str(self.curmaster+1) + " pledges " + str(pledge) + " stocks\n")
            # 处理船初始位置
            if not self.boat_pos.count(-1)==2:
                raise Exception("Invalid assignment")
            pos_sum=0
            for b in range(1,5):
                if self.boat_pos[b]>5:
                    raise Exception("Invalid assignment")
                if not self.boat_pos[b]==-1:
                    pos_sum+=self.boat_pos[b]
                else:
                    for pos in range(10*b+1,10*b+5):
                        if self.pos_state[pos]==-1:
                            self.pos_state[pos]=6
            if not pos_sum==9:
                raise Exception("Invalid assignment")
            log.write(strftime("%H:%M:%S", localtime()) + " Player" \
                + str(self.curmaster+1) + " assigns boats at " + str(self.boat_pos[1:])+"\n")
            # 处理购买股票
            if stocktype>0:
                curcost=min(10,self.stockprice[stocktype])
                if self.curmoney[self.curmaster]<curcost:
                    raise Exception("Invalid purchase of stock:lack of money")
                elif self.stockremain[stocktype]<=0:
                    raise Exception("Invalid purchase of stock:no available stock")
                else:
                    self.stockremain[stocktype]-=1
                    self.stocknum[self.curmaster][stocktype]+=1
                    self.curmoney[self.curmaster]-=curcost
                    log.write(strftime("%H:%M:%S", localtime()) + " Player" \
                              + str(self.curmaster + 1) + " buys stock of " + str(stocktype) + "\n")
            self.curstage=1
            # 第一轮放置随从
            p=self.curmaster
            for turn in range(4):
                (place,pledge)=self.players[p].place_retinue()
                # 处理抵押股票
                if pledge > 0:
                    if pledge > self.stocknum[p][1] + self.stocknum[p][2] + self.stocknum[p][3] + \
                            self.stocknum[p][4] - self.stockpledge[p]:
                        raise Exception("Invalid pledge")
                    else:
                        self.stockpledge[p] += pledge
                        self.curmoney[p] += 10 * pledge
                        log.write(strftime("%H:%M:%S", localtime()) \
                           + " Player" + str(p+1) + " pledges " + str(pledge) + " stocks\n")
                # 处理随从放置
                if place>0:
                    if not self.pos_state[place]==-1:
                        raise Exception("Invalid placement of retinue")
                    elif POS_COST[place]>self.curmoney[p]:
                        raise Exception("Invalid placement of retinue:lack of money")
                    else:
                        self.pos_state[place]=p
                        self.curmoney[p]-=POS_COST[place]
                        if place==91:
                            self.curmoney+=10
                        if place==81 and self.pos_state[82]==6:
                            self.pos_state[82] = -1
                        log.write(strftime("%H:%M:%S", localtime()) \
                           + " Player" + str(p + 1) + " places retinue at position " + str(place) + "\n")
                p=(p+1)%4
            # 第一轮投骰子
            for b in range(1,5):
                self.dice[b]=random.randint(1,6)
                if self.boat_pos[b]>=0:
                    self.boat_pos[b]+=self.dice[b]
                    log.write(strftime("%H:%M:%S", localtime()) \
                              + " Dice for Good " + str(b) + ": " + str(self.dice[b]) + "\n")
            self.curstage=2
            # 第二轮放置随从
            p = self.curmaster
            for turn in range(4):
                (place, pledge) = self.players[p].place_retinue()
                # 处理抵押股票
                if pledge > 0:
                    if pledge > self.stocknum[p][1] + self.stocknum[p][2] + self.stocknum[p][3] + \
                            self.stocknum[p][4] - self.stockpledge[p]:
                        raise Exception("Invalid pledge")
                    else:
                        self.stockpledge[p] += pledge
                        self.curmoney[p] += 10 * pledge
                        log.write(strftime("%H:%M:%S", localtime()) \
                           + " Player" + str(p+1) + " pledges " + str(pledge) + " stocks\n")
                # 处理随从放置
                if place > 0:
                    if not self.pos_state[place] == -1:
                        raise Exception("Invalid placement of retinue")
                    elif POS_COST[place] > self.curmoney[p]:
                        raise Exception("Invalid placement of retinue:lack of money")
                    else:
                        self.pos_state[place] = p
                        self.curmoney[p] -= POS_COST[place]
                        if place == 91:
                            self.curmoney[p] += 10
                        if place==81 and self.pos_state[82]==6:
                            self.pos_state[82] = -1
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Player" + str(p + 1) + " places retinue at position " + str(place) + "\n")
                p = (p + 1) % 4
            # 第二轮投骰子
            for b in range(1, 5):
                self.dice[b] = random.randint(1, 6)
                if self.boat_pos[b] >= 0:
                    self.boat_pos[b] += self.dice[b]
                    log.write(strftime("%H:%M:%S", localtime()) \
                              + " Dice for Good " + str(b) + ": " + str(self.dice[b]) + "\n")
                    if self.boat_pos[b]>13:
                        self.harbour_boats += 1
                        self.boat_pos[b]=50+self.harbour_boats
                        if self.pos_state[self.boat_pos[b]]==-1:
                            self.pos_state[self.boat_pos[b]]=6
                        for _pos in range(1,5):
                            if self.pos_state[b*10+_pos]==-1:
                                self.pos_state[b*10+_pos] = 6
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Good " + str(b) + " reaches the harbour\n")
            # 第二轮海盗登船
            if self.boat_pos.count(13)>=1 and not self.pos_state[81]==-1:
                replace1=self.players[self.pos_state[81]].pirateII(1)
                if not replace1 in [0,11,12,13,21,22,23,31,32,33,41,42,43,44]:
                    raise Exception("Invaid replace position")
                if replace1>0:
                    if self.boat_pos[replace1/10]!=13:
                        raise Exception("Invaid replace position:boat not available")
                    else:
                        self.pos_state[replace1]=self.pos_state[81]
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Pirate captain Player" + str(self.pos_state[81] + 1) + " launches position " + str(replace1) + "\n")
                        self.pos_state[81] = -1
                if not self.pos_state[82]==-1:
                    replace2 = self.players[self.pos_state[82]].pirateII(2,replace1)
                    if not replace2 in [0, 11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43, 44]:
                        raise Exception("Invaid replace position")
                    if replace2 > 0:
                        if self.boat_pos[replace2 / 10] != 13:
                            raise Exception("Invaid replace position:boat not available")
                        elif replace2==replace1:
                            raise Exception("Invaid replace position:cannot replace captain")
                        else:
                            self.pos_state[replace2] = self.pos_state[82]
                            log.write(strftime("%H:%M:%S", localtime()) \
                                      + " Pirate sailor Player" + str(
                                self.pos_state[82] + 1) + " launches position " + str(replace2) + "\n")
                            self.pos_state[82] = -1
                if self.pos_state[81]==-1 and not self.pos_state[82]==-1:
                    self.pos_state[81]=self.pos_state[82]
                    self.pos_state[82] = -1
            if self.harbour_boats<3:
                self.curstage = 3
                # 第三轮放置随从
                p = self.curmaster
                for turn in range(4):
                    (place, pledge) = self.players[p].place_retinue()
                    # 处理抵押股票
                    if pledge > 0:
                        if pledge > self.stocknum[p][1] + self.stocknum[p][2] + self.stocknum[p][3] + \
                                self.stocknum[p][4] - self.stockpledge[p]:
                            raise Exception("Invalid pledge")
                        else:
                            self.stockpledge[p] += pledge
                            self.curmoney[p] += 10 * pledge
                            log.write(strftime("%H:%M:%S", localtime()) \
                                      + " Player" + str(p + 1) + " pledges " + str(pledge) + " stocks\n")
                    # 处理随从放置
                    if place > 0:
                        if not self.pos_state[place] == -1:
                            raise Exception("Invalid placement of retinue")
                        elif POS_COST[place] > self.curmoney[p]:
                            raise Exception("Invalid placement of retinue:lack of money")
                        else:
                            self.pos_state[place] = p
                            self.curmoney[p] -= POS_COST[place]
                            if place == 91:
                                self.curmoney[p] += 10
                            if place == 81 and self.pos_state[82] == 6:
                                self.pos_state[82] = -1
                            log.write(strftime("%H:%M:%S", localtime()) \
                                + " Player" + str(p + 1) + " places retinue at position " + str(place) + "\n")
                    p = (p + 1) % 4
                # 领航员操纵船只
                if not self.pos_state[71]==-1:
                    move=self.players[self.pos_state[71]].move_boat(1)
                    if abs(move[0])+abs(move[1])+abs(move[2])+abs(move[3])>1:
                        raise Exception("Invalid move")
                    else:
                        for b in range(1,5):
                            if self.boat_pos[b]>0 and self.boat_pos[b]<=13:
                                self.boat_pos[b]=max(self.boat_pos[b]+move[b-1],0)
                                # 相当于直接排除了错误移动未启用和已进港船只的情况，视为没有移动
                                if self.boat_pos[b]>13:
                                    self.harbour_boats += 1
                                    self.boat_pos[b] = 50 + self.harbour_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(b) + " reaches the harbour\n")
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Player" + str(self.pos_state[71] + 1) + " moves boats： " + str(move) + "\n")
                if not self.pos_state[72]==-1:
                    move=self.players[self.pos_state[72]].move_boat(2)
                    if abs(move[0])+abs(move[1])+abs(move[2])+abs(move[3])>2:
                        raise Exception("Invalid move")
                    else:
                        for b in range(1,5):
                            if self.boat_pos[b]>0 and self.boat_pos[b]<=13:
                                self.boat_pos[b]=max(self.boat_pos[b]+move[b-1],0)
                                if self.boat_pos[b]>13:
                                    self.harbour_boats += 1
                                    self.boat_pos[b] = 50 + self.harbour_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(b) + " reaches the harbour\n")
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Player" + str(self.pos_state[72] + 1) + " moves boats： " + str(move) + "\n")
                # 掷第三轮骰子
                for b in range(1, 5):
                    self.dice[b] = random.randint(1, 6)
                    if self.boat_pos[b] >= 0 and self.boat_pos[b] <=13:
                        self.boat_pos[b] += self.dice[b]
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Dice for Good " + str(b) + ": " + str(self.dice[b]) + "\n")
                        if self.boat_pos[b] > 13:
                            self.harbour_boats += 1
                            self.boat_pos[b] = 50 + self.harbour_boats
                            log.write(strftime("%H:%M:%S", localtime()) \
                                      + " Good " + str(b) + " reaches the harbour\n")
                # 第三轮海盗登船
                if self.boat_pos.count(13) >= 1 and not self.pos_state[81] == -1:
                    (hijack1,direc1) = self.players[self.pos_state[81]].pirateIII(1)
                    if not hijack1 in [0,1,2,3,4]:
                        raise Exception("Invaid hijack")
                    if hijack1 > 0:
                        if self.boat_pos[hijack1] != 13:
                            raise Exception("Invaid hijack:boat not available")
                        else:
                            for pos in range(hijack1*10+1,hijack1*10+5):
                                if not self.pos_state[pos]==9:
                                    self.pos_state[pos] =-1
                            self.pos_state[hijack1*10+1]=self.pos_state[81]
                            log.write(strftime("%H:%M:%S", localtime()) + " Pirate captain Player"\
                                  + str(self.pos_state[81] + 1) + " hijacks boat " + str(hijack1) + "\n")
                            self.pos_state[81] = -1
                    if not self.pos_state[82] == -1:
                        (hijack2,direc2) = self.players[self.pos_state[82]].pirateIII(2, hijack1,direc1)
                        if not hijack2 in [0,1,2,3,4]:
                            raise Exception("Invaid hijack")
                        if hijack2 > 0:
                            if self.boat_pos[hijack2] != 13:
                                raise Exception("Invaid hijack:boat not available")
                            elif hijack2 == hijack1:
                                self.pos_state[hijack1 * 10 + 2] = self.pos_state[82]
                                log.write(strftime("%H:%M:%S", localtime()) + " Pirate sailor Player" \
                                          + str(self.pos_state[82] + 1) + " hijacks boat " + str(hijack1) + "\n")
                                self.pos_state[82] = -1
                                if direc1==5:
                                    self.harbour_boats += 1
                                    self.boat_pos[hijack1] = 50 + self.harbour_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack1) + " reaches the harbour\n")
                                elif direc1==6:
                                    self.repair_boats += 1
                                    self.boat_pos[hijack1] = 60 + self.repair_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack1) + " goes to the repair factory\n")
                            else:
                                for pos in range(hijack2 * 10 + 1, hijack2 * 10 + 5):
                                    if not self.pos_state[pos] == 9:
                                        self.pos_state[pos] = -1
                                self.pos_state[hijack2 * 10 + 1] = self.pos_state[82]
                                self.pos_state[82] = -1
                                log.write(strftime("%H:%M:%S", localtime()) + "Pirate sailor Player" \
                                          + str(self.pos_state[82] + 1) + " hijacks boat" + str(hijack2) + "\n")
                                if direc1==5:
                                    self.harbour_boats += 1
                                    self.boat_pos[hijack1] = 50 + self.harbour_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack1) + " reaches the harbour\n")
                                elif direc1==6:
                                    self.repair_boats += 1
                                    self.boat_pos[hijack1] = 60 + self.repair_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack1) + " goes to the repair factory\n")
                                if direc2==5:
                                    self.harbour_boats += 1
                                    self.boat_pos[hijack2] = 50 + self.harbour_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack2) + " reaches the harbour\n")
                                elif direc2==6:
                                    self.repair_boats += 1
                                    self.boat_pos[hijack2] = 60 + self.repair_boats
                                    log.write(strftime("%H:%M:%S", localtime()) \
                                              + " Good " + str(hijack2) + " goes to the repair factory\n")
                # 所有船确定去向
                for b in range(1,5):
                    if self.boat_pos[b]>=0 and self.boat_pos[b]<13:
                        self.repair_boats += 1
                        self.boat_pos[b] = 60 + self.repair_boats
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Good " + str(b) + " goes to the repair factory\n")
                    elif self.boat_pos[b]==13:
                        self.harbour_boats += 1
                        self.boat_pos[b] = 50 + self.harbour_boats
                        log.write(strftime("%H:%M:%S", localtime()) \
                                  + " Good " + str(b) + " reaches the harbour\n")
            assert self.harbour_boats+self.repair_boats==3
            # 股票涨价、进港船员分配利润
            for b in range(1,5):
                if self.boat_pos[b]//10==5: # 顺利进港
                    self.stockprice[b]+=5+(self.stockprice[b]>=10)*5
                    sailor=0
                    for pos in range(10*b+1,10*b+5):
                        if self.pos_state[pos]>=0 and self.pos_state[pos]<=3:
                            sailor+=1
                    if sailor>0:
                        for pos in range(10 * b + 1, 10 * b + 5):
                            if self.pos_state[pos] >= 0 and self.pos_state[pos] <= 3:
                                self.curmoney[self.pos_state[pos]]+=GOOD_GAIN[b]//sailor
                                log.write(strftime("%H:%M:%S", localtime()) \
                                          + " Player" + str(self.pos_state[pos]+1) + " gets "\
                                          +str(GOOD_GAIN[b]//sailor)+" from boat "+str(b)+"\n")
            # 码头、修理厂获利
            for pos in range(51,54):
                if self.pos_state[pos]>=0 and self.pos_state[pos] <= 3\
                    and 50+self.harbour_boats>=pos:
                    self.curmoney[self.pos_state[pos]]+=POS_GAIN[pos]
                    log.write(strftime("%H:%M:%S", localtime()) \
                              + " Player" + str(self.pos_state[pos] + 1) + " gets " \
                              + str(POS_GAIN[pos]) + " from position " + str(pos) + "\n")
            for pos in range(61,64):
                if self.pos_state[pos]>=0 and self.pos_state[pos] <= 3\
                    and 60+self.repair_boats>=pos:
                    self.curmoney[self.pos_state[pos]]+=POS_GAIN[pos]
                    log.write(strftime("%H:%M:%S", localtime()) \
                              + " Player" + str(self.pos_state[pos] + 1) + " gets " \
                              + str(POS_GAIN[pos]) + " from position " + str(pos) + "\n")
            # 保险代理人赔付
            if self.repair_boats>0 and self.pos_state[91]>=0\
                and self.pos_state[91]<=3:
                loss=[0,6,14,29]
                self.curmoney[self.pos_state[91]]-=loss[self.repair_boats]
                log.write(strftime("%H:%M:%S", localtime()) \
                          + " Player" + str(self.pos_state[91] + 1) + " pays " \
                          + str(min(loss[self.repair_boats],self.curmoney[self.pos_state[91]])) + " for insurance\n")
                self.curmoney[self.pos_state[91]]=max(0,self.curmoney[self.pos_state[91]])
            # 计算本轮排名
            for p in range(4):
                self.curtotal[p]=self.curmoney[p]-15*self.stockpledge[p]
                for b in range(1,5):
                    self.curtotal[p]+=self.stockprice[b]*self.stocknum[p][b]
            log.write(strftime("%H:%M:%S", localtime()) + " End of Round "+str(self.curround)+"\n")
            log.write(strftime("%H:%M:%S", localtime()) + " Stock price:"+str(self.stockprice[1:])+"\n")
            for p in range(4):
                log.write(strftime("%H:%M:%S", localtime()) + " Player"+str(p+1)+":"+ str(self.curmoney[p]) + " " + str(
                    self.curtotal[p] - self.curmoney[p] + 15 * self.stockpledge[p]) + " -" + str(
                    15 * self.stockpledge[p]) + " " + str(self.curtotal[p]) + "\n")
        log.write(strftime("%H:%M:%S", localtime()) + " End of Game \n")
        for p in range(4):
            log.write(strftime("%H:%M:%S", localtime()) + " Player" + str(p + 1) + ":" + str(self.curmoney[p]) + " " + str(
                    self.curtotal[p] - self.curmoney[p] + 15 * self.stockpledge[p]) + " -" + str(
                    15 * self.stockpledge[p]) + " " + str(self.curtotal[p]) + "\n")
            print("Player" + str(p + 1) + ":" + str(self.curmoney[p]) + " " + str(
                    self.curtotal[p] - self.curmoney[p] + 15 * self.stockpledge[p]) + " -" + str(
                    15 * self.stockpledge[p]) + " " + str(self.curtotal[p]))
        return

