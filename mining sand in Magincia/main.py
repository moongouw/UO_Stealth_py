from Scripts.Python.Include.all import Hungry
from Scripts.Python.mining.mining_Sand.GetInfoLocChar import GetLocInfoChar
from Scripts.Python.mining.mining_Sand.Mover import *
from Scripts.Python.mining.mining_Sand.MiningSand import Mining
from Scripts.Python.mining.mining_Sand.CheckResource import CheckResource

# The name of the file into which the coordinates are written.
# Имя файла в который записываются координаты.
LOC_FILE = 'coordinates_Magincia'

# Digging radius from coordinates
# Радиус обпкопки тайлов
RADIUS_D = 3

# Type you tool, now the pick
# Тип кирки
TOOL_TYPE = 0x0E85

# At what amount of sand in the bank to start the melting and sale procedure
# При каком количестве песка в банке начинать процедуру переплавки, крафта и продажи
MAX_SAND_COUNT_PROCESSED = 50000

# How much sand to carry to the bank
# Сколько песка таскать в банк
MAX_SAND_COUNT_MINING = 350

# How long to wait (per second) after death to resurrect
# Сколько ждать (в секунда) после смерти что бы реснуться
WAIT_TO_RES = 120


def main(_x, _y):
    while True:
        for x in range(_x - RADIUS_D, _x + RADIUS_D):
            for y in range(_y - RADIUS_D, _y + RADIUS_D):
                CheckConnect()
                CheckSave()
                CheckDead(120)
                if cr := CheckResource(MAX_SAND_COUNT_MINING, MAX_SAND_COUNT_PROCESSED, TOOL_TYPE):
                    while not Dead() and not Mining(cr, 0, x, y):
                        Hungry()
                    if not Dead():
                        msg("switch tile")
                else:
                    return False


if __name__ == '__main__':
    SetMoveOpenDoor(True)
    SetMoveCheckStamina(0)
    SetMoveThroughNPC(0)
    SetFindDistance(18)
    CheckConnect()
    CheckDead()
    _x, _y = GetLocInfoChar(LOC_FILE + '.csv', RADIUS_D)
    main(_x, _y)
    msg("End!")
    Disconnect()
    
