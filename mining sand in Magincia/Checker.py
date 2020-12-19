from py_stealth import *
from Scripts.Python.Include.all import msg, CheckConnect, CheckSave


def GetLock():
    locNewbies = {'Name': 'locNewbies',
                  'MinX': 4185, 'MaxX': 4403,
                  'MinY': 2711, 'MaxY': 2948}

    locMagincia = {'Name': 'locMagincia',
                   'MinX': 3420, 'MaxX': 3838,
                   'MinY': 1940, 'MaxY': 2320}

    loc = [locNewbies, locMagincia]
    x = GetX(Self())
    y = GetY(Self())
    for i in loc:
        if (x >= i.get('MinX')) and (x <= i.get('MaxX')):
            if (y >= i.get('MinY')) and (y <= i.get('MaxY')):
                return i.get('Name')
    return False


def FindVendor():
    dist = GetFindDistance()
    SetFindDistance(18)
    vendorType = [0x0190, 0x0191]
    vendorID = []
    for _vt in vendorType:
        FindType(_vt, Ground())
        findList = GetFindedList()
        if len(findList) <= 0:
            continue
        for _vi in findList:
            if "Invulnerable" in GetTooltip(_vi):
                vendorID.append([0] * 2)
                vendorID[len(vendorID) - 1][0] = _vi
                vendorID[len(vendorID) - 1][1] = GetDistance(_vi)
    SetFindDistance(dist)
    if len(vendorID) > 0:
        vendorID.sort(key=lambda i: i[1])
        return vendorID
    return False


def OpenBank():
    for i in range(11):
        CheckConnect()
        if Dead():
            return False
        CheckSave()
        UseObject(Backpack())
        CheckLag()
        if LastContainer() == Backpack():
            break
        if i == 11:
            return False
    for i in range(5):
        CheckConnect()
        if Dead():
            return False
        CheckSave()
        UOSay("bank")
        t = 0
        while LastContainer() != ObjAtLayer(BankLayer()) and t <= 30:
            CheckSave()
            Wait(100)
            t += 1
        if LastContainer() == ObjAtLayer(BankLayer()):
            return ObjAtLayer(BankLayer())
    return False


def CheckDead(WaitTimeResSec=0):
    if Dead():
        msg("You are dead :|")
        if WaitTimeResSec:
            msg(f"... need wait {WaitTimeResSec} sec...")
            Wait(WaitTimeResSec*1000)
        msg("let's go resurrect!")
        CheckConnect(), CheckSave()
        locNewbies = {'Name': 'locNewbies', 'x': 4248, 'y': 2912}
        locMagincia = {'Name': 'locMagincia', 'x': 3699, 'y': 2047}
        loc = [locNewbies, locMagincia]
        getLock = GetLock()
        for i in loc:
            if i.get('Name') == getLock:
                loc = i
                break
        while Dead():
            CheckConnect()
            CheckSave()
            NewMoveXY(loc.get('x'), loc.get('y'), True, 0, True)
            NewMoveXY(loc.get('x') + 1, loc.get('y'), True, 0, True)
    return True
