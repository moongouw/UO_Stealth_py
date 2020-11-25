from datetime import *
from py_stealth import InJournalBetweenTimes, Connected, Wait
from Scripts.Python.Include.checksave import CheckSave


def WaitJournal(msgWait, startTime, errorWaitTimeSec=15):
    t = 0
    while (InJournalBetweenTimes(msgWait, startTime, datetime.now()) == -1) and (errorWaitTimeSec * 20 >= t):
        if not Connected():
            print('WaitJournal.py: ERROR! not connected to server!')
            return False
        CheckSave()
        t += 1
        Wait(50)
    if (t >= errorWaitTimeSec * 20) and (t > 0):
        return False
    return True
