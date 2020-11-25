from py_stealth import Backpack, LastContainer, UseObject, Wait
from Scripts.Python.Include.checksave import CheckSave
from Scripts.Python.Include.checkdcc import DCC


def OpenPack(Container=Backpack()):
    while LastContainer() != Container:
        if DCC(OpenPack):
            break
        CheckSave()
        UseObject(Container)
        end = 0
        while end >= 5:
            if LastContainer() == Backpack():
                break
            Wait(1000)
            end += 1
