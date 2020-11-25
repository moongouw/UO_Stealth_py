import csv
import os
from datetime import *
from Scripts.Python.Include.all import *
from py_stealth import *

LOC_FILE = 'coordinates.csv'
RADIUS_D = 3
TOOL_TYPE = 0x0E85
MAX_SAND_COUNT_PROCESSED = 10000
TRADER = 0x0002F2B7


def GetLock():
    locNewbies = {'Name': 'locNewbies',
                  'MinX': 4185, 'MaxX': 4403,
                  'MinY': 2711, 'MaxY': 2948}

    locMarket = {'Name': 'locMarket',
                 'MinX': 2070, 'MaxX': 2225,
                 'MinY': 751, 'MaxY': 900}

    locBrit = {'Name': 'locBrit',
               'MinX': 1280, 'MaxX': 1740,
               'MinY': 1480, 'MaxY': 1820}

    _loc = [locNewbies, locMarket, locBrit]
    x = GetX(Self())
    y = GetY(Self())
    for _i in _loc:
        if (x >= _i.get('MinX')) and (x <= _i.get('MaxX')):
            if (y >= _i.get('MinY')) and (y <= _i.get('MaxY')):
                return _i.get('Name')
    return False


def Respawn(_location):
    locNewbies = {'Name': 'locNewbies', 'x': 4248, 'y': 2912}
    locMarket = {'Name': 'locMarket', 'x': 2129, 'y': 848}
    locBrit = {'Name': 'locBrit', 'x': 1491, 'y': 1720}
    _loc = [locNewbies, locMarket, locBrit]

    for _i in _loc:
        if _i.get('Name') == _location:
            _loc = _i
            break
    if Dead():
        msg("You are dead :|")
        msg("let's go resurrect!")
    while Dead():
        CheckConnect()
        NewMoveXY(_loc.get('x'), _loc.get('y'), True, 0, True)
        NewMoveXY(_loc.get('x') + 1, _loc.get('y'), True, 0, True)


def CheckDead():
    if not CheckConnect():
        return False
    if Dead():
        Respawn(GetLock())
    return True


def MoveIn(to):
    _rout = {}
    if to == 'locBrit':  # Go in to mining sand
        _rout = {'locNewbies': [4214, 2883], 'locMarket': [2129, 853]}
    elif to == 'locNewbies':  # go in to processed
        _rout = {'locBrit': [1415, 1688], 'locMarket': [2154, 828]}
    if not CheckConnect() or not CheckDead():
        return False
    msg(f'Move in to {to}')
    while _getLock := GetLock():
        if to == _getLock:
            return True
        while _gumpCount := GetGumpsCount():
            if IsGumpCanBeClosed(_gumpCount - 1):
                CloseSimpleGump(_gumpCount - 1)
            else:
                CloseSimpleGump(_gumpCount - 1)
        while not NewMoveXY(_rout[_getLock][0], _rout[_getLock][1], True, 0, True):
            CheckConnect()
            CheckSave()
            CheckLag(15000)
            Wait(5000)
        _findDist = GetFindDistance()
        SetFindDistance(0)
        if _item := FindType(0x1822, Ground()):
            while GetLock() == _getLock:
                CheckSave()
                CheckLag(15000)
                _x = GetX(Self())
                t = 0
                UOSay('market brit')
                while (_x == GetX(Self())) and (t <= 50):
                    if not CheckConnect():
                        return False
                    Wait(50)
                    t += 1
        SetFindDistance(_findDist)
        if IsGump():
            NumGumpRadiobutton(GetGumpsCount() - 1, 2049, 0)
            NumGumpRadiobutton(GetGumpsCount() - 1, 2057, 1)
            NumGumpButton(GetGumpsCount() - 1, 1025)
    return False


def WaitTargetOnSelf():
    if TargetPresent():
        CancelTarget()
    msg(f'...stand on the tile around which we will dig (radius: {RADIUS_D})...')
    msg('...point to yourself to write the coordinates of the tile...')
    ClientRequestObjectTarget()
    while not ClientTargetResponsePresent():
        Wait(50)
    if LastTarget() == Self():
        return ClientTargetResponse()
    else:
        msg('... you missed, try again ...')
        return False


def LocFileRecord(file):
    """CheckConnect()
    msg('...moving in to beach Britannia for recording coordinates...')
    MoveIn('locBrit')
    while not NewMoveXY(1572, 1749, True, 0, True):
        CheckConnect()
        CheckSave()
        Wait(50)"""
    t = False
    while not t:
        t = WaitTargetOnSelf()
        Wait(50)
    with open(file, 'a') as file:
        csv.writer(file).writerow([CharName(), Self(), t['X'], t['Y']])
    msg('...coordinates received and written to file...')
    msg(LOC_FILE)
    return {'x': t['X'], 'y': t['Y']}


def LocFileCreate():
    msg(f'...file {LOC_FILE} not found...')
    workFile = os.path.join(os.path.dirname(__file__), LOC_FILE)
    with open(workFile, 'a'):
        msg(f"...file {LOC_FILE} is created...")
        msg(f"path new file: {workFile}")
        return workFile


def LocFileRecordSearch(file):
    CheckConnect()
    with open(file) as f:
        for line in csv.reader(f):
            if (len(line) == 4) and (int(line[1]) == Self()):
                return {'x': int(line[2]), 'y': int(line[3])}
    return False


def LocFileSearch():
    find_dir = os.path.join(os.path.dirname(__file__))
    found_file = os.listdir(find_dir)
    for _i in found_file:
        if _i in LOC_FILE:
            return os.path.join(os.path.dirname(__file__), LOC_FILE)


def GetLocInfoChar():
    file = LocFileSearch()
    _return = False
    if not file:
        file = LocFileCreate()
    else:
        _return = LocFileRecordSearch(file)
    if not _return:
        _return = LocFileRecord(file)
    return _return


def Mining_Sand(tool, tile=0, x=Self(), y=Self(), z=Self()):
    if not tool:
        return False
    if TargetPresent():
        CancelTarget()
    if MenuPresent():
        CancelMenu()
    if not CheckConnect() or Dead() or not CheckLag(15000):
        return False
    if Dist(x, y, GetX(Self()), GetY(Self())) > 2:
        if not NewMoveXY(x, y, True, 21, True):
            msg(f"can't not moving out х{GetX(Self())} y{GetY(Self())} in x{x} y{y}")
            return False
    ct = datetime.now()
    msgC("mining")
    while not TargetPresent() and Connected() and not Dead():
        UseObject(tool)
        if WaitForTarget(10000):
            break
    TargetToTile(tile, x, y, z)
    if WaitJournal(
            "That is too far away.|"
            "You can't mine or dig anything there.|"
            "You stop mining.", ct, 30):
        return WaitJournal(
            "That is too far away.|"
            "You can't mine or dig anything there.|"
            "There's no sand left there.", ct, 0)
    return False


def CheckTool():
    layer = [ObjAtLayer(RhandLayer()), ObjAtLayer(LhandLayer())]
    for tool in layer:
        if GetType(tool) == TOOL_TYPE:
            return tool
    tool = FindType(TOOL_TYPE, Backpack())
    if FindCount() > 0:
        return tool
    return False


def CheckPos(xyz=1):
    if xyz == 1:
        xyz = {'x': 4264, 'y': 2883}  # in house
        NewMoveXY(4267, 2889, True, 0, True)
    else:
        xyz = {'x': 4267, 'y': 2889}  # out house
    while (GetX(Self()) != xyz['x']) or (GetY(Self()) != xyz['y']):
        newMoveXYZ(xyz['x'], xyz['y'], 1, 0, 100, True)
        Wait(1000)


def Sand():
    CheckConnect()
    FindTypeEx(0x0EED, 0x083B, Backpack(), False)
    if FindFullQuantity() > 0:
        CheckPos(1)
        SetFindDistance(1)
        forge = FindType(0x0FB1, Ground())
        if not forge:
            msg("ERROR: can't find a forge!")
            return
        while sand := FindTypeEx(0x0EED, 0x083B, Backpack(), False):
            msgC(f'Count sand: {FindFullQuantity()}')
            if TargetPresent():
                CancelTarget()
            tTime = datetime.now()
            UseObject(sand)
            WaitForTarget(15000)
            if TargetPresent():
                WaitTargetObject(forge)
            WaitJournal('Success.|Failed.', tTime)
        if FindFullQuantity() <= 0:
            msg('Sand processing is over!')
        CheckConnect()


def CreateBottle():
    CheckConnect()
    CancelMenu()
    AutoMenu('What', 'Alchemical Tools')
    AutoMenu('What', 'Empty Bottle')
    while True:
        CheckConnect()
        tool = FindType(0x1EBC, Backpack())
        if not tool:
            msg('ERROR: not found Tinker tool in backpack self!')
            return
        resource = FindType(0x1BF5, Backpack())
        if FindFullQuantity() < 20:
            FindType(0x0F0E, Backpack())
            msg("Craft bottle is finished!")
            msg(f"Total bottles crafted: {FindFullQuantity()}")
            return FindItem()
        msgC(f"ing all: {FindFullQuantity()}/{(FindFullQuantity() // 20)}")
        Hungry()
        if TargetPresent():
            CancelTarget()
        UseObject(tool)
        ct = datetime.now()
        if WaitForTarget(5000):
            WaitTargetObject(resource)
        WaitJournal('You stop.|Stop.', ct)


def Sell(bott):
    CheckConnect()
    oldDist = GetFindDistance()
    if oldDist < 18:
        SetFindDistance(18)
    vendorType = [0x0190, 0x0191]
    vendorID = []
    for _vt in vendorType:
        FindType(_vt, Ground())
        findList = GetFindedList()
        for _vi in findList:
            if "Invulnerable" in GetTooltip(_vi):
                vendorID.append([0] * 2)
                vendorID[len(vendorID)-1][0] = _vi
                vendorID[len(vendorID)-1][1] = GetDistance(_vi)
    vendorID.sort(key=lambda i: i[1])
    vendorID = vendorID[0][0]
    SetFindDistance(oldDist)
    if GetQuantity(bott):
        msg(f"Sell bottles to vendor name: {GetName(vendorID)}")
        while GetDistance(vendorID) > 0:
            CheckConnect()
            if NewMoveXY(GetX(vendorID), GetY(vendorID), True, 0, True):
                break
        if TargetPresent():
            CancelTarget()
        UOSay('sell')
        ct = datetime.now()
        if WaitForTarget(10000):
            WaitTargetObject(bott)
            WaitJournal('Your sale total is', ct)
    CheckPos(0)


def TradeGold():
    if IsTrade():
        for i in range(TradeCount()):
            if GetTradeOpponent(i) == TRADER:
                tradeID, tradeNum = GetTradeContainer(i, 1), i
                break
        FindTypeEx(0x0EED, 0x0000, Backpack(), False)
        if FindCount() <= 0:
            while IsTrade():
                CancelTrade(0)
            return
        if MoveItems(Backpack(), 0x0EED, 0x0000, tradeID, 1, 1, 1, 900):
            while GetTradeOpponent(i) == TRADER:
                if not TradeCheck(tradeNum, 1):
                    ConfirmTrade(tradeNum)
                Wait(100)


def CheckResource():
    FindTypeEx(0x0EED, 0x083B, Backpack(), False)
    if FindFullQuantity() >= MAX_SAND_COUNT_PROCESSED:
        return True
    return False


def main():
    CheckConnect()
    startCoor = GetLocInfoChar()
    xS = startCoor.get('x') - RADIUS_D
    xF = startCoor.get('x') + RADIUS_D
    yS = startCoor.get('y') - RADIUS_D
    yF = startCoor.get('y') + RADIUS_D
    while True:
        for _x in range(xS, xF):
            Hungry()
            for _y in range(yS, yF):
                CheckConnect()
                CheckDead()
                if CheckResource():
                    CheckConnect()
                    Sand()
                    if bottle := CreateBottle():
                        Sell(bottle)
                tool = CheckTool()
                if not tool and not Dead():
                    return print("not found tools")
                TradeGold()
                while not Mining_Sand(tool, 0, _x, _y, GetZ(Self())):
                    Wait(50)
                msgC("swift mining coordinates")


if __name__ == '__main__':
    SetMoveOpenDoor(True)
    SetMoveCheckStamina(0)
    SetMoveThroughNPC(0)
    main()
