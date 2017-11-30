import datetime, gspread, sys, re
from oauth2client.service_account import ServiceAccountCredentials

today = datetime.date.today()
apiCreds = 'MiscScripts-50022bf06964.json'

def getRowColumn(self, worksheet): # ugly code for stripping/regex/parsing hardcoded info from the google sheets.
	self = str(self) # 
	findRegex = str(worksheet.find(self)) 
	stringy = "'" #google response fluff
	stripSyntax = findRegex.rstrip('%s%s%s>' % (stringy, self, stringy)) #strip excess characters from Google's response.
	stripMoreSyntax = stripSyntax.lstrip('<Cell ') # strip Google response, to bare minimum info.
	
	rowRegex = re.compile(r'R(\d{2}|\d)') # regex parameters for parsing googles API internal response. 
	colRegex = re.compile(r'C(\d{2}|\d)')
	searchRow = rowRegex.search(stripMoreSyntax) # actually search, using regex as cross reference.
	searchCol = colRegex.search(stripMoreSyntax)
	finalRowLocation = searchRow.group() # string output of regex search, when matched.
	finalColumnLocation = searchCol.group()

	justTheRowInt = str(finalRowLocation).lstrip('R') # take off R/C string character, leave value. 
	justTheColInt = str(finalColumnLocation).lstrip('C')
	
	return int(justTheRowInt), int(justTheColInt) # return row, column tuple of found/matched cells corresponding to employee name, and todays date on the spreadsheet.

def getCoordOfToday(worksheet): #pass specially formatted datetime to row/column function. Which gets coordinates of cell corresponding to todays date.
	todayToTuple = getRowColumn(str(today.strftime('X%m/X%d/20%y').replace('X0', '').replace('X', '')), worksheet)
	return todayToTuple

def militaryTimestamp(): # return current time. For clock in/out stamp.
	return datetime.datetime.now().strftime('%H:%M')

def clockInCell(name, sheet, worksheet): # the final goods! line 61 is google API command being passed, coordinates of cell with todays date, employee column and current time.
	employeesColumn = getRowColumn(name, worksheet)[1] # get row/column coordinates of employee who is punching time card.
	worksheet.update_cell(getCoordOfToday(worksheet)[0], employeesColumn, militaryTimestamp()) # passing column of cell, row of cell, and what to update it with.
	namePunchAction = 'Name: %s\nDate: %s\nTime: %s\nAction: ClockIn\n' % (name, today.strftime('%m/%d/%y'), militaryTimestamp())
	return namePunchAction

def clockOutCell(name, sheet, worksheet): # Final goods, for clock out.
	employeesColumn = int(getRowColumn(name, worksheet)[1]) + 1 # Same as clock in but plus one. eg. Clock in is on column 5, clock out is column 6. 
	worksheet.update_cell(getCoordOfToday(worksheet)[0], employeesColumn, militaryTimestamp())
	namePunchAction = 'Name: %s\nDate: %s\nTime: %s\nAction: ClockOut\n' % (name, today.strftime('%m/%d/%y'), militaryTimestamp())
	return namePunchAction

def clock(inOut, name, sheet, worksheet):
	if inOut == 'CLOCKIN':
		return clockInCell(name, sheet, worksheet)
	elif inOut == 'CLOCKOUT':
		return clockOutCell(name, sheet, worksheet)

def main(sheetInput, action, employee):
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = ServiceAccountCredentials.from_json_keyfile_name(apiCreds, scope)
	gc = gspread.authorize(credentials)
	sheet = gc.open(sheetInput)
	worksheet = sheet.get_worksheet(0) # process, work on the first tab within above spreadsheet.
	#try:
	print clock(action, employee, sheet, worksheet)
	#except:
	#	print "Date Not Found! Newest Spreadsheet available?"
	#	print "Writing to log"
	#	workSheetName = re.findall(r"'(.*?)'", str(worksheet))
	#	print worksheet
	#	print workSheetName[0]