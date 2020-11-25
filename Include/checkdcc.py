from py_stealth import Dead, Connected, CheckLag


# message - enter name out function
def DCC(message, TimeWait=15000):
    if Dead() or not Connected() or not CheckLag(TimeWait):
        print(f"{message}: You dead, or something else!")
        return False
    return True
