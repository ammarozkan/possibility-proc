
import d1chess
import possibility_proc as PSP

import time

elapse = []

for j in range(0,4):
	gamedata, moves, sec, score = d1chess.Game()
	all_moves = [[] for i in range(0,15)]
	firsttable = gamedata["table"]
	print(gamedata["table"])
	calc_start = time.time()
	for i in range(0,13):
		print("Currently working on ",i," depth.")
		gamedata, moves, sec, score = d1chess.Game()
		while sec == "cont":
			calc_start = time.time()

			gameproc = list(PSP.psb_proc(dict(gamedata),d1chess.Game,moves,maxdepth=i))

			calc_end = time.time()
			moves,datas,scores = PSP.lwd_maincounter(gameproc)
			best = PSP.lwd_selectbestmove(moves,datas,scores,a = 1 if gamedata["turn"] == gamedata["player"] else -1)

			gamedata, moves, sec, score = d1chess.Game(gamedata,best[0])
			all_moves[i].append(gamedata["table"])
	calc_end = time.time()
	print(calc_end-calc_start)
	print(all_moves)
	elapse.append(calc_end-calc_start)

print(sum(elapse)/len(elapse))
