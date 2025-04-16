import d1chess
import possibility_proc as PSP

import time

from random import randint
from random import choice,shuffle


debugpr = False
def debugprint(*args,sep="\n"):
	global debugpr
	if debugpr: print(*args,sep=sep)
	else: pass


def humanplay(name,table,moves):
	print(f"TURN FOR {name}! TABLE:")
	print(table)
	for i in range(0,len(table)):
		print(i,end="")
	print()
	print(f"MOVES:")
	for i in range(0,len(moves)):
		print(f"{i}:{moves[i]}")
	selection = int(input("nm:"))
	print(f"{selection}! playing {moves[selection]} !!")
	return (moves[selection],100)

def playthem(p1name, p1, p2name, p2,table="default"):
	gamedata, moves, sec, score = d1chess.Game()
	print(moves)

	all_moves = []
	if table == "default": firsttable = gamedata["table"]
	else :
		firsttable = table
		gamedata["table"] = table
	gamedata, moves, sec, score = d1chess.Game(data=gamedata)
	#debugprint(gamedata["table"])

	while sec == "cont":
		calc_start = time.time()

		gameproc = list(PSP.psb_proc(dict(gamedata),d1chess.Game,moves,maxdepth=8))

		calc_end = time.time()
		debugprint(calc_end-calc_start," second passed while calculating.")
		print(gamedata["table"],gamedata["ruleofdraw"])
		moves, datas, scores = PSP.lwd_maincounter(gameproc)
		debugprint("moves:",moves,"\ndatas:",datas,"\nscores:",scores)

		best = None
		if gamedata["turn"] == gamedata["player"]:
			if p1name[0:len("HUMANPLAYER")] == "HUMANPLAYER": best = humanplay(p1name,gamedata["table"],moves)
			else : best = PSP.lwd_selectbestmove(moves,datas,scores,a = 1,pointfunc = p1)
		else:
			if p2name[0:len("HUMANPLAYER")] == "HUMANPLAYER": best = humanplay(p2name,gamedata["table"],moves)
			else: best = PSP.lwd_selectbestmove(moves,datas,scores,a = -1,pointfunc = p2)
		#best = PSP.lwd_selectbestmove(moves,datas,a = 1 if gamedata["turn"] == gamedata["player"] else -1,pointfunc = pointcalc1 if )
		debugprint(best[0]," with ",best[1]," points.")

		gamedata, moves, sec, point = d1chess.Game(gamedata,best[0])
		all_moves.append(gamedata["table"])
	debugprint(sec,firsttable,*all_moves,sep="\n")
	if sec == "lose":
		print(f"{p2name} Wins against {p1name}")
		return 2
	elif sec == "win":
		print(f"{p1name} wins against {p2name}")
		return 1
	else:
		print(f"draw... {p1name}-{p2name}")
		return 0

# data = [win,lose,draw,continue] and score = score
nottoloseplay = lambda data,score : (data[0]-data[2]-data[1]**2)
notloseplay = lambda data,score : (data[0]-data[1]**2)
agressiveplay = lambda data,score : (data[0]**2-2*data[2]-data[1]-data[3])
justscoreplay = lambda data,score : (score)
madplay = lambda data,score : (randint(5,20)*data[0]**2+score**2 - randint(0,3)*data[1])
action = lambda data,score : (data[0]+data[3]-10*data[2]**5)
cowardplay = lambda data,score : (-data[1])/sum(data)
naturalplay = lambda data, score: (data[0]-data[1])/sum(data)


players1 = [("magnuscarslen",notloseplay),("HUMANPLAYERJACK",None)]
players2 = []

players = players1

draws = dict()

tables = ["oP_PP_P_x_o_P_PP_Px","x___P__P___o","xxxx_oooo","P_P_PP__x_o__PP_P_P","xxoxxPooxoo"]

def getwinner(players):
	shuffle(players)
	print(f"match ",end='\t')
	for pl in players:
		print(f"{pl[0]}",end='-')
	print()
	if len(players) == 0: return []
	elif len(players) == 1: return [players[0]]
	elif len(players) == 2:
		table = "default"
		if str([players[0],players[1]]) in draws: table = choice(tables)
		rs = playthem(players[0][0],players[0][1],players[1][0],players[1][1],table=table)
		if rs == 1: return [players[0]]
		elif rs == 2: return [players[1]]
		elif rs == 0:
			draws[str([players[0],players[1]])] = True
			return [players[0],players[1]]
	elif len(players) == 3:
		wn = getwinner([players[0],players[1]])
		if len(wn) == 1:
			return getwinner([wn[0],players[2]])
		else: return getwinner([players[2],players[0],players[1]])
	else:
		group1 = players[:int(len(players)/2)]
		group2 = players[int(len(players)/2):]
		return getwinner(getwinner(group1)+getwinner(group2))

print("WINNER:",getwinner(players))

#playthem("nottoloseplay",nottoloseplay,"naturalplay",naturalplay)
