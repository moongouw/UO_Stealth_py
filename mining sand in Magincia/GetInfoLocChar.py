import csv
import os
from py_stealth import *
from Scripts.Python.Include.all import msg, CheckSave, CheckConnect
from Scripts.Python.mining.mining_Sand.Mover import MoveIn


def WaitTargetOnSelf(radius):
    if TargetPresent():
        CancelTarget()
    msg(f'...stand on the tile around which we will dig (radius: {radius})...')
    msg('...point to yourself to write the coordinates of the tile...')
    ClientRequestObjectTarget()
    while not ClientTargetResponsePresent():
        Wait(50)
    if LastTarget() == Self():
        return ClientTargetResponse()
    else:
        msg('... you missed, try again ...')
        return False


def LocFileRecord(file, locFile, radius):
    CheckConnect()
    msg('...moving in to beach Magincia for recording coordinates...')
    MoveIn('locMagincia')
    while not NewMoveXY(3716, 2043, True, 0, True):
        CheckConnect()
        CheckSave()
        Wait(50)
    t = False
    while not t:
        t = WaitTargetOnSelf(radius)
        Wait(50)
    with open(file, 'a') as file:
        csv.writer(file).writerow([CharName(), Self(), t['X'], t['Y']])
    msg('...coordinates received and written to file...')
    msg(locFile)
    return {'x': t['X'], 'y': t['Y']}


def LocFileCreate(locFile):
    msg(f'...file {locFile} not found...')
    workFile = os.path.join(os.path.dirname(__file__), locFile)
    with open(workFile, 'a'):
        msg(f"...file {locFile} is created...")
        msg(f"path new file: {workFile}")
        return workFile


def LocFileRecordSearch(file):
    CheckConnect()
    with open(file) as f:
        for line in csv.reader(f):
            if (len(line) == 4) and (int(line[1]) == Self()):
                return {'x': int(line[2]), 'y': int(line[3])}
    return False


def LocFileSearch(locFile):
    find_dir = os.path.join(os.path.dirname(__file__))
    found_file = os.listdir(find_dir)
    for _i in found_file:
        if _i in locFile:
            return os.path.join(os.path.dirname(__file__), locFile)


def GetLocInfoChar(locFile, radius):
    file = LocFileSearch(locFile)
    _return = False
    if not file:
        file = LocFileCreate(locFile)
    else:
        _return = LocFileRecordSearch(file)
    if not _return:
        _return = LocFileRecord(file, locFile, radius)
    return _return['x'], _return['y']
