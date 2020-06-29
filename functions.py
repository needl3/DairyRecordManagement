import tkinter as tkk, tkcalendar as tc, tkinter.messagebox, os, datetime

# Global variables
default_color = '#d1fcf1'
dairy_pricing_coefecient = (57.11/(4*8))

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
			with open('milk_data.txt','r') as file:
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
				self.writeDataChronologically(given_data=entry, date=self.selected_date, file_given='milk_data.txt', title = title)
				
				# Then sort the whole document(I will update the algorithm later, it's a bit resource using)
				self.writeDataChronologically(file_given='milk_data.txt', title = title)

		elif title=='Edit':
			self.writeDataChronologically(given_data=entry+'\n', date=self.selected_date, file_given='milk_data.txt', title = title)
		else:
			# Passing date means deleting the record of that date
			self.writeDataChronologically(date=self.selected_date, file_given='milk_data.txt', title = title)


	# To delete, call it with date parmenter.
	# To edit, pass the editing line as given_data=editing_line .
	def writeDataChronologically(self, given_data = None, date=None, file_given=None, title = None):
		print(given_data, date, file_given, title)
		if given_data == None and date == None:	#Sort all data from scratch
			date_list = []
			sorted_data = []
			with open(file_given, 'r') as file:
				data = file.readlines()
			i=0
			for datum in data:
				print('Datum is '+datum)
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

			with open('temp_milk_data.txt', 'w') as file:
				for i in sorted_data:
					file.write(i+'\n')

			os.remove(file_given)
			os.rename('temp_milk_data.txt',file_given)

		elif given_data == None and date != None:	#Delete specific data for given date
			index = None

			# Read file
			with open(file_given, 'r') as file:
				data = file.readlines()

			# Find index of the specific date if exists
			for line in data:
				if date == line.split('-')[0]:
					index = data.index(line)

			# If data exists
			if index != None:
				del data[index]
				with open(file_given, 'w') as file:
					for i in data:
						file.write(i)
			tkinter.messagebox.showinfo('Success', 'Record '+ title+ 'ed for ' +date)

		else:		#Add the given data in the line
			with open(file_given, 'r') as file:
				data = file.readlines()

			# Now find the date's index position
			index = None
			for i in data:
				print(i.split('-')[0], given_data.split('-')[0], i.split('-')[0]==given_data.split('-')[0])
				if i.split('-')[0] in given_data.split('-')[0]:
					print('Inside index conditionn\n')
					index = data.index(i)
					break

			print(index)
			# Abort the adding process if data already exists for that date
			if index != None and title =='Add':
				tkinter.messagebox.showinfo('Record exists', 'Record already exists for '+date+'\nEdit the record instead of adding')
				return
			# Edit
			elif index != None:
				print('In edit')
				del data[index]
				data.insert(index, given_data)
				print('Edited')
			

			# Add
			else:
				print('In add')
				data.append('\n'+given_data)
				print('Added')
			
			
			with open(file_given, 'w') as file:
				for datum in data:
					file.write(datum)
	
			tkinter.messagebox.showinfo('Success', 'Record '+ title+ 'ed for ' +date)

	# To show data store success, pass success=True
	# To show no data, pass nothing
	def showConfirmation(self, selected_date=None, title=None, success=False):
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
					'No Data', 'No previous data found to '+title+'.\nFirst Add data for '+
					 selected_date)

			self.fetchDataButton.configure(text='Check Data')

		else:
			tkinter.messagebox.showinfo("Record Update","Record {}d Successfully for: {}".format(
				title,
				selected_date
				)
			)
	def fetchDataMilk(self):
		flag = False
		# Stores calendar date in string format
		self.selected_date = self.cal.selection_get().strftime('%m/%d/%Y')

		try:
			with open('milk_data.txt', 'r') as file1:

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
				self.showConfirmation(selected_date = self.selected_date, title=self.title)
				return
				
		except FileNotFoundError:
			self.showConfirmation(selected_date = self.selected_date, title = self.title)
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
		temp_month = 12 if int(date[1])-1 == 0 else int(date[1])-1
		cal1 = tc.Calendar(dateRangeFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(temp_month))
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
		def scrollfunction(event):
		    canvas.configure(scrollregion=canvas.bbox("all"),width=670,height=400)
		
		# For Scrollbar
		myframe=tkk.LabelFrame(mainframe2,width=50,height=130,bd=1, bg=default_color)
		myframe.grid(row=2, column=1)


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
		tkk.Label(sectionTitles, text='S.N', borderwidth =2, relief='ridge', font=('30'), bg='cyan').grid(row=2, column=0, rowspan=2, padx=20)
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
		with open('milk_data.txt', 'r') as file:
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
		fatCount=0
		totalMilk = 0
		averageFat = 0
		averageSnf = 0
		for lines in content:
			lines = lines.split('-')

			# Datas
			date_to_be_displayed = lines[0]
			morningMilk = lines[1].split(',')
			eveningMilk = lines[2].split(',')

			# Displays Number
			tkk.Label(sectionTitles, text=str(ro-3), font=('20'), bg=default_color).grid(row=ro, column=0, pady=10)

			# Displays date
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
			if morningMilk[1] != '':
				fatCount += 1
			if eveningMilk[1] != '':
				fatCount += 1

			if morningMilk[0] == '':
				morningMilk[0] = 0
			if eveningMilk[0] == '':
				eveningMilk[0] = 0
			totalMilk += float(morningMilk[0])+float(eveningMilk[0])

			if morningMilk[1] != '':
				averageFat += float(morningMilk[1])
			if eveningMilk[1] != '':
				averageFat += float(eveningMilk[1])

			if morningMilk[2] != '':
				averageSnf += float(morningMilk[2])
			if eveningMilk[2] != '':
				averageSnf += float(eveningMilk[2])

		averageFat = round(averageFat/fatCount, 3)
		averageSnf = round(averageSnf/fatCount, 3)

		# Calculate income based on current pricing scheme
		# of respective dairy companies in this case it's safal dairy
		# Data is that 

		expectedIncome = round(totalMilk * dairy_pricing_coefecient * averageFat * averageSnf, 3)

		# Frame for displaying total quantities of elements
		totalFrame = tkk.Frame(mainframe2, bg=default_color)
		
		# Title Labels
		tkk.Label(totalFrame, text='Total Litres', bg=default_color).grid(row = 1, column=1, padx=20)
		tkk.Label(totalFrame, text='Average Fat', bg=default_color).grid(row = 1, column=2, padx=20)
		tkk.Label(totalFrame, text='Average SNF', bg=default_color).grid(row = 1, column=3, padx=20)
		tkk.Label(totalFrame, text='Expected Income', bg=default_color).grid(row = 1, column=4, padx=20)

		# Labels values
		litreEntry = tkk.Entry(totalFrame, width = 10)
		fatEntry = tkk.Entry(totalFrame, width = 10)
		snfEntry = tkk.Entry(totalFrame, width = 10)
		expectedIncomeEntry = tkk.Entry(totalFrame, width=15)

		litreEntry.insert(0, totalMilk)
		fatEntry.insert(0, averageFat)
		snfEntry.insert(0, averageSnf)
		expectedIncomeEntry.insert(0, expectedIncome)

		litreEntry.configure(state='readonly')
		fatEntry.configure(state='readonly')
		snfEntry.configure(state='readonly')
		expectedIncomeEntry.configure(state='readonly')

		litreEntry.grid(row=2, column=1)
		fatEntry.grid(row=2, column=2)
		snfEntry.grid(row=2, column=3)
		expectedIncomeEntry.grid(row=2, column=4)

		totalFrame.grid(row=3, column=1, pady=20)
	
	def setRange(self, mainframe2, date1, date2):
		intended_dates = [date1+datetime.timedelta(days=i) for i in range((date2-date1).days+1)]
		self.placeData(mainframe2, intended_dates)
class expenseRecord:
	def __init__(self, title, root, mainframe):
		self.title = title
		mainframe.grid(row=1)
		root.title(title+' Expenses Record')
		root.configure(background=default_color)
		
		tkk.Label(mainframe, text = title.upper() + ' EXPENSES RECORD', bg=default_color, font=('20')).grid(row=0, columnspan=10, pady=20)

		if title != 'View':
			self.add(mainframe)
		else:
			self.view(mainframe)

	def add(self, mainframe):

		def writeData():
			if self.title == 'Add' or self.title == 'Edit':
				milkRecord.writeDataChronologically(self,
					given_data='{}-{},{},{},{},{}'.format(cal.selection_get().strftime('%m/%d/%Y'), self.chhokarEntry.get(), self.danaEntry.get(), self.aataEntry.get(), self.gheeEntry.get(),self.otherEntry.get()),
					date=cal.selection_get().strftime('%m/%d/%Y'),
					file_given='expenses_data.txt',
					title=self.title)
				
			else:
				# First get the status of checkbutton 1-ticked, 0-unticked
				data = []
				for i in range(5):
					data.append(var_tkk[i].get())

				# Now replace the 0 with empty string in data from file
				with open('expenses_data.txt', 'r') as file:
					data_from_file = file.readlines()
				flag = False
				for i in data_from_file:
					if i.split('-')[0] == cal.selection_get().strftime('%m/%d/%Y'):
						data_from_file = i.split('-')[1].split(',')
						flag = True
						break
				# If data is not found do this
				if not flag:
					tkinter.messagebox.showinfo('No record', 'No record found to delete for ' + cal.selection_get().strftime('%m/%d/%Y'))
					return
				# If data is found then write it down
				print(data, data_from_file)
				data_from_file_refined = []
				for i in range(5):
					if data[i] == 0:
						data_from_file_refined.append(data_from_file[i])
					else:
						data_from_file_refined.append('')
				data_from_file_refined = ','.join(data_from_file_refined)
				
				print('Final data is:  ' + str(data_from_file_refined))
				
				# First check for all delete condition
				if var_tkk_all.get() == 1:
					print('All data')
					milkRecord.writeDataChronologically(self,
							date=cal.selection_get().strftime('%m/%d/%Y'),
							file_given = 'expenses_data.txt',
							title = 'Delete'
						)
					return

				# These 4 lines will ensure there is atleast 1 ticked checkbutton if all delete button is not ticked
				flag=False
				for i in data_from_file_refined:
					if i != '':
						flag=True
						break
				if flag:
					milkRecord.writeDataChronologically(self,
					given_data=cal.selection_get().strftime('%m/%d/%Y')+'-'+data_from_file_refined+'\n',
					date=cal.selection_get().strftime('%m/%d/%Y'),
					file_given='expenses_data.txt',
					title=self.title)
				else:
					tkinter.messagebox.showinfo('Nothing to delete', 'Tick at least a button to delete for ' + cal.selection_get().strftime('%m/%d/%Y'))

		# Placing left Frame
		leftFrame = tkk.Frame(mainframe, bg=default_color,)
		leftFrame.grid(row=1, column=1)

		# Placing right frame
		rightFrame = tkk.Frame(mainframe, bg=default_color,)
		rightFrame.grid(row=1, column=2, padx=20)

		tkk.Label(rightFrame, text='Select Date', font=('1'), bg= default_color).grid(row=0, pady=10)
		cal = tc.Calendar(rightFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1]))
		cal.grid(row=1)

		if self.title == 'Add' or self.title == 'Edit':
			# Placing quantities Entries
			self.chhokarEntry = tkk.Entry(leftFrame, width=12)
			self.chhokarEntry.grid(row=2, column=1, padx=20)

			self.danaEntry = tkk.Entry(leftFrame, width=12)
			self.danaEntry.grid(row=2, column=2, padx=20)

			self.aataEntry = tkk.Entry(leftFrame, width=12)
			self.aataEntry.grid(row=2, column=3, padx=20)

			self.gheeEntry = tkk.Entry(leftFrame, width=12)
			self.gheeEntry.grid(row=2, column=4, padx=20)

			self.otherEntry = tkk.Entry(leftFrame, width=12)
			self.otherEntry.grid(row=4, column=2, columnspan=2)
			
			self.fetchDataButton = tkk.Button(rightFrame, text='Fetch Data', command=lambda: self.fetchData(
				cal.selection_get().strftime('%m/%d/%Y'),
				file_given = 'expenses_data.txt'), bg=default_color,
			)
			self.fetchDataButton.grid(row=2, pady=10)

			spec_text1 = 'Specify number of boras'
			spec_text2 = 'Other(Specify Rupees)'
		
		elif self.title == 'Delete':
			# Create tkinter variables for checkbuttons
			var_tkk = []
			var_tkk_all = tkk.IntVar()  #This variable is to delete all record
			for i in range(6):
				var_tkk.append(tkk.IntVar())

			# Place CheckButtons for item selection
			for i in range(4):
				tkk.Checkbutton(leftFrame, variable=var_tkk[i], bg=default_color, onvalue=1, offvalue=0).grid(row=2, column=i+1, padx=20)
			tkk.Checkbutton(leftFrame, variable=var_tkk[4], bg=default_color, onvalue=1, offvalue=0).grid(row=4, column=2, columnspan=2, padx=20)

			spec_text1 = 'Tick to delete individual items'
			spec_text2 = 'Other'
			tkk.Label(leftFrame, text='Tick to delete all record for selected date', bg=default_color).grid(row=5, columnspan=5, pady=10)
			tkk.Checkbutton(leftFrame, variable=var_tkk_all, bg=default_color, onvalue=1, offvalue=0).grid(row=6, columnspan=5)


		# Placing expenses titles
		tkk.Label(leftFrame, text=spec_text1, font=('1'), bg=default_color,).grid(row=0, columnspan=5, pady=5)
		tkk.Label(leftFrame, text='Chhokar', bg=default_color,).grid(row=1, column=1)
		tkk.Label(leftFrame, text='Dana', bg=default_color,).grid(row=1, column=2)
		tkk.Label(leftFrame, text='Aata', bg=default_color,).grid(row=1, column=3)
		tkk.Label(leftFrame, text='Ghee', bg=default_color,).grid(row=1, column=4)
		tkk.Label(leftFrame, text=spec_text2, bg=default_color,).grid(row=3, columnspan=5, pady=10)



		addButton = tkk.Button(mainframe, text=self.title + ' Record',
			font=('1'),
			command = writeData,
			bg=default_color
			)
		addButton.grid(row=2, columnspan=3)

	def fetchData(self, cal_date, file_given = None):
		flag = False
		try:
			with open(file_given, 'r') as file:
				read_data = file.readlines()
			for i in read_data:
				if cal_date == i.split('-')[0]:
					self.fetchDataButton.configure(text='Fetch Data(Data Found)')
					self.chhokarEntry.delete(0,tkk.END)
					self.chhokarEntry.insert(0,i.split('-')[1].split(',')[0])

					self.danaEntry.delete(0,tkk.END)
					self.danaEntry.insert(0,i.split('-')[1].split(',')[1])

					self.aataEntry.delete(0,tkk.END)
					self.aataEntry.insert(0,i.split('-')[1].split(',')[2])

					self.gheeEntry.delete(0,tkk.END)
					self.gheeEntry.insert(0,i.split('-')[1].split(',')[3])

					self.otherEntry.delete(0,tkk.END)
					self.otherEntry.insert(0,i.split('-')[1].split(',')[4])
					flag=True
		except FileNotFoundError:
			tkinter.messagebox.showinfo(
					'No Data', 'No previous data found to '+self.title+'.\nFirst Add data for '+
					 cal_date)
		if not flag:
			tkinter.messagebox.showinfo(
			'No Data', 'No previous data found to '+self.title+'.\nFirst Add data for '+
			 cal_date)
	# Lists the total expenses between two selected dates
	def view(self, mainframe):
		current_date = datetime.datetime.now().strftime('%m/%d/%Y')
		
		# Parent Frames for view mosule
		leftFrame = tkk.LabelFrame(mainframe, bg=default_color)
		leftFrame.grid(row=1, column=1, padx=20)
		tkk.Label(leftFrame, text='List of Records', font=('1'), bg=default_color).grid(row=0, columnspan=10, pady=20)

		rightFrame = tkk.LabelFrame(mainframe, bg=default_color, text='Set Date Range')
		rightFrame.grid(row=1, column=2)

		# Right frame contents
		# Child Widgets of dateRangeFrame
		tkk.Label(rightFrame, text='From', font=('8'), padx=20, bg=default_color).grid(row=1, column=1, pady=20)
		temp_month = 12 if int(date[1])-1 ==0 else int(date[1])-1
		cal1 = tc.Calendar(rightFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(temp_month))
		cal1.grid(row=1, column=2, padx=20)

		tkk.Label(rightFrame, text='To', font=('8'), padx=20, bg=default_color).grid(row=3, column=1, pady=20)
		cal2 = tc.Calendar(rightFrame, selectmode='day',
			year=int(date[0]),
			day=int(date[2]),
			month=int(date[1]))
		cal2.grid(row=3, column=2, pady=20, padx=20)
		
		setButton = tkk.Button(
			rightFrame,
			text='Set Range',
			bg=default_color,
			command = lambda: setRange(
				leftFrame,
				cal1.selection_get(),
				cal2.selection_get())
			)
		setButton.grid(row=4, columnspan=3)
		


		# Contents of the headins
		def setRange(mainframe, date1, date2):
			print('Range set as: ' + str(date1) +'   '+str(date2))
			intended_dates = [date1+datetime.timedelta(days=i) for i in range((date2-date1).days+1)]
			placeData(mainframe, intended_dates)

		def placeData(mainframe, ranged_date=[]):

			# Left Frame Contents
			# First make scrollable section
			def scrollfunction(event):
			    canvas.configure(scrollregion=canvas.bbox("all"),width=670,height=400)
			# For Scrollbar
			myframe=tkk.LabelFrame(mainframe,width=50,height=130,bd=1, bg=default_color)
			myframe.grid(row=1, columnspan=10)


			canvas=tkk.Canvas(myframe, bg=default_color)
			sectionTitles=tkk.Frame(canvas, bg=default_color)
			scrollbar=tkk.Scrollbar(myframe,orient="vertical",command=canvas.yview)
			canvas.configure(yscrollcommand=scrollbar.set)

			scrollbar.pack(side="right",fill="y")
			canvas.pack(side="left")
			canvas.create_window((0,0),window=sectionTitles,anchor='nw')
			sectionTitles.bind("<Configure>",scrollfunction)

			# Heading of list
			tkk.Label(sectionTitles, text='S.N', bg=default_color).grid(row=1, column=1, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Date', bg=default_color).grid(row=1, column=2, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Chhokar(Bora)', bg=default_color).grid(row=1, column=3, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Dana(Bora)', bg=default_color).grid(row=1, column=4, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Aata(Bag)', bg=default_color).grid(row=1, column=5, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Ghee(Jar)', bg=default_color).grid(row=1, column=6, padx=20, pady=20)
			tkk.Label(sectionTitles, text='Other(Rs.)', bg=default_color).grid(row=1, column=7, padx=20, pady=20)

			# First read data
			with open('expenses_data.txt', 'r') as file:
				content1 = file.readlines()

			# Check if user has clicked set date button or the window is openes first time
			if len(ranged_date) != 0:
				ranged_date_refined = [i.strftime('%m/%d/%Y') for i in ranged_date]
			# If set button is pressed
			else:
				# Get the dates from today to last month
				today = datetime.date.today()
				first = today.replace(day=1)
				lastMonth = first - datetime.timedelta(days=1)
				delta = today-lastMonth

				ranged_date_refined = [lastMonth+datetime.timedelta(days=i) for i in range(delta.days+1)]
				ranged_date_refined = [i.strftime('%m/%d/%Y') for i in ranged_date_refined]

			content=[]
			for line in content1:
				if line.split('-')[0] in ranged_date_refined:
					content.append(line)
			# 'content' is the data to be displayed
			ro=2
			total_chokkar = 0
			total_dana = 0
			total_aata = 0
			total_ghee = 0
			total_other_expenses = 0
			# this loop will place all available datas between given range
			# ?Also will calculate total of all entities
			for i in content:
				i = i.split('-')
				others = i[1].split(',')
				tkk.Label(sectionTitles, text=ro-1, bg=default_color).grid(row=ro, column=1)
				tkk.Label(sectionTitles, text=i[0], bg=default_color).grid(row=ro, column=2)
				tkk.Label(sectionTitles, text=others[0], bg=default_color).grid(row=ro, column=3)
				tkk.Label(sectionTitles, text=others[1], bg=default_color).grid(row=ro, column=4)
				tkk.Label(sectionTitles, text=others[2], bg=default_color).grid(row=ro, column=5)
				tkk.Label(sectionTitles, text=others[3], bg=default_color).grid(row=ro, column=6)
				tkk.Label(sectionTitles, text=others[4], bg=default_color).grid(row=ro, column=7)
				ro+=1
		
				# Update the 'total' entities
				total_chokkar = total_chokkar+int(others[0]) if others[0] != '' else total_chokkar+0
				total_dana = total_dana+int(others[1]) if others[1] != '' else total_dana+0
				total_aata = total_aata+int(others[2]) if others[2] != '' else total_aata+0
				total_ghee = total_ghee+int(others[3]) if others[3] != '' else total_ghee+0
				total_other_expenses = total_other_expenses+int(others[4]) if others[4] != '' else total_ghee+0

			# Place the section to display total of all these
			# Title of total expenses
			tkk.Label(leftFrame, text='Total Chokkar(Boras)', bg=default_color).grid(row=2, column=1, padx=5, pady=20)
			tkk.Label(leftFrame, text='Total Dana(Boras)', bg=default_color).grid(row=2, column=2, padx=5, pady=20)
			tkk.Label(leftFrame, text='Total Aata(Bag)', bg=default_color).grid(row=2, column=3, padx=5, pady=20)
			tkk.Label(leftFrame, text='Total Ghee(Box)', bg=default_color).grid(row=2, column=4, padx=5, pady=20)
			tkk.Label(leftFrame, text='Total other expenses', bg=default_color).grid(row=2, column=5, padx=5, pady=20)
			tkk.Label(leftFrame, text='Total Net Expenses', bg=default_color).grid(row=2, column=6, padx=50, pady=20)
			# Value of totalExpenses
			chokkar_entry = tkk.Entry(leftFrame, width=10, text=total_chokkar)
			dana_entry = tkk.Entry(leftFrame, width=10)
			aata_entry = tkk.Entry(leftFrame, width=10)
			ghee_entry = tkk.Entry(leftFrame, width=10)
			other_entry = tkk.Entry(leftFrame, width=10)

		# initially place the data from today to previous month
		placeData(leftFrame)


if __name__ == '__main__':
	root = tkk.Tk()
	mainframe = tkk.LabelFrame(root, border=2)
	expenseRecord('View', root, mainframe)
	root.mainloop()

