from stealth import *
from Scripts.Python.Include.all import CheckSave
from Scripts.Python.Include.checkdcc import DCC


# FT=TypeItem, FC=ColorItem, FQ=Maximal count in stack
def StuckB(FT=0xFFFF, FC=0xFFFF, FQ=60000):
    if not DCC('StuckB'):
        return
    IgnoreReset()
    FindTypeEx(FT, FC, Backpack(), False)
    findList = GetFindedList()
    for _itemID in findList:
        if GetQuantity(_itemID) >= FQ:
            Ignore(_itemID)
    findList.clear()

    while itemID := FindTypeEx(FT, FC, Backpack(), False):
        if FindCount() <= 1:
            break
        findList = GetFindedList()
        for _itemID in findList:
            if GetQuantity(itemID) >= FQ:
                Ignore(itemID)
                break
            if _itemID != itemID:
                if not DCC('StuckB.py'):
                    return
                if TargetPresent():
                    CancelTarget()
                CheckSave()
                MoveItem(_itemID, FQ - GetQuantity(itemID), itemID, 0, 0, 0)
                Wait(1000)
