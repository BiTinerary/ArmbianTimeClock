import OPi.GPIO as GPIO
from blinky import *
from gSheetPunch import *
from threading import Thread
import datetime, time, sys, os

def MasterLog(employee, data): ## GOOGLE API CREDZ PARAM
        with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
                MasterLog.write("%s,%s" % (employee, data))
        MasterLog.close()
        print 'Master Log Written Succesfully!'
        blink(['red', 'green'], 3)

def timeCard(punch):
        deptSheet, employee, data, action = punch[0], punch[1], punch[2], punch[3]
        directory = 'TimeCards'
        
        if not os.path.exists(directory):
                os.makedirs(directory)
                
        with open("%s/%s.csv" % (directory, employee), 'a+') as employeeLogFile:
                timeCardData = "%s,%s,%s\n" % (action, data[0], data[1])
                employeeLogFile.write(timeCardData)
        employeeLogFile.close()

        MasterLogThread = threadFunction(MasterLog, [employee, timeCardData]) ## GOOGLE API CREDZ PARAM
        MasterLogThread.start()
        
        try:
                gSheetPunch(deptSheet, employee, action)
        except:
                blink(redLedPin, 10)
        print "%s %s on %s at %s" % (employee, action, data[0], data[1])

def threadFunction(func, array):
        return Thread(target=func, args=(array))

def mainSwipe(deptSheet, employeeName):
        
        dtNow = datetime.datetime.now()
        punchDayTime = [dtNow.strftime("%m-%d-%Y"), dtNow.strftime("%H:%M")]
        
        redLedPin = 7
        greenLedPin = 15
        
        try:
                if dtNow.time() < datetime.time(12):
                        punch = [deptSheet, employeeName, punchDayTime, "CLOCKIN"]
                        ledThread = threadFunction(blink, [greenLedPin, 3])

                elif dtNow.time() > datetime.time(12):
                        punch = [deptSheet, employeeName, punchDayTime, "CLOCKOUT"]            
                        ledThread = threadFunction(blink, [greenLedPin, 6])

                timeCard(punch)
                ledThread.start()
        except:
                blink(redLedPin, 10)

if __name__ == '__main__':
        mainSwipe(sys.argv[1], sys.argv[2])  
