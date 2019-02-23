from Basics import Player,POS_GAIN,POS_COST,GOOD_GAIN
from numpy import random

class XiaoGuo(Player):
    def bid(self,Curprice=0):
        # Curprice:当前报价
        wtp=min(20,self.board.curmoney[self.turn]-15) # Will to pay
        if Curprice<wtp:
            return (Curprice+1,0)
        else:
            return (-1,0) # -1代表退出竞拍，0代表不抵押股票


    def master(self):
        # 购买股票，按1+已有股票为权重随机选择，若无效重选，反复三次
        prob=[-1,1,1,1,1]
        for b in range(1,5):
            prob[b]+=self.board.stocknum[self.turn][b]
        psum=prob[1]+prob[2]+prob[3]+prob[4]
        for b in range(1,5):
            prob[b]/=psum
        buystock=random.choice([1,2,3,4],p=[prob[1],prob[2],prob[3],prob[4]])
        if self.board.stockremain[buystock]==0 or self.board.stockprice[buystock]>self.board.curmoney[self.turn]:
            buystock = random.choice([1, 2, 3, 4])
            if self.board.stockremain[buystock] == 0 or self.board.stockprice[buystock] > self.board.curmoney[
                self.turn]:
                buystock = random.choice([1, 2, 3, 4])
                if self.board.stockremain[buystock] == 0 or self.board.stockprice[buystock] > self.board.curmoney[
                    self.turn]:
                    buystock = 0
        # 放置船只
        boatpos=[-1,0,0,0,0]
        for b in range(1,5):
            if self.board.stocknum[self.turn][b]>=2:
                boatpos[b]=5
            elif self.board.stocknum[self.turn][b]==1:
                boatpos[b]=4
            else:
                boatpos[b]=3
        for b in range(1,5):
            if boatpos[b]==3:
                boatpos[b]=-1
                break
        while boatpos[1]+boatpos[2]+boatpos[3]+boatpos[4]>8:
            reduct=False
            for b in range(1, 5):
                if boatpos[b] <=3 and boatpos[b]>0:
                    boatpos[b] -=1
                    reduct=True
                    break
            if not reduct:
                for b in range(1, 5):
                    if boatpos[b] ==4:
                        boatpos[b] -=1
                        reduct=True
                        break
            if not reduct:
                for b in range(1, 5):
                    if boatpos[b] ==5:
                        boatpos[b] -=1
                        break
        return [boatpos[1],boatpos[2],boatpos[3],boatpos[4],buystock,0]


    def place_retinue(self):
        choice=0
        gain=0
        if self.board.curstage==1:
            for pos in [11,12,13,21,22,23,31,32,33,41,42,43,44]:
                if not self.board.pos_state[pos]==-1:
                    continue
                if POS_COST[pos]>self.board.curmoney[self.turn]:
                    continue
                curgain=self.board.boat_pos[pos//10]-pos%10
                if curgain>gain:
                    gain=curgain
                    choice=pos
        elif self.board.curstage==2:
            prob=[0,1/36,1/12,1/6,5/18,5/12,7/12,13/18,5/6,11/12,35/36,1,1,1]
            # 只考虑掷骰子，当前位置为0-13的船到港的概率
            boat_occ=[-1,0,0,0,0]
            boat_occ[1]=(self.board.pos_state[11]>=0)+(self.board.pos_state[12]>=0)+(self.board.pos_state[13]>=0)
            boat_occ[2] = (self.board.pos_state[21] >= 0) + (self.board.pos_state[22] >= 0) + (
                        self.board.pos_state[23] >= 0)
            boat_occ[3] = (self.board.pos_state[31] >= 0) + (self.board.pos_state[32] >= 0) + (
                        self.board.pos_state[33] >= 0)
            boat_occ[4] = (self.board.pos_state[41] >= 0) + (self.board.pos_state[42] >= 0) + (
                        self.board.pos_state[43] >= 0)+(self.board.pos_state[44] >= 0)
            # 各船已有人数
            for pos in [11,12,13,21,22,23,31,32,33,41,42,43,44]:
                if not self.board.pos_state[pos]==-1:
                    continue
                if POS_COST[pos]>self.board.curmoney[self.turn]:
                    continue
                curgain=prob[self.board.boat_pos[pos//10]]*(GOOD_GAIN[pos//10]/(boat_occ[pos//10]+1))\
                    -POS_COST[pos]
                if curgain>gain:
                    gain=curgain
                    choice=pos
            exp_harbour=0
            for b in range(1,5):
                if self.board.boat_pos[b]==-1:
                    continue
                exp_harbour+=prob[self.board.boat_pos[b]]
            for pos in [51,52,53]:
                if not self.board.pos_state[pos]==-1:
                    continue
                if POS_COST[pos]>self.board.curmoney[self.turn]:
                    continue
                if pos%10>exp_harbour+0.3:
                    continue
                curgain=POS_GAIN[pos]-POS_COST[pos]
                if curgain>gain:
                    gain=curgain
                    choice=pos
            for pos in [61,62,63]:
                if not self.board.pos_state[pos]==-1:
                    continue
                if POS_COST[pos]>self.board.curmoney[self.turn]:
                    continue
                if pos%10>3-exp_harbour+0.3:
                    continue
                curgain=POS_GAIN[pos]-POS_COST[pos]
                if curgain>gain:
                    gain=curgain
                    choice=pos
            for pos in [91]:
                if not self.board.pos_state[pos]==-1:
                    continue
                if exp_harbour<2:
                    continue
                curgain=4+6*(exp_harbour-2)
                if curgain>gain:
                    gain=curgain
                    choice=pos
        elif self.board.curstage == 3:
            prob = [0, 0, 0, 0, 0,0,0,1/6,1/3,1/2, 2/3, 5/6, 1, 1]
            # 只考虑掷骰子，当前位置为0-13的船到港的概率
            boat_occ = [-1, 0, 0, 0, 0]
            boat_occ[1] = (self.board.pos_state[11] >= 0) + (self.board.pos_state[12] >= 0) + (
                        self.board.pos_state[13] >= 0)
            boat_occ[2] = (self.board.pos_state[21] >= 0) + (self.board.pos_state[22] >= 0) + (
                    self.board.pos_state[23] >= 0)
            boat_occ[3] = (self.board.pos_state[31] >= 0) + (self.board.pos_state[32] >= 0) + (
                    self.board.pos_state[33] >= 0)
            boat_occ[4] = (self.board.pos_state[41] >= 0) + (self.board.pos_state[42] >= 0) + (
                    self.board.pos_state[43] >= 0) + (self.board.pos_state[44] >= 0)
            # 各船已有人数
            for pos in [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43, 44]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if POS_COST[pos] > self.board.curmoney[self.turn]:
                    continue
                curgain = prob[self.board.boat_pos[pos // 10]] * (GOOD_GAIN[pos // 10] / (boat_occ[pos // 10] + 1)) \
                          - POS_COST[pos]
                if curgain > gain:
                    gain = curgain
                    choice = pos
            exp_harbour = self.board.harbour_boats
            # 考虑码头、修理厂
            for b in range(1, 5):
                if self.board.boat_pos[b] == -1 or self.board.boat_pos[b] >=50:
                    continue
                exp_harbour += prob[self.board.boat_pos[b]]
            for pos in [51, 52, 53]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if POS_COST[pos] > self.board.curmoney[self.turn]:
                    continue
                if pos % 10 > exp_harbour + 0.3:
                    continue
                curgain = POS_GAIN[pos] - POS_COST[pos]
                if curgain > gain:
                    gain = curgain
                    choice = pos
            for pos in [61, 62, 63]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if POS_COST[pos] > self.board.curmoney[self.turn]:
                    continue
                if pos % 10 > 3 - exp_harbour + 0.3:
                    continue
                curgain = POS_GAIN[pos] - POS_COST[pos]
                if curgain > gain:
                    gain = curgain
                    choice = pos
            # 考虑做海盗
            pirategain=0
            for b in range(1,5):
                if self.board.boat_pos[b]<13 and self.board.boat_pos[b]>6:
                    pirategain+=GOOD_GAIN[b]
            for pos in [81,82]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if POS_COST[pos] > self.board.curmoney[self.turn]:
                    continue
                curgain = pirategain/(6+2*(pos%10)) - POS_COST[pos]
                if curgain > gain:
                    gain = curgain
                    choice = pos
            # 考虑代理保险
            for pos in [91]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if exp_harbour < 2:
                    continue
                curgain = 4 + 6 * (exp_harbour - 2)
                if curgain > gain:
                    gain = curgain
                    choice = pos
            # 以一定概率上领航操盘，向宇宙最伟大的操盘手致敬
            for pos in [71,72]:
                if not self.board.pos_state[pos] == -1:
                    continue
                if POS_COST[pos] > self.board.curmoney[self.turn]:
                    continue
                if gain>4:
                    continue
                rand=random.randint(100)
                if rand>=40 and rand<40+10*(3-pos%10):
                    choice=pos
        return (choice,0)
    def move_boat(self,type):
        # type为1：小领航，type为2：大领航
        determined=False
        move=[-1,0,0,0,0]
        for b in range(1,5):
            if self.board.boat_pos[b]>=7 and self.board.boat_pos[b]<=10:
                if self.board.pos_state[b*10+1]==self.turn or self.board.pos_state[b*10+2]==self.turn\
                    or self.board.pos_state[b*10+3]==self.turn or self.board.pos_state[b*10+4]==self.turn:
                    move[b]=type
                    determined=True
                    break
        if not determined:
            for b in range(1, 5):
                if self.board.boat_pos[b] >= 7 and self.board.boat_pos[b] <= 10:
                    if self.board.pos_state[b * 10 + 1] != self.turn and self.board.pos_state[b * 10 + 2] != self.turn \
                            and self.board.pos_state[b * 10 + 3] != self.turn and self.board.pos_state[
                        b * 10 + 4] != self.turn:
                        move[b] = -type
                        determined = True
                        break
        if not determined:
            for b in range(1, 5):
                if self.board.boat_pos[b] >=11:
                    if self.board.pos_state[b * 10 + 1] == self.turn or self.board.pos_state[b * 10 + 2] == self.turn \
                            or self.board.pos_state[b * 10 + 3] == self.turn or self.board.pos_state[
                        b * 10 + 4] == self.turn:
                        move[b] = type
                        determined = True
                        break
        if not determined:
            for b in range(1, 5):
                if self.board.boat_pos[b] >= 11:
                    if self.board.pos_state[b * 10 + 1] != self.turn and self.board.pos_state[b * 10 + 2] != self.turn \
                            and self.board.pos_state[b * 10 + 3] != self.turn and self.board.pos_state[
                        b * 10 + 4] != self.turn:
                        move[b] = -type
                        break
        return (move[1],move[2],move[3],move[4])

    def pirateIII(self,type,captain_boat=-1,captain_choice=5):
        # type为1：海盗船长，此时后两个参数无意义
        # type为2：海盗船员，此时captain_boat为船长所选船的货物类型（1-4）
        # captain_choice为该船的去向（5代表港口，6代表修理厂）
        gain=0
        pirate_boat=0
        if type==1:
            for b in range(1,5):
                if not self.board.boat_pos[b]==13:
                    continue
                if GOOD_GAIN[b]>gain:
                    gain=GOOD_GAIN[b]
                    pirate_boat=b
        elif type==2:
            for b in range(1,5):
                if not self.board.boat_pos[b]==13:
                    continue
                if GOOD_GAIN[b]/(1+(b==captain_boat))>gain:
                    gain=GOOD_GAIN[b]/(1+(b==captain_boat))
                    pirate_boat=b
        return (pirate_boat,5) # 第一个返回值为所选船的货物类型，第二个返回值为船的去向
