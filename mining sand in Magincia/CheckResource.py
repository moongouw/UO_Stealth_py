from datetime import datetime
from py_stealth import *
from Scripts.Python.Include.all import msg, CheckConnect, CheckSave, WaitJournal, Hungry
from Scripts.Python.mining.mining_Sand.Mover import GoToBank, MoveIn
from Scripts.Python.mining.mining_Sand.Checker import FindVendor


def CheckResource(sandQuantityMax, sandQuantityProcessed, typePickAxe=0x0E85, tool=0x1EBC, food=0x097B):
    CheckConnect(), CheckSave(), CheckLag()
    if Dead():
        return False
    # check count pickaxe
    pickAxe = None
    layer = (RhandLayer(), LhandLayer())
    for i in layer:
        if GetType(ObjAtLayer(i)) == typePickAxe:
            pickAxe = ObjAtLayer(i)
    if not pickAxe:
        if FindType(typePickAxe, Backpack()):
            pickAxe = FindItem()
    toolID = FindItem() if FindType(tool, Backpack()) else False
    # check quantity sand
    sand = FindTypeEx(0x0EED, 0x083B, Backpack(), False)
    if FindCount() <= 0 or sandQuantityMax > FindQuantity():
        sand = None
    # check ingots quantity >= 20
    ingots, bottle = False, False
    if FindType(0x1BF5, Backpack()):
        if FindFullQuantity() >= 20:
            ingots = FindItem()
    # check count bottle
    if FindType(0x0F0E, Backpack()):
        bottle = FindItem()
    # go to bank for drop sand or give pickaxe
    if not pickAxe or sand or toolID or bottle or ingots:
        bankID = GoToBank()
        # drop sand
        CheckSave()
        if sand:
            msg("drop sand")
            if sandBank := FindTypeEx(0x0EED, 0x083B, bankID, False):
                MoveItem(sand, GetQuantity(sand), sandBank, 0, 0, 0)
            else:
                MoveItem(sand, GetQuantity(sand), bankID, 0, 0, 0)
            Wait(1000)
        # find and get pickaxe
        if not CheckConnect():
            bankID = GoToBank()
        CheckSave()
        if not pickAxe:
            msg("find and get pickaxe")
            if pickAxe := FindType(typePickAxe, bankID):
                Grab(pickAxe, 1)
                Wait(1000)
            else:
                msg("... not found PickAxe in bank!!! Check this!!!")
                return 0
        # find and get food
        if not CheckConnect():
            bankID = GoToBank()
        CheckSave()
        FindType(food, Backpack())
        if FindQuantity() < 20:
            msg("find and get food")
            backpackFoodQuantity = FindQuantity()
            if bankFood := FindType(food, bankID):
                Grab(bankFood, 20 - backpackFoodQuantity)
        # check quantity sand in back, if quantity >= MAX_SAND_COUNT_PROCESSED
        # go to processed sand
        if not CheckConnect():
            bankID = GoToBank()
        CheckSave()
        FindTypeEx(0x0EED, 0x083B, bankID, False)
        if FindQuantity() >= sandQuantityProcessed or bottle or ingots:
            msg("go to processed sand")
            FindType(tool, bankID)
            if FindCount() or toolID:
                ProcessedSand(tool, toolID)
            else:
                msg("....i not found TinkerTools :|!")
                msg("....checked this!!!")
        elif toolID:
            MoveItem(toolID, 1, bankID, 0, 0, 0)
    return pickAxe


def ProcessedSand(tool, toolID):
    # Go in Newbies to bank and get sand, tinker tool
    MoveIn('locNewbies')
    bankID = GoToBank()
    item = [[0x0EED, 0x083B], [tool, 0xFFFF]]
    for i in item:
        if not CheckConnect():
            bankID = GoToBank()
        if not toolID:
            if itemBank := FindTypeEx(i[0], i[1], bankID, False):
                CheckSave()
                Grab(itemBank, GetQuantity(itemBank))
                Wait(1000)
            else:
                return
    # processed sand
    Sand()
    # processed create bottle
    if bottle := CreateBottle():
        # sell bottle to vendor
        Sell(bottle)
    # Drop gold and tool in bank
    DropGoldAndTool(tool)
    # Goto locMagincia
    MoveIn("locMagincia")


def DropGoldAndTool(tool):
    CheckConnect()
    if Dead():
        return
    # find gold, bottle, tinker tool and move to bank
    item = [0x0EED, 0x0F0E, tool]
    bankID = GoToBank()
    for i in item:
        if not CheckConnect():
            bankID = GoToBank()
        while itemID := FindType(i, Backpack()):
            CheckSave(), CheckLag()
            MoveItem(itemID, FindQuantity(), bankID, 1, 1, 1)
            Wait(500)


def Sand():
    while GetX(Self()) != 4267 or GetY(Self()) != 2889:
        CheckConnect(), CheckSave()
        newMoveXYZ(4267, 2889, 5, 0, 10, True)
    if forge := FindType(0x0FB1, Ground()):
        while GetDistance(forge) > 1:
            CheckConnect(), CheckSave()
            newMoveXYZ(GetX(forge), GetY(forge), GetZ(forge), 1, 0, True)
        while sand := FindTypeEx(0x0EED, 0x083B, Backpack(), False):
            msg(f'Count sand: {FindFullQuantity()}')
            ct = datetime.now()
            if TargetPresent():
                CancelTarget()
            while not TargetPresent():
                CheckConnect(), CheckSave()
                UseObject(sand)
                WaitForTarget(3000)
            TargetToObject(forge)
            WaitJournal('Success.|Failed.', ct)
    else:
        msg("ERROR: can't find a forge!")
        return False
    msg('Sand processing is over!')
    return True


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
            if FindCount() <= 0:
                return
            msg("Craft bottle is finished!")
            msg(f"Total bottles crafted: {FindFullQuantity()}")
            return FindItem()
        msg(f"ing all: {FindFullQuantity()}/{(FindFullQuantity() // 20)}")
        Hungry()
        if TargetPresent():
            CancelTarget()
        UseObject(tool)
        ct = datetime.now()
        if WaitForTarget(5000):
            WaitTargetObject(resource)
        WaitJournal('You stop.|Stop.', ct)


def CheckPos(xyz=1):
    if xyz == 1:
        xyz = {'x': 4264, 'y': 2883}  # in house
        NewMoveXY(4267, 2889, True, 0, True)
    else:
        xyz = {'x': 4267, 'y': 2889}  # out house
    while (GetX(Self()) != xyz['x']) or (GetY(Self()) != xyz['y']):
        newMoveXYZ(xyz['x'], xyz['y'], 1, 0, 100, True)
        Wait(1000)


def Sell(bott):
    CheckConnect(), CheckSave()
    vendorList = FindVendor()
    for vendorID in vendorList:
        x, y, z, vendorID = GetX(vendorID[0]), GetY(vendorID[0]), GetZ(vendorID[0]), vendorID[0]
        msg(f"name vendor: {GetName(vendorID)}")
        while GetDistance(vendorID) > 1:
            newMoveXYZ(x, y, z, 1, 0, True)
            CheckSave()
        for i in range(5):
            UOSay("sell")
            if WaitForTarget(3000):
                ct = datetime.now()
                WaitTargetObject(bott)
                if WaitJournal('Your sale total is', ct):
                    CheckPos(0)
                    return
        msg("hmm... this bad vendor, not sell :(")
        msg("need change vendor...")
