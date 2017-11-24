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

def clockIn(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		clockInData = "CLOCKIN, %s, %s\n" % (dtPunchDay, dtPunchTime)
		employeeLogFile.write(clockIn)
	employeeLogFile.close()

	with open('MasterTimeClockLog.csv') as MasterLog:
		MasterLog.write("%s, %s\n" % (employee, clockInData))
	MasterLog.close()

	print "%s punched in on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink('green', 3)

def clockOut(employee):
	with open("%s-%s.csv" % (employee, dtPunchDay), 'a+') as employeeLogFile:
		employeeLogFile.write("CLOCKOUT, %s, %s\n" % (dtPunchDay, dtPunchTime))
	employeeLogFile.close()

	print "%s punched out on %s at %s" % (employee, dtPunchDay, dtPunchTime)
	blink('green', 9)

#try:
if dtNow.time() < datetime.time(12):
	clockIn(employeeName)

elif dtNow.time() > datetime.time(12):
	clockOut(employeeName)

#except:
#	blink('red', 3000)