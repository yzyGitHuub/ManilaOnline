
from Basics import Player,Board
from XiaoGuo import XiaoGuo

Guo1=XiaoGuo("Guo1")
Guo2=XiaoGuo("Guo2")
Guo3=XiaoGuo("Guo3")
Guo4=XiaoGuo("Guo4")
Idiot1=Player("Idiot1")
Idiot2=Player("Idiot2")
Idiot3=Player("Idiot3")
Idiot4=Player("Idiot4")
ManilaBoard=Board([Guo1,Guo2,Guo3,Guo4])
ManilaBoard.game_process()