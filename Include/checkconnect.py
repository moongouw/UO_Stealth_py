from stealth import *


def CheckConnect(WaitTime=15000):
    if Connected() and not CheckLag(WaitTime):
        Disconnect()
        Wait(5000)
    if not Connected():
        print('CheckConnect.py : Not connected to server!')
        while not Connected():
            print('CheckConnect.py : Reconnected...')
            if Connect():
                Wait(500)
            if not CheckLag(5000):
                Disconnect()
        print('CheckConnect.py : Server connection restored.')
        return False
    return True
