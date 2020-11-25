from datetime import datetime
from stealth import *


def Hungry(food=0x097B):  # food default "fish steaks", search in you backpack
    while True:
        if Dead() or not Connected() or not CheckLag(15000):
            print("Hungry: You dead, or not connected or hard lags!")
            return False
        FindType(food, Backpack())
        if FindCount() <= 0:
            print("Hungry: not food!")
            return
        ct = datetime.now()
        UOSay(".hungry")
        if not WaitJournalLine(ct, 'stuffed', 5000):
            UseObject(FindItem())
            Wait(1500)
        else:
            return True
