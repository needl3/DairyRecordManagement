import tkinter as tkk, tkcalendar as tc, tkinter.messagebox, os
import datetime

default_color = '#d1fcf1'

# Get todays date in list format Y/M/D
date = datetime.date.today().strftime('%Y/%m/%d').split('/')

class milkRecord:
	def __init__(self,title, root, mainframe1):
		self.title = title
		self.root=root
		self.root.title(title + ' Milk Record')

		self.mainframe1 = mainframe1
		self.headingLabel = tkk.Label(self.mainframe1, text=title.upper() + ' MILK RECORD', font=('30'), bg=default_color)

		# Left Frame from here
		self.lFrame = tkk.LabelFrame(self.mainframe1, bg=default_color)
		self.litreEntryM = tkk.Entry(self.lFrame,width=10)
		self.fatEntryM = tkk.Entry(self.lFrame,width=10)
		self.snfEntryM = tkk.Entry(self.lFrame,width=10)

		# Middle frame from here----------
		self.mFrame = tkk.LabelFrame(self.mainframe1, bg=default_color)
		self.litreEntryE = tkk.Entry(self.mFrame, width=10)
		self.fatEntryE = tkk.Entry(self.mFrame,width=10)
		self.snfEntryE = tkk.Entry(self.mFrame,width=10)

		# Right Frame from here
		self.rFrame = tkk.LabelFrame(self.mainframe1, bg=default_color)
		# Select date label
		self.cal = tc.Calendar(self.rFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1]))
		if self.title == 'Edit' or self.title == 'Delete':
			self.fetchDataButton = tkk.Button(self.rFrame, text='Check Data', command = self.fetchDataMilk, width=20, bg=default_color)
		# Add Record Button
		self.doneButton = tkk.Button(
			self.mainframe1, text=title + ' Record', font=('10'), height=3, width=100,
			command = lambda: self.recordAddedMilk(title), bg=default_color)

		
		if title == 'Delete':
			self.changeEntryState('readonly')

	def placeGuiMilk(self):

		tkk.Label(self.lFrame, text='MORNING', font=('15'), bg=default_color).grid(row=1, padx=5, pady=30, columnspan=4)
		tkk.Label(self.mFrame, text='LITRE', bg=default_color).grid(row=2, column=1, padx=5)
		tkk.Label(self.mFrame, text='FAT', bg=default_color).grid(row=2, column=2)
		tkk.Label(self.mFrame, text='SNF', bg=default_color).grid(row=2, column=3)

		tkk.Label(self.mFrame, text='EVENING', font=('15'), bg=default_color).grid(row=1, padx=5, pady=30, columnspan=4)
		tkk.Label(self.lFrame, text='LITRE', bg=default_color).grid(row=2, column=1, padx=5)
		tkk.Label(self.lFrame, text='FAT', bg=default_color).grid(row=2, column=2)
		tkk.Label(self.lFrame, text='SNF', bg=default_color).grid(row=2, column=3)
		
		self.headingLabel.grid(row=0, columnspan=4, padx=10, pady=10)

		self.litreEntryM.grid(row=3, column=1, padx=10, pady=10)
		self.fatEntryM.grid(row=3, column=2, padx=10, pady=10)
		self.snfEntryM.grid(row=3, column=3, padx=10, pady=10)

		self.lFrame.grid(row=1, column=1, padx=20)
		self.litreEntryE.grid(row=3, column=1, padx=10, pady=10)
		self.fatEntryE.grid(row=3, column=2, padx=10, pady=10)
		self.snfEntryE.grid(row=3, column=3, padx=10, pady=10)

		self.mFrame.grid(row=1, column=2, padx=20)

		tkk.Label(self.rFrame, text='Select date', font=('5'), bg=default_color).grid(row=0, pady=10, columnspan=2)

		self.cal.grid(row=2, column=1, padx=20, pady=20)

		if self.title == 'Edit' or self.title == 'Delete':
			self.fetchDataButton.grid(row=3, columnspan=2, pady=10, padx=10)

		self.rFrame.grid(row=1, column = 3, padx=20, pady=20)

		self.doneButton.grid(row=2, columnspan = 5, padx=10, pady=10)

		self.mainframe1.grid(row=1, pady=20)

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
		self.selected_date = self.cal.selection_get().strftime('%m/%d/%Y')
		entry = self.cal.selection_get().strftime('%m/%d/%Y') + '-{},{},{}-{},{},{}'.format(
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
					if line.split('-')[0] == self.cal.selection_get().strftime('%m/%d/%Y'):
						flag=True
						break
			if flag:
				tkinter.messagebox.showinfo(
						'Record Exists', 'Record already exists for: '+
						 self.selected_date + '\n Edit the record instead of adding.')
				return

			else:
				# First Add record at last position
				self.writeDataChronologically(given_data=entry)
				
				# Then sort the whole document(I will update the algorithm later, it's a bit resource using)
				self.writeDataChronologically()

		elif title=='Edit':
			self.writeDataChronologically(given_data=entry+'\n')
		else:
			# Passing date means deleting the record of that date
			self.writeDataChronologically(date=self.selected_date)

		self.showConfirmation(success=True)

	# To delete, call it with date parmenter.
	# To edit, pass the editing line as given_data=editing_line .
	def writeDataChronologically(self,given_data = None, date=None):
		if given_data == None and date == None:	#Sort all data from scratch
			date_list = []
			sorted_data = []
			with open('data.txt', 'r') as file:
				data = file.read().split('\n')
			i=0
			for datum in data:
				year = int(datum.split('-')[0].split('/')[2])
				month = int(datum.split('-')[0].split('/')[0])
				day = int(datum.split('-')[0].split('/')[1])
				date_list.append(datetime.datetime(year, month, day))

			date_list.sort()

			# I'm using variables to store even shortterm data
			# to reduce the time complexity by repeated
			# strip and split actions in the loop

			for sorted_date in date_list:
				sorted_date = sorted_date.strftime('%m/%d/%Y')
				for raw_date in data:
					raw_date_temp = raw_date.split('-')[0]
					# print(raw_date_temp)
					if sorted_date == raw_date_temp:
						sorted_data.append(raw_date)

			with open('temp_data.txt', 'w') as file:
				for i in sorted_data:
					file.write(i+'\n')

			os.remove('data.txt')
			os.rename('temp_data.txt','data.txt')

		elif given_data == None and date != None:	#Delete specific data for given date
			index = None

			# Read file
			with open('data.txt', 'r') as file:
				data = file.readlines()

			# Find index of the specific date if exists
			for line in data:
				if date == line.split('-')[0]:
					index = data.index(line)

			# If data exists
			if index != None:
				del data[index]
				with open('data.txt', 'w') as file:
					for i in data:
						print(i)
						file.write(i)

		else:		#Add the given data in the line
			with open('data.txt', 'r') as file:
				data = file.readlines()

			# Now find the date's index position
			index=None
			for i in data:
				if i.split('-')[0] == given_data.split('-')[0]:
					index = data.index(i)
					break

			# Edit
			if index != None:
				del data[index]
				data.insert(index, given_data)
			# Add
			else:
				data.append(given_data)
			
			print(data)
			
			with open('data.txt', 'w') as file:
				for datum in data:
					file.write(datum)
	
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
					 self.selected_date)

			self.fetchDataButton.configure(text='Check Data')

		else:
			tkinter.messagebox.showinfo("Record Update","Record {}ed Successfully for: {}".format(
				self.title,
				self.selected_date
				)
			)
	def fetchDataMilk(self):
		flag = False
		# Stores calendar date in string format
		self.selected_date = self.cal.selection_get().strftime('%m/%d/%Y')

		try:
			with open('data.txt', 'r') as file1:

				# Read through the lines
				for num, line in enumerate(file1, 1):
					splittedData = line.split('-')

					# If data exists
					if self.cal.selection_get().strftime('%m/%d/%Y') == splittedData[0]:
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
class viewMilkRecord:
	def __init__(self, title, root, mainframe2):
		self.title = title
		self.root = root
		self.root.title(title + ' Record')
		self.root.configure(background=default_color)

		# Main Frame
		mainframe2.grid(row=2, pady=20, padx=20)

		# Title
		tkk.Label(mainframe2, text = title.upper() + ' MILK RECORD', bg=default_color, font=('12')).grid(row=1, columnspan = 100, pady=20)

		self.placeData(mainframe2)
		#Date Range Selection
		dateRangeFrame = tkk.LabelFrame(mainframe2, text='Set Date Range', bg=default_color)
		dateRangeFrame.grid(row=2, rowspan=5,column=2, padx=30)

		# Child Widgets of dateRangeFrame
		tkk.Label(dateRangeFrame, text='From', font=('8'), padx=20, bg=default_color).grid(row=1, column=1, pady=20)
		cal1 = tc.Calendar(dateRangeFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1])-1)
		cal1.grid(row=1, column=2, padx=20)

		tkk.Label(dateRangeFrame, text='To', font=('8'), padx=20, bg=default_color).grid(row=3, column=1, pady=20)
		cal2 = tc.Calendar(dateRangeFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1]))
		cal2.grid(row=3, column=2, pady=20, padx=20)
		
		setButton = tkk.Button(
			dateRangeFrame,
			text='Set Range',
			bg=default_color,
			command = lambda: self.setRange(
				mainframe2,
				cal1.selection_get(),
				cal2.selection_get())
			)
		setButton.grid(row=4, columnspan=3)

	def placeData(self, mainframe2, ranged_date=[]):
		# For Scrollbar
		myframe=tkk.LabelFrame(mainframe2,width=50,height=100,bd=1)
		myframe.grid(row=2, column=1)

		def scrollfunction(event):
		    canvas.configure(scrollregion=canvas.bbox("all"),width=650,height=400)

		canvas=tkk.Canvas(myframe, bg=default_color)
		sectionTitles=tkk.Frame(canvas, bg=default_color)
		scrollbar=tkk.Scrollbar(myframe,orient="vertical",command=canvas.yview)
		canvas.configure(yscrollcommand=scrollbar.set)

		scrollbar.pack(side="right",fill="y")
		canvas.pack(side="left")
		canvas.create_window((0,0),window=sectionTitles,anchor='nw')
		sectionTitles.bind("<Configure>",scrollfunction)

		# # Section titles
		# sectionTitles = tkk.LabelFrame(canvas, border=2, bg=default_color)
		# sectionTitles.pack(side='left')

		
		# Date
		tkk.Label(sectionTitles, text='Date', borderwidth=2, relief='ridge', font=('30'), bg='cyan').grid(row=2, column=1, rowspan=2, padx=40)

		# Morning section
		tkk.Label(sectionTitles, text='MORNING', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=2, column=2, columnspan=3, padx=40)
		tkk.Label(sectionTitles, text='LITRE', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=2, padx=20, pady=10)
		tkk.Label(sectionTitles, text='FAT', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=3, padx=20, pady=10)
		tkk.Label(sectionTitles, text='SNF', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=4, padx=20, pady=10)

		# Evening Section
		tkk.Label(sectionTitles, text='EVENING', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=2, column=5, columnspan=4, padx=40)
		tkk.Label(sectionTitles, text='LITRE', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=5, padx=20, pady=10)
		tkk.Label(sectionTitles, text='FAT', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=6, padx=20, pady=10)
		tkk.Label(sectionTitles, text='SNF', borderwidth=2, relief = 'ridge', font=('30'), bg='cyan').grid(row=3, column=7, padx=20, pady=10)

		# Read all record
		with open('data.txt', 'r') as file:
			content1 = file.read()
		
		if len(ranged_date) != 0:
			ranged_date_refined = [i.strftime('%m/%d/%Y') for i in ranged_date]
		else:
			# Get the dates from today to last month
			today = datetime.date.today()
			first = today.replace(day=1)
			lastMonth = first - datetime.timedelta(days=1)
			delta = today-lastMonth

			ranged_date_refined = [lastMonth+datetime.timedelta(days=i) for i in range(delta.days+1)]
			ranged_date_refined = [i.strftime('%m/%d/%Y') for i in ranged_date_refined]

		content1 = content1.split('\n')
		content=[]
		for line in content1:
			if line.split('-')[0] in ranged_date_refined:
				content.append(line)
			# Write an algorithm to store the data
			# of dates between max and min dates

		ro = 4
		for lines in content:
			lines = lines.split('-')

			# Datas
			date_to_be_displayed = lines[0]
			morningMilk = lines[1].split(',')
			eveningMilk = lines[2].split(',')

			tkk.Label(sectionTitles, text=date_to_be_displayed, font=('20'), bg=default_color).grid(row = ro, column = 1, pady=10)
			
			# Morning Data
			tkk.Label(sectionTitles, text=morningMilk[0], font=('20'), bg=default_color).grid(row=ro, column=2, pady=10)
			tkk.Label(sectionTitles, text=morningMilk[1], font=('20'), bg=default_color).grid(row=ro, column=3, pady=10)
			tkk.Label(sectionTitles, text=morningMilk[2], font=('20'), bg=default_color).grid(row=ro, column=4, pady=10)

			# Evening Data
			tkk.Label(sectionTitles, text=eveningMilk[0], font=('20'), bg=default_color).grid(row=ro, column=5, pady=10)
			tkk.Label(sectionTitles, text=eveningMilk[1], font=('20'), bg=default_color).grid(row=ro, column=6, pady=10)
			tkk.Label(sectionTitles, text=eveningMilk[2], font=('20'), bg=default_color).grid(row=ro, column=7, pady=10)
			ro += 1

	def setRange(self, mainframe2, date1, date2):
		intended_dates = [date1+datetime.timedelta(days=i) for i in range((date2-date1).days+1)]
		self.placeData(mainframe2, intended_dates)
class expensesRecord:
	def __init__(self, title, root, mainframe2):
		pass




if __name__ == '__main__':
	root = tkk.Tk()
	mainframe = tkk.LabelFrame(root, border=2)
	milkRecord('Add', root, mainframe).placeGuiMilk()
	root.mainloop()

