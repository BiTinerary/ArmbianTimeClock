import OPi.GPIO as GPIO
from blinky import *
#from threading import Thread
import threading, datetime, time, sys, os

def MasterLog(employee, data): ## GOOGLE API CREDZ PARAM
        with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
                MasterLog.write("%s, %s" % (employee, data))
        MasterLog.close()
        print 'Master Log Written Succesfully!'
        
        ## PARSE MASTERLOG FOR HUMAN VIEWING
        ## CREATE MASTER SHEET
        ## GOOGLE CREDZ API, PUNCH GSHEET WITH MASTER SHEET 
        
        blink(['red', 'green'], 3)

def timeCard(punch):
        action, employee, data = punch[0], punch[1], punch[2]
        
        with open("%s.csv" % (employee), 'a+') as employeeLogFile:
                timeCardData = "%s, %s, %s\n" % (action, data[0], data[1])
                employeeLogFile.write(timeCardData)
        employeeLogFile.close()

        MasterLogThread = threadFunction(MasterLog, [employee, timeCardData]) ## GOOGLE API CREDZ PARAM
        MasterLogThread.start()
        print "%s %s on %s at %s" % (employee, action, data[0], data[1])

def threadFunction(func, array):
        return threading.Thread(target=func, args=(array))

def everySwipe():
        employeeName = sys.argv[1]
        dtNow = datetime.datetime.now()
        punchDayTime = [dtNow.strftime("%m-%d-%Y"), dtNow.strftime("%H:%M")]
        
        redLedPin = 7
        greenLedPin = 15
        
        try:
                if dtNow.time() < datetime.time(12):
                        punch = ["CLOCKIN", employeeName, punchDayTime]
                        #actionThread = threadFunction(timeCard, action).start()
                        ledThread = threadFunction(blink, [greenLedPin, 3])

                elif dtNow.time() > datetime.time(12):
                        punch = ["CLOCKOUT", employeeName, punchDayTime]            
                        #actionThread = threadFunction(timeCard, action).start
                        ledThread = threadFunction(blink, [greenLedPin, 6])

                timeCard(punch)
                ledThread.start()
        except:
                blink(redLedPin, 9999)
everySwipe()  
