from py_stealth import *
from Scripts.Python.Include.all import *
from datetime import datetime
from Scripts.Python.mining.mining_Sand.Mover import MoveIn


def Mining(pickaxe, tile=0, x=0, y=0, z=GetZ(Self())):
    waitMiningMsg = "That is too far away.|"\
                    "You can't mine or dig anything there.|"\
                    "You stop mining."
    finishMiningMsg = "That is too far away.|" \
                      "You can't mine or dig anything there.|" \
                      "There's no sand left there."
    if not pickaxe:
        return False
    if TargetPresent():
        CancelTarget()
    if MenuPresent():
        CancelMenu()
    if not CheckConnect() or Dead() or not CheckLag(15000):
        return False
    MoveIn("locMagincia")
    if Dist(x, y, GetX(Self()), GetY(Self())) > 2:
        if not NewMoveXY(x, y, True, 21, True):
            msg(f"can't not moving out х{GetX(Self())} y{GetY(Self())} in x{x} y{y}")
            return False
    ct = datetime.now()
    msg("mining")
    while not TargetPresent() and Connected() and not Dead():
        UseObject(pickaxe)
        if WaitForTarget(10000):
            break
    TargetToTile(tile, x, y, z)
    if WaitJournal(waitMiningMsg, ct, 30):
        return WaitJournal(finishMiningMsg, ct, 0)
    return False
