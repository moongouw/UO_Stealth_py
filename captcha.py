from py_stealth import *
from Scripts.Include.message import msg
from math import sqrt


def GetLength(x1, y1, x2, y2):
    x = (x2 - x1) ** 2
    y = (y2 - y1) ** 2
    return round(sqrt(x + y))


def GetRange(l):
    result = []
    for i in range(len(l[0]) - 1):
        result.append(
            GetLength(l[0][i], l[1][i], l[0][i + 1], l[1][i + 1])
        )
    result = sorted(result)
    resultMax = result[len(result) - 1] + ((result[len(result) - 1] / 100) * 20)
    resultMiddle = round(sum(result) / len(result))
    resultMiddle += (resultMiddle / 100) * 2
    return [round(resultMiddle), round(resultMax)]


def GetBlocks(l):
    array = [[], []]
    block = [[], []], [[], []], [[], []], [[], []]
    t = 0
    for b in range(0, 4):
        for i in range(t, t + 5):
            array[0].append(l[0][i])
            array[1].append(l[1][i])
        rangeMax = GetRange(array)
        array[0].clear()
        array[1].clear()
        for i in range(t, len(l[0])):
            block[b][0].append(l[0][i])
            block[b][1].append(l[1][i])
            if b < 3 and GetLength(l[0][i], l[1][i], l[0][i + 1], l[1][i + 1]) >= rangeMax[1]:
                t = i + 1
                break
    return block


def CheckBlock(l):
    n3 = [0, 0, 0, 1, 0, 0, 0, 1, 0, 0]
    n4 = [1, 1, 1, 1, 0, 0, 0, 0]
    n5 = [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]
    n6 = [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0]
    n7 = [0, 0, 1, 1, 0, 0, 0]
    n8 = [0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0]
    n9 = [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0]
    array = [n3, n4, n5, n6, n7, n8, n9]
    result = ''
    for b in range(len(l)):
        if len(l[b]) == 4:
            result += '1'
            continue
        for i in range(3, 11):
            if i >= 10:
                result += '2'
                break
            if l[b] == array[i-3]:
                result += str(i)
                break
    return result


def DecryptBlocks(l):
    array = [[], [], [], []]
    for b in range(len(l)):
        rangeMiddle = GetRange(l[b])[0]
        for i in range(len(l[b][0]) - 1):
            gl = GetLength(l[b][0][i], l[b][1][i], l[b][0][i + 1], l[b][1][i + 1])
            if gl <= rangeMiddle:
                array[b].append(0)
            else:
                array[b].append(1)
    return CheckBlock(array)


def GetXYCoordinates(text):
    result = [], []
    for i in range(len(text)):
        result[0].append(text[i].get('X'))
        result[1].append(text[i].get('Y'))
    return result


def Captcha():
    if IsGump():
        g = GetGumpInfo(GetGumpsCount() - 1)
        if g.get('Text')[0][0].find("капча") != -1:
            YXCoorList = GetXYCoordinates(g.get('TilePics'))
            b = GetBlocks(YXCoorList)
            numberList = DecryptBlocks(b)
            msg(f'numbers in captcha: {numberList}')
            GumpAutoTextEntry(g.get('TextEntries')[0].get('ReturnValue'), numberList)
            NumGumpButton(GetGumpsCount() - 1, g.get('GumpButtons')[0].get('ReturnValue'))
            Wait(1000)
        else:
            CloseSimpleGump(GetGumpsCount() - 1)
