import tkinter as tkk
import tkcalendar as tc
from datetime import datetime
import tkinter.messagebox
import os

# Get todays date in list format
date = datetime.date(datetime.now()).strftime('%Y-%m-%d').split('-')

def give_month(month):
	return {
		1: 'Jan',
		2: 'Feb',
		3: 'Mar',
		4: 'Apr',
		5: 'May',
		6: 'Jun',
		7: 'Jul',
		8: 'Aug',
		9: 'Sep',
		10: 'Oct',
		11: 'Nov',
		12: 'Dec',

	}.get(month)

class milkRecord:
	def __init__(self,title):
		self.title = title
		self.root=tkk.Tk()
		self.root.title(title + ' Milk Record')

		self.headingLabel = tkk.Label(self.root, text=title.upper() + ' MILK RECORD', font=('30'))

		# Left Frame from here
		self.lFrame = tkk.LabelFrame(self.root)
		self.litreEntryM = tkk.Entry(self.lFrame,width=10)
		self.fatEntryM = tkk.Entry(self.lFrame,width=10)
		self.snfEntryM = tkk.Entry(self.lFrame,width=10)

		# Middle frame from here----------
		self.mFrame = tkk.LabelFrame(self.root)
		self.litreEntryE = tkk.Entry(self.mFrame, width=10)
		self.fatEntryE = tkk.Entry(self.mFrame,width=10)
		self.snfEntryE = tkk.Entry(self.mFrame,width=10)

		# Right Frame from here
		self.rFrame = tkk.LabelFrame(self.root)
		# Select date label
		self.cal = tc.Calendar(self.rFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1]))
		self.fetchDataButton = tkk.Button(self.rFrame, text='Check Data', command = self.fetchDataMilk, width=20)
		# Add Record Button
		self.doneButton = tkk.Button(
			self.root, text=title + ' Record', font=('10'), height=3, width=100,
			command = lambda: self.recordAddedMilk(title))

		self.exitButton = tkk.Button(
			self.root, text='Done ' + title + 'ing', height = 2, width=20, command= self.root.destroy
			)
		if title == 'Delete':
			self.changeEntryState('readonly')

	def placeGui(self):

		tkk.Label(self.lFrame, text='MORNING', font=('15')).grid(row=1, padx=5, pady=30, columnspan=4)
		tkk.Label(self.mFrame, text='LITRE').grid(row=2, column=1, padx=5)
		tkk.Label(self.mFrame, text='FAT').grid(row=2, column=2)
		tkk.Label(self.mFrame, text='SNF').grid(row=2, column=3)

		tkk.Label(self.mFrame, text='EVENING', font=('15')).grid(row=1, padx=5, pady=30, columnspan=4)
		tkk.Label(self.lFrame, text='LITRE').grid(row=2, column=1, padx=5)
		tkk.Label(self.lFrame, text='FAT').grid(row=2, column=2)
		tkk.Label(self.lFrame, text='SNF').grid(row=2, column=3)
		
		self.headingLabel.grid(row=0, columnspan=4, padx=10, pady=10)

		self.litreEntryM.grid(row=3, column=1, padx=10, pady=10)
		self.fatEntryM.grid(row=3, column=2, padx=10, pady=10)
		self.snfEntryM.grid(row=3, column=3, padx=10, pady=10)

		self.lFrame.grid(row=1, column=1, padx=20)
		self.litreEntryE.grid(row=3, column=1, padx=10, pady=10)
		self.fatEntryE.grid(row=3, column=2, padx=10, pady=10)
		self.snfEntryE.grid(row=3, column=3, padx=10, pady=10)

		self.mFrame.grid(row=1, column=2, padx=20)

		tkk.Label(self.rFrame, text='Select date', font=('5')).grid(row=0, pady=10, columnspan=2)

		self.cal.grid(row=2, column=1, padx=20, pady=20)

		if self.title == 'Edit' or 'Delete':
			self.fetchDataButton.grid(row=3, columnspan=2, pady=10, padx=10)

		self.rFrame.grid(row=1, column = 3, padx=20, pady=20)

		self.doneButton.grid(row=2, columnspan = 5, padx=10, pady=10)
		self.exitButton.grid(row=3, column=3, padx=10, pady=20, sticky='e')

		self.root.mainloop()

	# Changes the state of entry widget
	# pass in the state as argument
	def changeEntryState(self, stat):
		self.litreEntryM.configure(state=stat)
		self.fatEntryM.configure(state=stat)
		self.snfEntryM.configure(state=stat)

		self.litreEntryE.configure(state=stat)
		self.fatEntryE.configure(state=stat)
		self.snfEntryE.configure(state=stat)


	def recordAddedMilk(self, title=None):
		self.selected_date = self.cal.get_date().split('/')
		entry = self.cal.get_date() + '-{},{},{}-{},{},{}'.format(
				self.litreEntryM.get(),
				self.fatEntryM.get(),
				self.snfEntryM.get(),
				self.litreEntryE.get(),
				self.fatEntryE.get(),
				self.snfEntryE.get()
			)
		
		if title == 'Add':
			flag=False
			
			# Checks for the date selected if its already added or not
			with open('data.txt','r') as file:
				for line in file:
					if line.split('-')[0] == self.cal.get_date():
						flag=True
						break
			if flag:
				tkinter.messagebox.showinfo(
						'Record Exists', 'Record already exists for: '+
						 give_month(int(self.selected_date[0])) + ' ' + self.selected_date[1] + ' 20'+
						 self.selected_date[2] + '\n Edit the record instead of adding.')
				return

			else:
				self.updateFileMilk(entry)

		elif title =='Edit':
			self.updateFileMilk(entry)

		else:
			# No argument means deletion
			self.updateFileMilk()

		self.showConfirmation(success=True)


	# To delete, call it without parameters.
	# To edit, pass the editing line with date.
	def updateFileMilk(self, edit=None):
		with open('temp.txt', 'w') as temp_file:
			with open('data.txt', 'r') as data_file:
				for line in data_file:
					if self.cal.get_date() not in line:
						temp_file.write(line)
				if edit != None:
					temp_file.write('\n'+edit)

		os.remove('data.txt')
		os.rename('temp.txt', 'data.txt')

	# To show data store success, pass success=True
	# To show no data, pass nothing
	def showConfirmation(self, success=False):
		if self.title == 'Delete':
			self.changeEntryState('normal')
			# Morning data
			self.litreEntryM.delete(0, tkk.END)
			self.fatEntryM.delete(0, tkk.END)
			self.snfEntryM.delete(0, tkk.END)

			# Evening data
			self.litreEntryE.delete(0, tkk.END)
			self.fatEntryE.delete(0, tkk.END)
			self.snfEntryE.delete(0, tkk.END)

			self.changeEntryState('readonly')
		if not success:
			# Morning data
			self.litreEntryM.delete(0, tkk.END)
			self.fatEntryM.delete(0, tkk.END)
			self.snfEntryM.delete(0, tkk.END)

			# Evening data
			self.litreEntryE.delete(0, tkk.END)
			self.fatEntryE.delete(0, tkk.END)
			self.snfEntryE.delete(0, tkk.END)
			tkinter.messagebox.showinfo(
					'No Data', 'No previous data found to '+self.title+'.\nFirst Add data for '+
					 give_month(int(self.selected_date[0])) + ' ' + self.selected_date[1] + ' 20' + self.selected_date[2])

			self.fetchDataButton.configure(text='Check Data')

		else:
			tkinter.messagebox.showinfo("Record Update","Record {}ed Successfully for: {} {} 20{}".format(
				self.title,
				give_month(int(self.selected_date[0])),
				self.selected_date[1],
				self.selected_date[2])
			)
	def fetchDataMilk(self):
		flag = False
		# Stores calendar date in string format
		self.selected_date = self.cal.get_date().split('/')

		try:
			with open('data.txt', 'r') as file1:

				# Read through the lines
				for num, line in enumerate(file1, 1):
					splittedData = line.split('-')

					# If data exists
					if self.cal.get_date() == splittedData[0]:
						self.line_number = num
						flag = True
						morning_data = splittedData[1].split(',') 
						evening_data = splittedData[2].split(',')

						# Update the Entries
						if self.title == 'Delete':
							self.changeEntryState('normal')
						# Morning data
						self.litreEntryM.insert(0, morning_data[0])
						self.fatEntryM.insert(0, morning_data[1])
						self.snfEntryM.insert(0, morning_data[2])

						# Evening data
						self.litreEntryE.insert(0, evening_data[0])
						self.fatEntryE.insert(0, evening_data[1])
						self.snfEntryE.insert(0, evening_data[2])

						if self.title == 'Delete':
							self.changeEntryState('readonly')
						self.fetchDataButton.configure(text='Check Data (Data Found)')

						break

			if not flag:
				self.showConfirmation(False)
				return
				
		except FileNotFoundError:
			self.showConfirmation(False)
			return

if __name__ == '__main__':
	milkRecord('Edit').placeGui()