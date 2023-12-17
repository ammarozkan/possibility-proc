import d1chess
import possibility_proc as PSP

import time

from random import randint

gamedata, moves, sec, score = d1chess.Game()
all_moves = []
firsttable = gamedata["table"]
print(gamedata["table"])

# data = [win,lose,draw,continue] and score = score
nottoloseplay = lambda data,score : (data[0]-data[2]-data[1]**2)
agressiveplay = lambda data,score : (data[0]**2-2*data[2]-data[1]-data[3])
justscoreplay = lambda data,score : (score)
madplay = lambda data,score : (randint(5,20)*data[0]**2+score**2 - randint(0,3)*data[1])
action = lambda data,score : (data[0]+data[3]-10*data[2]**5)
cowardplay = lambda data,score : (-data[1])/sum(data)
naturalplay = lambda data, score: (data[0]-data[1])/sum(data)

while sec == "cont":
	calc_start = time.time()

	gameproc = list(PSP.psb_proc(dict(gamedata),d1chess.Game,moves,maxdepth=8))

	calc_end = time.time()
	print(calc_end-calc_start," second passed while calculating.")
	print(gamedata["table"],gamedata["ruleofdraw"])
	moves, datas, scores = PSP.lwd_maincounter(gameproc)
	print("moves:",moves,"\ndatas:",datas,"\nscores:",scores)

	best = None
	if gamedata["turn"] == gamedata["player"]:
		best = PSP.lwd_selectbestmove(moves,datas,scores,a = 1,pointfunc = justscoreplay)
	else:
		best = PSP.lwd_selectbestmove(moves,datas,scores,a = -1,pointfunc = agressiveplay)
	#best = PSP.lwd_selectbestmove(moves,datas,a = 1 if gamedata["turn"] == gamedata["player"] else -1,pointfunc = pointcalc1 if )
	print(best[0]," with ",best[1]," points.")

	gamedata, moves, sec, point = d1chess.Game(gamedata,best[0])
	all_moves.append(gamedata["table"])
print(sec,firsttable,*all_moves,sep="\n")
if sec == "lose":
	print("agressiveplay Wins")
elif sec == "win":
	print("justscoreplay wins!")
else:
	print("draw...")