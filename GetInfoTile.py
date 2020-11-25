from py_stealth import *


def CheckTile(x, y,):
    tile = ReadStaticsXY(x, y, WorldNum())
    if len(tile) > 0:
        _t = 0
        for _i in tile:
            msg(f"{t}#{_t} Tile: {_i.get('Tile')}, Z: {_i.get('Z')}")
            _t += 1
    else:
        msg("Тайл пуст...")
    msg('------------------')


def WaitTarget():
    if TargetPresent():
        CancelTarget()
    msg('Кликните на тайл')
    ClientRequestObjectTarget()
    while not ClientTargetResponsePresent():
        Wait(50)
    if LastTarget() == Self():
        return 0
    x = ClientTargetResponse()
    return x


def msg(Message):
    print(Message)
    ClientPrintEx(0, 60, 2, Message)


if __name__ == '__main__':
    t = 0
    while i := WaitTarget():
        t += 1
        CheckTile(i.get('X'), i.get('Y'))
    msg('END')
