from Scripts.Python.mining.mining_Sand.Checker import *


def MoveIn(to):
    rout = {}
    if to == 'locMagincia':  # Go in to mining sand
        rout = {'locNewbies': [4214, 2883]}
    elif to == 'locNewbies':  # go in to processed
        rout = {'locMagincia': [3564, 2140]}

    CheckConnect()
    CheckDead()
    getLock = GetLock()
    if to == getLock:
        return True
    msg(f'Move in to {to}')
    for i in range(5):
        if IsGump():
            CloseSimpleGump(0)
    x, y = rout[getLock][0], rout[getLock][1]
    CheckSave()
    if GetX(Self()) == x and GetY(Self()) == y:
        NewMoveXY(x + 1, y, True, 0, True)
    while NewMoveXY(x, y, True, 0, True):
        t = 0
        while not IsGump() and t <= 50:
            if not CheckConnect() or not CheckDead():
                return False
            Wait(100)
            t += 1
        CheckSave()
        if not IsGump():
            NewMoveXY(x + 1, y, True, 0, True)
        else:
            NumGumpRadiobutton(GetGumpsCount() - 1, 2049, 0)
            NumGumpRadiobutton(GetGumpsCount() - 1, 2056, 1)
            NumGumpButton(GetGumpsCount() - 1, 1025)
            t = 0
            while GetLock() != to and t <= 100:
                Wait(100)
                t += 1
            if GetLock == to:
                return True


def GoToBank():
    getLock = GetLock()
    if getLock == 'locMagincia':  # Go to Magincia bank
        x, y = 3717, 2172
    elif getLock == 'locNewbies':  # Go to Newbies bank
        x, y = 4230, 2835
    else:
        return False
    t = 0
    msg(f"go to bank in {getLock}")
    while GetX(Self()) != x or GetY(Self()) != y:
        CheckSave()
        newMoveXYZ(x, y, 0, 0, 100, True)
        Wait(1000)
        t += 1
        if t >= 5 or not Connected() or Dead() or not CheckLag(15000):
            return False
    vendorList = FindVendor()
    for _vendorList in vendorList:
        x, y, z, vendorID = GetX(_vendorList[0]), GetY(_vendorList[0]), \
                            GetZ(_vendorList[0]), _vendorList[0]
        while GetDistance(vendorID) > 1:
            CheckConnect(), CheckSave(), CheckLag(), CheckDead()
            newMoveXYZ(x, y, z, 1, 100, True)
        if _return := OpenBank():
            return _return
    return False
