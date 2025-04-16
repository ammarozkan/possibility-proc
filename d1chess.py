 
# x__o
# x_o_
# _xo_
# _o__ o wins

# x___o
# x__o_
# _x_o_
# _x__o
# __x_o
# __xo_
# ___x_ x wins


# xx__oo
# xx_o_o
# x_xo_o
# x_xoo_
# xx_oo_
# xxo_o_
# x_x_o_
# x_x__o
# x__x_o
# x__xo_
# x___x_ x wins

# P_xx__oo_P
# Px_x__oo_P
# Px_x_o_o_P
# Px_x_oo__P
# Pxx__oo__P
# _xxP_oo__P
# x_xP_oo__P
# x_xP_oo__P

# xx__B__oo
# x_x_B__oo
# x_x_B_o_o
# x__xB__oo
# x__xBx_oo
# x__xBxo_o
# x__xB_x_o
# x__xB_xo_
# x__xB__x_ x wins

def moves(table,turn,nexturn):
    Pjump = 3
    result = []
    for i in range(0,len(table)):
        if table[i] == "_" : continue

        if table[i] == "P" and not ((i+1 < len(table) and table[i+1] == "P") or (i-1 > 0 and table[i-1] == "P")):
            if i + Pjump < len(table) and table[i+Pjump] == "_": result.append((i,i+Pjump))
            if i - Pjump > 0 and table[i-Pjump] == "_": result.append((i,i-Pjump))

        if table[i] == turn:
            pmove = (i-1 >= 0 and table[i-1] == "P") or (i+1 < len(table) and table[i+1] == "P")
            if i-1 >= 0 and table[i-1] == "P" and i+Pjump < len(table) and (table[i+Pjump] == "_" or table[i+Pjump] == nexturn):
                result.append((i,i+Pjump))
            elif i+1 < len(table) and table[i+1] == "P" and i-Pjump >= 0 and (table[i-Pjump] == "_" or table[i-Pjump] == nexturn):
                result.append((i,i-Pjump))
            elif not pmove:
                if (i+1 < len(table)) and (table[i+1] == "_" or table[i+1] == nexturn): result.append((i,i+1))
                if i-1 >= 0 and (table[i-1] == "_" or table[i-1] == nexturn): result.append((i,i-1))
    return result



def Game(data={"moves":[],"table":"P_xxx_ooo_P","turn":"o","nexturn":"x","player":"x","opponent":"o","ruleofdraw":None},nex=None):
    newdata = {"moves":list(data["moves"]),"table":str(data["table"]),"turn":data["turn"],"nexturn":data["nexturn"],"player":data["player"],"opponent":data["opponent"],"ruleofdraw":data["ruleofdraw"]}

    if nex == None:
        pass
    else:
        newdata["turn"] = data["nexturn"]
        newdata["nexturn"] = data["turn"]

    #play
    if nex != None:
        newtable = list(data["table"])
        if nex[1] >= len(newtable): print(f"FART {newtable} {nex}")

        newtable[nex[1]] = newtable[nex[0]]
        newtable[nex[0]] = "_"
        newdata["table"] = "".join(newtable)

    if nex != None: newdata["moves"] = list([a for a in data["moves"]] + [nex])

    sec = ""
    if newdata["player"] in newdata["table"] and newdata["opponent"] in newdata["table"]:
        sec = "cont"
    elif newdata["player"] not in newdata["table"] and newdata["opponent"] in newdata["table"]:
        sec = "lose"
    elif newdata["player"] in newdata["table"] and newdata["opponent"] not in newdata["table"]:
        sec = "win"

    if newdata["ruleofdraw"] != None and newdata["ruleofdraw"][0] == newdata["table"].count(newdata["player"]) and newdata["ruleofdraw"][1] == newdata["table"].count(newdata["opponent"]):
        newdata["ruleofdraw"] = (newdata["ruleofdraw"][0],newdata["ruleofdraw"][1],newdata["ruleofdraw"][2]+1)
    else: newdata["ruleofdraw"] = (newdata["table"].count(newdata["player"]),newdata["table"].count(newdata["opponent"]),0)

    nextmoves = moves(newdata["table"],newdata["turn"],newdata["nexturn"])
    if sec=="cont" and (newdata["ruleofdraw"][2] == 15 or len(nextmoves) == 0):
        if newdata["table"].count(newdata["player"]) > newdata["table"].count(newdata["opponent"]): sec = "win"
        elif newdata["table"].count(newdata["player"]) < newdata["table"].count(newdata["opponent"]): sec = "lose"
        else: sec="draw"
    #if len(newdata["moves"]) == 1: sec="win"


    return dict(newdata), nextmoves, sec, (newdata["table"].count(newdata["player"])-newdata["table"].count(newdata["opponent"]))
