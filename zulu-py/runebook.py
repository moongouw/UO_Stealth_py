from py_stealth import *
from datetime import datetime 

class RecallRunebook:
    def __init__(self, runebook):
        self._id_runebook = runebook
        self._runebook_info = None
        self._charge = self._chargeMax = None

    def _open_runebook(self):
        ClearGumpsIgnore()
        while IsGump():
            CloseSimpleGump(GetGumpsCount()-1)
            Wait(1000)
        CheckLag(10000)
        while not IsGump():
            UseObject(self._id_runebook)
            for i in range(50):
                if IsGump():
                    return True
                Wait(100)
        return False

    def _get_info_gump(self):
        if not self._open_runebook():
            return False
        gump_info = GetGumpInfo(GetGumpsCount()-1)
        result = []
        if len(gump_info):

            # смотрим кол-во рун в рунбуку
            if len(gump_info.get('Text')) <= 3:
                print('Runebook empty!')
                return False

            # запоминаем сколько осталось зарядов и сколько зарядов вмещает
            _charge = gump_info.get('Text')[0][0].split(':')
            self._charge = int(_charge[len(_charge) - 1].strip())

            _chargeMax = gump_info.get('Text')[1][0].split(':')
            self._chargeMax = int(_chargeMax[len(_chargeMax) - 1].strip())

            # создаём и заполняем лист именами рун
            for g in range(3, len(gump_info.get('Text'))):
                if gump_info.get('Text')[g][0] in 'Set default':
                    break
                result.append({'name': gump_info.get('Text')[g][0]})

            # ищем первый гамп, от него будем записывать последующие
            gump = 0
            for i in range(len(gump_info.get('GumpButtons'))):
                if gump_info.get('GumpButtons')[i].get('ReturnValue') > 0:
                    gump = gump_info.get('GumpButtons')[i].get('ReturnValue')
                    break
            if gump == 0:
                return False

            # сначало scroll, так как эти гампы идут самыми первыми по порядку
            for s, i in zip(range(gump, gump + len(result)), range(len(result))):
                result[i].update({'scroll': s})
                gump += 1

            # потом остальное
            for i in range(len(result)):
                for d in ['def', 'drop', 'reg', 'gate']:
                    result[i].update({d: gump})
                    gump += 1
            self._runebook_info = result
            return True

    @staticmethod
    def _check_pos():
        st = datetime.now()
        x, y, z = GetX(Self()), GetY(Self()), GetZ(Self())
        for i in range(150):
            if x != GetX(Self()) or y != GetY(Self()) or z != GetZ(Self()):
                return True
            if InJournalBetweenTimes("You have lost your concentration!|"
                                     "You can't recall to a non-friend house.|"
                                     "You are not skilled enough to cast this spell.|"
                                     "You lack reagent", st, datetime.now()) != -1:
                break
            Wait(100)
        return False

    @property
    def get_charge(self):
        if self._get_info_gump():
            for i in range(GetGumpsCount() - 1):
                if IsGump():
                    CloseSimpleGump(i)
            return self._charge
        return False

    @property
    def get_max_charge(self):
        if self._get_info_gump():
            for i in range(GetGumpsCount() - 1):
                if IsGump():
                    CloseSimpleGump(i)
            return self._chargeMax
        return False

    def set_def(self, rune):
        if self._get_info_gump():
            if gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump.get('def'))

    def recall_on_scroll(self, rune):
        if self._get_info_gump():
            if self._charge <= 0:
                print('There are no scrolls in the runebook')
            elif gump := self._check_rune(rune):
                newMoveXY(GetX(Self())+1, GetY(Self()), True, 0, True)
                NumGumpButton(GetGumpsCount() - 1, gump.get('scroll'))
                if self._check_pos():
                    return True
        return False

    def recall_on_reagents(self, rune):
        if self._get_info_gump():
            if any(i < 1 for i in [BPCount(), MRCount(), BMCount()]):
                print(f'Not enough reagents (BP:{BPCount()}, MR:{MRCount()}, BM:{BMCount()})')
            elif Mana() < 11:
                print(f"Not enough mana! <11 ({Mana()}/{MaxMana()})")
            elif gump := self._check_rune(rune):
                newMoveXY(GetX(Self()) + 1, GetY(Self()), True, 0, True)
                NumGumpButton(GetGumpsCount() - 1, gump.get('reg'))
                if self._check_pos():
                    return True
            return False

    def gate(self, rune):
        if self._get_info_gump():
            if any(i < 1 for i in [BPCount(), MRCount(), SACount()]):
                print(f'Not enough reagents (BP:{BPCount()}, MR:{MRCount()}, SA:{SACount()})')
            elif Mana() < 40:
                print(f"Not enough mana! <40 ({Mana()}/{MaxMana()})")
            elif gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump.get('gate'))
                old_dist = GetFindDistance()
                SetFindDistance(1)
                if FindType(0x0F6C, Ground()):
                    for i in GetFindedList():
                        Ignore(i)
                st = datetime.now()
                for i in range(150):
                    if InJournalBetweenTimes("Spell Fizzled.", st, datetime.now()) != -1:
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
        if self._get_info_gump():
            if gump := self._check_rune(rune):
                NumGumpButton(GetGumpsCount() - 1, gump.get('drop'))

    def _check_rune(self, rune):
        if isinstance(rune, int):
            if len(self._runebook_info) >= rune > 0:
                return self._runebook_info[rune-1]
            print(f"Error index rune! ({rune})")
        else:
            for _runeInfo in self._runebook_info:
                if _runeInfo.get('name') in rune:
                    return _runeInfo
            print(f"Error name rune, this name rune not exist! ({rune})")
        return False
