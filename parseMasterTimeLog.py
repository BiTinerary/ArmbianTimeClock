import csv

with open('masterTimeLog.csv', 'r') as parseMasterLog:
	reader = csv.reader(parseMasterLog)
	swipes = list(reader)

	for each in swipes:
		if each[1] == 'CLOCKIN':
			print "%s %s @ %s on %s" % (each[0], each[1], each[3], each[2])
