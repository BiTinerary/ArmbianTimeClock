import OPi.GPIO as GPIO
import threading, datetime, time, sys, os

employeeName = sys.argv[1]
dtNow = datetime.datetime.now()
punchDayTime = [dtNow.strftime("%m-%d-%Y"), dtNow.strftime("%H:%M")]

redLedPin = 12
greenLedPin = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redLedPin, GPIO.OUT)
GPIO.setup(greenLedPin, GPIO.OUT)

def blink(color, times):
        def onOff(color):
                ledOn = os.system('echo 1 >/sys/class/leds/%s_led/brightness' % color)
                time.sleep(.1)
                ledOff = os.system('echo 0 >/sys/class/leds/%s_led/brightness' % color)
                time.sleep(.1)

        for x in range(times):
                if len(color) == 2:
                        for redGreen in color:
                                onOff(redGreen)
                else:
                        GPIO.cleanup()
                        time.sleep(.2)
                        GPIO.output(greenLedPin, GPIO.HIGH)
                        time.sleep(.2)
                        GPIO.output(greenLedPin, GPIO.LOW)

def MasterLog(employee, data):
        with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
                MasterLog.write("%s, %s\n" % (employee, data))
        MasterLog.close()
        print 'Master Log Written Succesfully!'

        blink(['red', 'green'], 3)

def timeCard(action, employee, data):
        with open("%s.csv" % (employee), 'a+') as employeeLogFile:
                timeCardData = "%s, %s, %s\n" % (action, data[0], data[1])
                employeeLogFile.write(timeCardData)
        employeeLogFile.close()

        threadFunction(MasterLog, [employee, timeCardData])
        print "%s %s on %s at %s" % (employee, action, data[0], data[1])

def threadFunction(func, array):
        return threading.Thread(target=func, args=(array))

#while True:
#try:
if dtNow.time() < datetime.time(12):
        action = ["CLOCKIN", employeeName, punchDayTime]
        actionThread = threadFunction(timeCard, action)
        ledThread = threadFunction(blink, [greenLedPin, 3])

elif dtNow.time() > datetime.time(12):
        action = ["CLOCKOUT", employeeName, punchDayTime]
        actionThread = threadFunction(timeCard, action)
        ledThread = threadFunction(blink, [greenLedPin, 7])

actionThread.start()
ledThread.start()
actionThread.join()
ledThread.join()
#except:
