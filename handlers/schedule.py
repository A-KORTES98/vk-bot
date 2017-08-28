import time
import os
parentDir = os.path.dirname(os.path.dirname(__file__))

TIMEDIFF_Ashburn_Spb = 25200

timesched = {
    'CLASS1' : {'start': (8, 0), 'break_dur': 15, 'toStr' : '8:00-9:35  '},
    'CLASS2' : {'start': (9, 50), 'break_dur': 15, 'toStr' : '9:50-11:25 '},
    'CLASS3' : {'start': (11, 40), 'break_dur': 30, 'toStr' : '11:40-13:15'},
    'CLASS4' : {'start': (13, 45), 'break_dur': 15, 'toStr' : '13:45-15:20'},
    'CLASS5' : {'start': (15, 35), 'break_dur': 15, 'toStr' : '15:35-17:10'},
    'CLASS6' : {'start': (17, 25), 'break_dur': 15, 'toStr' : '17:25-19:00'}
}

def getEndOfCls(starting):
    return (starting[0] + 1, starting[1] + 35) if starting[1] < 25 else (starting[0] + 2, (starting[1] + 35) % 60)


def timeGrandThen(fTime, sTime):
    if (fTime[0] > sTime[0]):
        return True
    elif (fTime[0] == sTime[0]) and (fTime[1] > sTime[1]):
        return True
    else:
        return False


def formSchdlResponse(todayCls, cTime):
    rezult = todayCls.pop(0).pop() + '\n'
    isCurOrNextClsDetect = False
    numOfCls = 1
    for uClass in todayCls:
        curCls = timesched[('CLASS' + str(numOfCls))]
        fEl = uClass.pop(0)
        numOfCls += 1
        if fEl == "-\n":
            rezult += curCls['toStr'] + '   -\n'
            continue
        sEl = uClass.pop(0)
        rezult += curCls['toStr'] + '|ауд. №: ' + uClass.pop(0) + '|' + uClass.pop(0)
        if isCurOrNextClsDetect == False:
            if (timeGrandThen(curCls['start'], cTime)):
                rezult += '     \u21E2\n'
                isCurOrNextClsDetect = True
            elif timeGrandThen(getEndOfCls((curCls['start'])), cTime):
                rezult += '     \u0298\n'
                isCurOrNextClsDetect = True
            else:
                rezult += '\n'
        else:
            rezult += '\n'
    if not isCurOrNextClsDetect:
        rezult += '\nНа сегодня всё =)))'
        #True:
    print(rezult)
    return rezult

def getSchedle():
    tm = time.localtime(time.time()+TIMEDIFF_Ashburn_Spb)
    print(tm)
    isOddWeek ='1' if (tm.tm_yday-226) % 14 < 7 else '2'
    if tm.tm_wday == 6:
        return 'Воскресенье\n\nToday there are no classes amigo!'
    if tm.tm_wday == 5:
        return 'Суббота\n\nToday there are no classes amigo!'
    if tm.tm_wday == 2:
        return 'Среда\n\n9:50-17:10 ВМП'
    currDayOfWeek = '#' + str(tm.tm_wday) + '\n'
    currTime = (tm.tm_hour, tm.tm_min)
    schedule = open(parentDir + '/schedules/schedule' + isOddWeek + '.txt', 'r')
    todaysCls = []
    strInFile = ''
    while strInFile != currDayOfWeek:
        strInFile = schedule.readline()
    while True:
        strInFile = schedule.readline()
        if (strInFile == '\n'):
            break
        todaysCls.append(strInFile.split(' '))
    for i in todaysCls:
        print(i)
    i = 0
    return formSchdlResponse(todaysCls, currTime)

