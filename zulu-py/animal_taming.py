from py_stealth import *
from datetime import datetime, timedelta

# все type и ID пишутся не через $, а через 0x!!!
# не так: $00E1, $0003939B
# а вот так: 0x00E1, 0x0003939B


# Info
# Что делает скрипт:
# Ищет животных вокруг себя, если есть не приручённые, пытается затамить.
# Если затамить не получилось с 3-го раза, ставит данную тварь на ожидание и пытается тамить через 5 минут.
# Сворачивает всех прирученных тварюг в диды.
# Разворачивает 1 дид и даёт команду all release


# !!! FAQ !!!
# Заранее приручаем штук 8 животных и сворачиваем их в дид у вендора (команда: stable).
# В пак закидываем еду и деньги, много денег, что бы хватило.
# Желательно поставить чара в комнате с вендором так, чтобы животные не могли уйти дальше 4 тайлов от чара .
# Это связано с тем, что если вдруг чар не сможет затамить животину с 3-го раза, скрипт будет тамить эту животину только
# через 5 минут, а за это время, тварюга может уйти пешкодралом аж до брита.
# Не забудьте вбить свои данные в настройках нижу
# Таблица животных: http://play.zuluhotel.com/tab/tabl34.do?npcgpoup=animal

ANIMAL_TYPE = 0x00E1  # type животинки, на которой качаемся
MAX_SKILL = 50  # потолок скилла до которого качаемся
ID_NPC = 0x0003939B  # ID вендора
MIN_GOLD = 100  # минимальное количество золота, если меньше, то выходим


class ProcessedAnimals:
    def __init__(self):
        self.animals = {}

    def __call__(self):
        self.__get_animals()
        self.__taming_animal()
        if not self.__stable_animals():
            return False
        return True

    # ищем и заносим в список зверей вокруг
    def __get_animals(self):
        FindType(ANIMAL_TYPE, Ground())
        if GetFindedList():
            for i in GetFindedList():
                RequestStats(i)
                CheckLag(10000)
                # прирученных заносим как True
                if MobileCanBeRenamed(i):
                    self.animals.update({i: True})
                # не прирученных заносим с временем
                if self.animals.get(i) is None:
                    self.animals.update({i: datetime.now()})

    # сворачиваем зверей вы дид у вендора
    def __stable_animals(self):
        for animal in self.animals.copy():
            FindTypeEx(0x0EED, 0x0000, Backpack(), True)
            if FindFullQuantity() < MIN_GOLD:
                print(f"Not Gold!({Gold()})")
                return False
            if self.animals[animal] is True:
                if not check_npc():
                    return False
                if TargetPresent():
                    CancelTarget()
                CheckLag(10000)
                UOSay("stable")
                if WaitForTarget(10000):
                    WaitTargetObject(animal)
                    CheckLag(10000)
                    Wait(1000)
                self.animals.pop(animal)
        return True

    # тамим зверей из списка
    def __taming_animal(self):
        for animals in self.animals.copy():
            # приручаем только в том случае, если время у животного меньше настоящего
            if isinstance(self.animals[animals], datetime) and self.animals[animals] <= datetime.now():
                if not IsObjectExists(animals) or GetDistance(animals) > 4:
                    self.animals.pop(animals)
                    continue
                while True:
                    if TargetPresent():
                        CancelTarget()
                    UseSkill('Animal Taming')
                    ct = datetime.now()
                    if WaitForTarget(10000):
                        WaitTargetObject(animals)
                        WaitJournalLineSystem(ct, "You successfully|That creature looks|You failed to tame", 11000)
                        CheckLag(10000)
                        Wait(1000)
                        # если зверь уже приручен или приручение удалось, заносим в список как True и выходим из цикла
                        if 1 >= FoundedParamID() >= 0:
                            self.animals[animals] = True
                            break
                        # если после неудачной попытки появился имунитет к тамингу (3-я попятка failed)
                        # выходим из цикла и обновляем в списке таймер на 5 минут
                        elif FoundedParamID() > 1:
                            Wait(2000)
                            if InJournalBetweenTimes("And have made", ct, datetime.now()) != -1:
                                self.animals[animals] = datetime.now()+timedelta(minutes=5)
                                break


def check_npc():
    if IsObjectExists(ID_NPC):
        if GetDistance(ID_NPC) > 1:
            print(f"distance NPC {GetName(ID_NPC)} > 1 (dist: {GetDistance(ID_NPC)})")
            return False
    else:
        print(f"NPC({ID_NPC}) not exists!")
        return False
    return True


def unstable_and_released():
    if not check_npc():
        return False
    IgnoreReset()
    if did := FindType(0x14F0, Backpack()):
        ct = datetime.now()
        # добавлякем в игнор всех животных нужного типа
        FindType(ANIMAL_TYPE, Ground())
        for i in GetFindedList():
            Ignore(i)

        MoveItem(did, 1, ID_NPC, 0, 0, 0)
        CheckLag(10000)
        if WaitJournalLine(ct, "Take care and be sure to feed it!", 10000):
            for i in range(5):
                if FindType(ANIMAL_TYPE, Ground()):
                    break
                Wait(1000)
        UOSay("all release")
        for i in range(5):
            RequestStats(FindItem())
            if not MobileCanBeRenamed(FindItem()):
                IgnoreReset()
                break
            Wait(1000)
    Wait(2000)
    return True


if __name__ == '__main__':
    SetFindDistance(4)
    if not GetARStatus():
        SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(True)
    CheckLag(10000)
    _proc_anim = ProcessedAnimals()
    while GetSkillValue('Animal Taming') < MAX_SKILL:
        if not _proc_anim():
            break
        if not unstable_and_released():
            break
        Wait(500)
    print("End!")
    SetPauseScriptOnDisconnectStatus(False)
    if GetARStatus():
        SetARStatus(False)
    Disconnect()
