from py_stealth import CheckLag
from Scripts.Python.Include.all import CheckSave, CheckConnect


def CheckAll(WaitTimeCheckLag=15000):
    CheckConnect()
    CheckSave()
    CheckLag(WaitTimeCheckLag)
