from py_stealth import ClientPrintEx, ClearSystemJournal


def msg(Message):
    print(Message)
    ClientPrintEx(0, 60, 2, Message)


def msgC(Message):
    ClearSystemJournal()
    print(Message)
    ClientPrintEx(0, 60, 2, Message)
