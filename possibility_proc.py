#game function should be
#data, nexts, sec = game(data,move)

def psb_proc(data,game,nexts,depth=0,maxdepth=-1):
    if depth == 0 : data["moves"] = []
    yielded = False
    for i in range(0,len(nexts)):
        yielded = True
        datai, nextsi, sec, score = game(data,nexts[i])
        if sec == "cont" and depth != maxdepth:
            yield from psb_proc(datai,game,nextsi,depth+1,maxdepth)
        else : yield (datai, sec, score)
    if not yielded:
        datai, nextsi, sec, score = game(data)
        yield (datai,sec, score)


def lwd_counter(dd):
    result = {"win":0,"lose":0,"draw":0}
    for d in dd:
        match d[1]:
            case "win":
                result["win"]+=1
            case "lose":
                result["lose"]+=1
            case "draw":
                result["draw"]+=1
    return result

def lwdmove_counter(dd):
    result = {} #"(1,2)":[wincount,losecount,drawcount,continuecount]
    for d in dd:
        match d[1]:
            case "win":
                if len(d[0]["moves"]) != 0:
                    if str(d[0]["moves"][0]) in result: result[str(d[0]["moves"][0])][0]+=1
                    else : result[str(d[0]["moves"][0])] = [1,0,0,0]
            case "lose":
                if len(d[0]["moves"]) != 0:
                    if str(d[0]["moves"][0]) in result: result[str(d[0]["moves"][0])][1]+=1
                    else : result[str(d[0]["moves"][0])] = [0,1,0,0]
            case "draw":
                if len(d[0]["moves"]) != 0:
                    if str(d[0]["moves"][0]) in result: result[str(d[0]["moves"][0])][2]+=1
                    else : result[str(d[0]["moves"][0])] = [0,0,1,0]
            case "cont":
                if len(d[0]["moves"]) != 0:
                    if str(d[0]["moves"][0]) in result: result[str(d[0]["moves"][0])][3]+=1
                    else : result[str(d[0]["moves"][0])] = [0,0,0,1]
    return result

def lwdbestpercent_counter(dd):
    result = {}
    rr = lwdmove_counter(dd)
    for r in rr:
        result[r] = 100*(rr[r][0]-rr[r][1])/sum(rr[r])
    return result

def lwdpoint(data,score):
    return (data[0]**2-2*data[2]-data[1]-data[3])/sum(data)

# data returns [wins,loses,draws,continues]
def lwd_maincounter(dd):
    moves = []
    datas = []
    scores= []

    for d in dd:
        firstmove = d[0]["moves"][0] if len(d[0]["moves"]) != 0 else ["None"]
        hadmove = firstmove in moves
        if hadmove: scores[moves.index(firstmove)] += d[2]
        else: scores.append(d[2])
        match d[1]:
            case "win":
                if hadmove: datas[moves.index(firstmove)][0]+=1
                else : 
                    moves.append(firstmove)
                    datas.append([1,0,0,0])
            case "lose":
                if hadmove: datas[moves.index(firstmove)][1]+=1
                else : 
                    moves.append(firstmove)
                    datas.append([0,1,0,0])
            case "draw":
                if hadmove: datas[moves.index(firstmove)][2]+=1
                else : 
                    moves.append(firstmove)
                    datas.append([0,0,1,0])
            case "cont":
                if hadmove: datas[moves.index(firstmove)][3]+=1
                else : 
                    moves.append(firstmove)
                    datas.append([0,0,0,1])

    for i in range(0,len(scores)):
        scores[i] = scores[i]/sum(datas[i])

    return moves,datas,scores

def lwd_selectbestmove(moves,datas,scores,a=1,pointfunc=lwdpoint): # a should be -1 if opponent plays
    best = (moves[0],lwdpoint(datas[0],scores[0])*a) # move point

    for i in range(0,len(datas)):
        np = pointfunc(datas[i],scores[i])
        if best[1] < np*a : best = (moves[i],np)

    return best
