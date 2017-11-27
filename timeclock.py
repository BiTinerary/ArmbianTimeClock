import OPi.GPIO as GPIO
import threading, time, sys
import datetime

employeeName = sys.argv[1]
dtNow = datetime.datetime.now()
punchDayTime = [dtNow.strftime("%m-%d-%Y"), dtNow.strftime("%H:%M")]
redLedPin = 22
greenLedPin = 18

def blink(color, times):
	for x in xrange(times):
		GPIO.cleanup() # Run first in case multiple RFID scans within length of this threads.
		time.sleep(.2) # ^ Only be applicable if erroring out, not for standard clock in/out thread ^
		GPIO.output(color, GPIO.HIGH)
		time.sleep(.2)
		GPIO.output(color, GPIO.LOW)

def MasterLog(employee, data):
	with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
		MasterLog.write("%s, %s\n" % (employee, data))
	MasterLog.close()

	for i in range(2):
		blink(redLedPin)
		blink(greenLedPin)

def timeCard(action, employee, data):
	with open("%s.csv" % (employee), 'a+') as employeeLogFile:
		timeCardData = "%s, %s, %s\n" % (action, data[0], data[1])
		employeeLogFile.write(timeCardData)
	employeeLogFile.close()

	MasterLog(employee, timeCardData)

	print "%s %s on %s at %s" % (employee, action, data[0], data[1])

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redLedPin, GPIO.OUT)
GPIO.setup(greenLedPin, GPIO.OUT)

ledThread = threading.Thread(target=blink, args=(, times))

#try:
if dtNow.time() < datetime.time(12):
	timeCard("CLOCKIN", employeeName, punchDayTime)
	threading.Thread(target=blink, args=(greenLedPin, 3)).start()

elif dtNow.time() > datetime.time(12):
	timeCard("CLOCKOUT", employeeName, punchDayTime)
	threading.Thread(target=blink, args=(greenLedPin, 7)).start()

#except:
#	threading.Thread(target=blink, args=(redLedPin, 25)).start()

#punchDay = dtNow.strftime("%m-%d-%Y")
#punchTime = dtNow.strftime("%H:%M")

"""
def clockIn(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		clockInData = "CLOCKIN, %s, %s\n" % (dtPunchDay, dtPunchTime)
		employeeLogFile.write(clockInData)
	employeeLogFile.close()

	MasterLog(employee, clockInData)

	print "%s punched in on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink(greenLed, 3)

def clockOut(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		clockOutData = "CLOCKOUT, %s, %s\n" % (dtPunchDay, dtPunchTime)
		employeeLogFile.write(clockOutData)
	employeeLogFile.close()

	MasterLog(employee, clockOutData)

	print "%s punched out on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink(greenLed, 9)
"""