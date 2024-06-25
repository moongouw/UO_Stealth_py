from py_stealth import *
from datetime import datetime

DROP_RECALL = True


def meditation():
    while Mana() < MaxMana():
        ct = datetime.now()
        if TargetPresent():
            CancelTarget()
        UseSkill('Meditation')
        if WaitJournalLine(ct, 'You enter a meditative trance.', 10000):
            while InJournalBetweenTimes('You moved and lost your concetration.|'
                                        'You stop meditating.', ct, datetime.now()) == -1:
                Wait(1000)


def inscription():
    if FindTypeEx(0x0E34, 0x0000, Backpack(), False):
        ct = datetime.now()
        if TargetPresent():
            CancelTarget()
        UseSkill('Inscription')
        if WaitForTarget(10000):
            WaitTargetObject(FindItem())
            if FindTypeEx(0x0EFA, 0x0488, Backpack(), False):
                if WaitForTarget(10000):
                    WaitTargetObject(FindItem())
                if WaitJournalLine(ct, 'Success.|Failed.', 10000):
                    while InJournalBetweenTimes("You don't have enough mana.", ct, datetime.now()) == -1:
                        Wait(1000)
                return True
    else:
        print('not found blank scrolls')
    return False


def drop_recall_scrolls():
    if s := FindTypeEx(0x1F4C, 0x0000, Backpack(), False):
        if FindTypeEx(0x1F4C, 0x0000, Ground(), False):
            MoveItem(s, GetQuantity(s), FindItem(), 0, 0, 0)
            Wait(2000)
        else:
            DropHere(s)
            

def check_autoloop_settings():
    while IsGump():
        CloseSimpleGump(GetGumpsCount() - 1)
    UOSay('.options')
    while not IsGump():
        Wait(100)
    else:
        NumGumpCheckBox(GetGumpsCount()-1, 1540, 1)
        NumGumpButton(GetGumpsCount() - 1, 1029)


def main():
    check_autoloop_settings()
    AutoMenu('Select', 'Circle 4 spells')
    AutoMenu('Select', 'Recall')
    while True:
        meditation()
        if DROP_RECALL:
            drop_recall_scrolls()
        if not inscription():
            break


if __name__ == '__main__':
    SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(True)
    SetFindDistance(2)
    main()
    SetARStatus(False)
    SetPauseScriptOnDisconnectStatus(False)
    print("End!")
    Disconnect()
