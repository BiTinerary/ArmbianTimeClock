import time, sys, os
import datetime

dtNow = datetime.datetime.now()
dtPunchDay = dtNow.strftime("%m-%d-%Y")
dtPunchTime = dtNow.strftime("%H:%M")

employeeName = sys.argv[1]

def blink(color, times):
	for x in xrange(times):
		os.system('echo 1 >/sys/class/leds/%s_led/brightness' % color)
		time.sleep(.1)
		os.system('echo 0 >/sys/class/leds/%s_led/brightness' % color)
		time.sleep(.1)
		os.system('echo 1 >/sys/class/leds/%s_led/brightness' % color)
		time.sleep(.1)

def MasterLog(employee, swipeData):
	with open('MasterTimeClockLog.csv', 'a+') as MasterLog:
		MasterLog.write("%s, %s\n" % (employee, swipeData))
	MasterLog.close()

def clockIn(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		clockInData = "CLOCKIN, %s, %s\n" % (dtPunchDay, dtPunchTime)
		employeeLogFile.write(clockInData)
	employeeLogFile.close()

	MasterLog(employee, clockInData)

	print "%s punched in on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink('green', 3)

def clockOut(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		clockOutData = "CLOCKOUT, %s, %s\n" % (dtPunchDay, dtPunchTime)
		employeeLogFile.write(clockOutData)
	employeeLogFile.close()

	MasterLog(employee, clockOutData)

	print "%s punched out on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink('green', 9)

#try:
if dtNow.time() < datetime.time(12):
	clockIn(employeeName)

elif dtNow.time() > datetime.time(12):
	clockOut(employeeName)

#except:
#	blink('red', 3000)