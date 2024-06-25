from py_stealth import *
from datetime import datetime

# version 2 by nepret

# Летаем по рунам и стрижем овечек, в паке иметь ножници, еду, рунбуку с рунами
# в настройках ниже указать руны, id рунбуки, перерабатывать ли шерсть в ткань,
# если да то указать контейнер куда ткань скидывать

# На землю возле тп в доме в радиусе 2 клеток, оставить пачку реколов
# и если перерабатываем шерсть в ткань, то там же ставим прялку, веретено и пак куда скидывать ткань


RUNES = ['dom1', 'dom2', 'dom3', 'DomProcessed']  # руны по которым летать
# можно указать по порядку цифрами [1, 2, 3, 10], или название рун в рунбуке (с учётом регистра)
# последняя руна ВСЕГДА руна в дом, в радиусе 2 клеток от точки рекала в доме оставить пачку реколов

ID_RUNEBOOK = 0x40C3E45F  # ID рунбуки

PROCESSED = True  # True перерабатывать шерсть после обхода овец, False нет
ID_CONT = 0x44B5277D  # ID контейнера куда кидаем рулоны


#############################################################################
# создаём объект c параметром ID рунбуки и в объекте выбираем нужную функцию
# _runebook = RecallRunebook(0x40C32345)
# _runebook.gate()
# в параметрах функции, указываем или номер руны, или название руны
# _runebook.recall_on_scroll('Dom'), _runebook.recall_on_reagents(1)


class RecallRunebook:
    def __init__(self, id_runebook):
        self._id_runebook = id_runebook
        self._runeInfo = []
        self._chargeMax = None
        self._charge = None

    @staticmethod
    def _check_pos(ct):
        x, y, z = GetX(Self()), GetY(Self()), GetZ(Self())
        for i in range(150):
            if x != GetX(Self()) or y != GetY(Self()) or z != GetZ(Self()):
                return True
            if InJournalBetweenTimes("You have lost your concentration!|"
                                     "You can't recall to a non-friend house.|"
                                     "You are not skilled enough to cast this spell.|"
                                     "You lack reagent", ct, datetime.now()) != -1:
                break
            Wait(100)
        return False

    @property
    def get_charge(self):
        self._check_runebook()
        self._get_info_gump()
        for i in range(GetGumpsCount() - 1):
            if IsGump():
                CloseSimpleGump(i)
        return self._charge

    @property
    def get_max_charge(self):
        if self._chargeMax is None:
            self._check_runebook()
            self._get_info_gump()
        return self._chargeMax

    def set_def(self, rune):
        if self._check_runebook() and self._get_info_gump():
            if gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump['def'])

    def recall_on_scroll(self, rune):
        if self._check_runebook() and self._get_info_gump():
            if self._charge <= 0:
                print('There are no scrolls in the runebook')
            elif gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump['scroll'])
                if self._check_pos(datetime.now()):
                    return True
        return False

    def recall_on_reagents(self, rune):
        if self._check_runebook() and self._get_info_gump():
            if any(i < 1 for i in [BPCount(), MRCount(), BMCount()]):
                print(f'Not enough reagents (BP:{BPCount()}, MR:{MRCount()}, BM:{BMCount()})')
            elif Mana() < 11:
                print(f"Not enough mana! <11 ({Mana()}/{MaxMana()})")
            elif gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump['reg'])
                if self._check_pos(datetime.now()):
                    return True
            return False

    def gate(self, rune):
        if self._check_runebook() and self._get_info_gump():
            if any(i < 1 for i in [BPCount(), MRCount(), SACount()]):
                print(f'Not enough reagents (BP:{BPCount()}, MR:{MRCount()}, SA:{SACount()})')
            elif Mana() < 40:
                print(f"Not enough mana! <40 ({Mana()}/{MaxMana()})")
            elif gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump['gate'])
                old_dist = GetFindDistance()
                SetFindDistance(1)
                if FindType(0x0F6C, Ground()):
                    for i in GetFindedList():
                        Ignore(i)
                ct = datetime.now()
                for i in range(150):
                    if InJournalBetweenTimes("Spell Fizzled.", ct, datetime.now()) != -1:
                        break
                    if FindType(0x0F6C, Ground()):
                        SetFindDistance(old_dist)
                        IgnoreReset()
                        return True
                    Wait(100)
                IgnoreReset()
                SetFindDistance(old_dist)
        return False

    def drop_rune(self, rune):
        if self._check_runebook() and self._get_info_gump():
            if gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump['drop'])

    def _check_rune(self, rune):
        if isinstance(rune, int):
            if len(self._runeInfo) >= rune > 0:
                return self._runeInfo[rune - 1]
            print(f"Error index rune! ({rune})")
        else:
            for _runeInfo in self._runeInfo:
                if _runeInfo.get('name') in rune:
                    return _runeInfo
            print(f"Error name rune, this name rune not exist! ({rune})")
        return False

    def _check_runebook(self):
        # открываекм рунбуку
        if not Dead():
            if LastContainer() != Backpack():
                UseObject(Backpack())
                CheckLag(1000)
                Wait(1000)
            if IsObjectExists(self._id_runebook):
                for i in range(GetGumpsCount()):
                    CloseSimpleGump(i)
                g = GetGumpsCount()
                UseObject(self._id_runebook)
                for i in range(100):
                    if GetGumpsCount() > g:
                        return True
                    Wait(100)
                print(f"I can not open the runebook (id:{hex(self._id_runebook)})")
            else:
                print(f"Runebook not founded (id:{hex(self._id_runebook)})")
        return False

    def _get_info_gump(self):
        gumps = GetGumpInfo(GetGumpsCount() - 1)

        # смотрим кол-во рун в рунбуку
        if len(gumps['Text']) <= 3:
            print('Runebook empty!')
            return False

        # запоминаем сколько осталось зарядов и сколько зарядов вмещает
        self._charge = gumps['Text'][0][0].split(':')
        self._charge = int(self._charge[len(self._charge) - 1].strip())

        self._chargeMax = gumps['Text'][1][0].split(':')
        self._chargeMax = int(self._chargeMax[len(self._chargeMax) - 1].strip())

        # создаём и заполняем лист именами рун
        self._runeInfo.clear()
        for g in range(3, len(gumps['Text'])):
            if gumps['Text'][g][0] in 'Set default':
                break
            self._runeInfo.append({'name': gumps['Text'][g][0]})

        # ищем первый гамп, от него будем записывать последующие
        gump = 0
        for i in range(len(gumps['GumpButtons'])):
            if gumps['GumpButtons'][i]['ReturnValue'] > 0:
                gump = gumps['GumpButtons'][i]['ReturnValue']
                break

        if gump == 0:
            return False

        # сначало scroll, так как эти гампы идут самыми первыми по порядку
        for s, i in zip(range(gump, gump + len(self._runeInfo)), range(len(self._runeInfo))):
            self._runeInfo[i]['scroll'] = s
            gump += 1

        # потом остальное
        for i in range(len(self._runeInfo)):
            for d in ['def', 'drop', 'reg', 'gate']:
                self._runeInfo[i][d] = gump
                gump += 1
        return True


def check_scissors():
    if FindType(0x0F9E, Backpack()):
        return True
    print("not found scissors in backpack!")
    return False


def wool_processed():
    print('wool_processed start')
    if FindType(0x0DF8, Backpack()):
        if FindQuantity() >= 5:
            ct = datetime.now()
            UseObject(FindItem())
            while InJournalBetweenTimes('You stop.', ct, datetime.now()) == -1:
                Wait(1000)

    if FindType(0x0E1D, Backpack()):
        if FindQuantity() >= 5:
            ct = datetime.now()
            UseObject(FindItem())
            while InJournalBetweenTimes('You stop.', ct, datetime.now()) == -1:
                Wait(1000)

    if FindType(0x0F95, Backpack()):
        if IsObjectExists(ID_CONT):
            MoveItem(FindItem(), GetQuantity(FindItem()), ID_CONT, 0, 0, 0)
        else:
            DropHere(FindItem())
        Wait(2000)
    print('wool_processed finish')


def use_sheep(place):
    print(f'use_sheep start: {place}')
    while sheep := FindType(0x00CF, Ground()):
        if TargetPresent():
            CancelTarget()
        ct = datetime.now()
        UseType(0x0F9E, 0xFFFF)
        if WaitForTarget(10000):
            WaitTargetObject(sheep)
        WaitJournalLineSystem(ct, "Failed.|Success.|That is too far away."
                                  "|You stop shearing.|You have found a black pearl!", 10000)
        if InJournalBetweenTimes("That is too far away.", ct, datetime.now()) != -1:
            Ignore(sheep)
    print('use_sheep finish')


def recharge():
    max_charge = _rb.get_max_charge
    charge = _rb.get_charge
    if FindType(0x1F4C, 0x0000):
        if FindQuantity() > max_charge:
            if MoveItem(FindItem(), max_charge - charge, ID_RUNEBOOK, 0, 0, 1):
                Wait(5000)
                return True
            else:
                print('recharge processed ERROR')
        else:
            print('not need count recall scrolls')
    else:
        print('not found recall scrolls')
    return False


def check_autoloop_settings():
    while IsGump():
        CloseSimpleGump(GetGumpsCount() - 1)
    UOSay('.options')
    while not IsGump():
        Wait(100)
    else:
        NumGumpCheckBox(GetGumpsCount()-1, 1540, 1)
        NumGumpButton(GetGumpsCount() - 1, 1029)


def main():
    check_autoloop_settings()
    while not Dead():
        if not check_scissors():
            break
        for i in range(len(RUNES) - 1):
            newMoveXY(GetX(Self())+1, GetY(Self()), True, 0, False)
            _rb.recall_on_scroll(RUNES[i])
            Wait(5000)
            use_sheep(RUNES[i])
        if PROCESSED:
            _rb.recall_on_scroll(RUNES[len(RUNES)-1])
            Wait(5000)
            wool_processed()
        if not recharge():
            break
        print('Wait restart wool to sheeps')
        Wait(10*60*1000)


if __name__ == '__main__':
    SetFindDistance(3)
    SetFindVertical(20)
    SetARStatus(True)
    if not Connected():
        Wait(10000)
    SetPauseScriptOnDisconnectStatus(True)
    _rb = RecallRunebook(ID_RUNEBOOK)
    main()
    SetARStatus(False)
    SetPauseScriptOnDisconnectStatus(False)
    print("End!")
    Disconnect()
