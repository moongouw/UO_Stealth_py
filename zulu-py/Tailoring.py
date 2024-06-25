from py_stealth import *
from datetime import datetime


# Скрипт для прокачки Tailoring от 33 до 150
# * !!! Включаем autoloop в настройках .options
# * Ставим чара так, что бы в радиусе 2 клеток у него была "A Trash Can" и куча ткани
# * В чара закинуть еду и инструмент (sewing kit)
# * В настройках стелса выставить авто-реконект секунд 10-15
# * Запустить скрипт


class Tailoring:
    def __init__(self):
        self._id_trash = None
        self._quantity_cloth = 10
        self._clot_id = None
        self._tool = None
        self._craft_item = None
        self._break_skill_value = None
        self._menu_chose = None

    def __call__(self):
        while GetSkillValue('Tailoring') < 150:
            if Dead():
                print('Character is dead!')
                break
            # проверяем наличие трешки, ткани и инструмента
            open_backpack()
            if not all(i for i in [self._get_trash_id(), self._check_cloth(), self._check_tool()]):
                break
            # проверяем уровень скилла и выбираем что крафтить
            self._check_skill()
            # крафт
            ct = datetime.now()
            self._make_items()
            # ждём нужные фразы и повторяем поиск(на случай дисконектов)
            while WaitJournalLine(ct, 'Success|You destroyed|You stop.', 15000):
                ct = datetime.now()
                # уничтожаем в треш бочке скрафченые предметы
                self._destroy_items()
                # если скилл равен или привышает нужны:
                # перезаходим в игру что бы остановить игровой autoloop и выходим из цикла
                if GetSkillValue('Tailoring') >= self._break_skill_value:
                    Disconnect()
                    Wait(5000)
                    CheckLag(60000)
                    break
                Wait(1000)
                # если autoloop остановился по каким то причинам ("You stop."), выходим из цикла
                if FoundedParamID() > 1:
                    break
        if GetSkillValue('Tailoring') >= 150:
            print(f"Skill upgraded to {GetSkillValue('Tailoring')}")

    def _destroy_items(self):
        # при первом запуске скрипта или при смене крафтового предмета узнаём type
        # для его последующего удаления
        if self._craft_item is None:
            FindType(-1, Backpack())
            for i in GetFindedList():
                Ignore(i)
            while not FindType(-1, Backpack()):
                Wait(1000)
            self._craft_item = GetType(FindItem())
            IgnoreReset()
        # удаление предмета в треш бочке
        elif f := FindType(self._craft_item, Backpack()):
            MoveItem(f, 1, self._id_trash, 0, 0, 0)

    def _check_skill(self):
        if self._break_skill_value is None or GetSkillValue('Tailoring') >= self._break_skill_value:
            self._craft_item = None
            skills = {
                35: {'chose': ['Shirts', 'Checkered Surcoat'], 'quantity': 15},
                50: {'chose': ['Misc', 'Full Apron'], 'quantity': 10},
                75: {'chose': ['Misc', '(5)'], 'quantity': 15},
                100: {'chose': ['Carpet', '(1)'], 'quantity': 10},
                110: {'chose': ['Carpet', 'Persian Rag 105'], 'quantity': 10},
                115: {'chose': ['Carpet', 'Fancy Persian Rag 110'], 'quantity': 14},
                120: {'chose': ['Carpet', 'Fancy Persian Rag 115'], 'quantity': 14},
                125: {'chose': ['Carpet', 'Fancy Persian Rag 120'], 'quantity': 14},
                130: {'chose': ['Carpet', 'Fancy Persian Rag 125'], 'quantity': 16},
                135: {'chose': ['Carpet', 'Fancy Persian Rag 130'], 'quantity': 16},
                140: {'chose': ['Carpet', 'Fancy Persian Rag 135'], 'quantity': 18},
                145: {'chose': ['Carpet', 'Fancy Persian Rag 140'], 'quantity': 20},
                150: {'chose': ['Carpet', 'Fancy Persian Rag 145'], 'quantity': 25}
            }
            for s in skills:
                if GetSkillValue('Tailoring') < s:
                    self._break_skill_value = int(s)
                    self._menu_chose = skills[s]['chose']
                    self._quantity_cloth = skills[s]['quantity']
                    break

    def _make_items(self):
        if TargetPresent():
            CancelTarget()
        if MenuPresent():
            CancelMenu()
        for _menu_chose in self._menu_chose:
            WaitMenu('What', _menu_chose)
        UseObject(self._tool)
        if WaitForTarget(10000):
            WaitTargetObject(self._clot_id)

    def _check_tool(self):
        if f := FindType(0x0F9D, Backpack()):
            if self._tool is None or self._tool != f:
                self._tool = f
            return True
        else:
            print('Not found sewing tool kit!')
        return False

    def _check_cloth(self):
        FindType(0x1765, Backpack())
        while FindQuantity() < self._quantity_cloth:
            if f := FindType(0x1765, Ground()):
                MoveItem(f, 30000, Backpack(), 0, 0, 1)
                CheckLag(10000)
                Wait(2000)
            else:
                print('Not found cloth!')
                return False
            FindType(0x1765, Backpack())
        self._clot_id = FindItem()
        return True

    def _get_trash_id(self):
        if self._id_trash is None:
            CheckLag(10000)
            if FindType(0x0E77, Ground()):
                for i in GetFindedList():
                    ClickOnObject(i)
                    CheckLag(10000)
                    if 'Trash' in GetTooltip(i):
                        self._id_trash = i
                        return True
            print('Not found A Trash Can')
            return False
        return True


def open_backpack():
    while LastContainer() != Backpack():
        UseObject(Backpack())
        CheckLag(10000)
        Wait(1000)


if __name__ == '__main__':
    SetFindDistance(2)
    SetARStatus(True)
    SetPauseScriptOnDisconnectStatus(True)
    _tailor = Tailoring()
    _tailor()
    SetARStatus(False)
    SetPauseScriptOnDisconnectStatus(False)
    print("End!")
    Disconnect()
