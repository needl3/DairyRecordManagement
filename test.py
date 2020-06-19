import tkinter as tkk, tkcalendar as tc, os, tkinter.messagebox, datetime

default_color = '#d1fcf1'

class ExpenseRecord:
	def __init__(self, title, root, mainframe):
		self.root = root
		self.mainframe = mainframe
		self.title = title
		root.title(title+' Expenses Record')
		root.configure(background=default_color)
		
		tkk.Label(mainframe, text = title.upper() + ' EXPENSES RECORD', bg=default_color, font=('20')).grid(row=0, columnspan=4, pady=20)
		tkk.Button(mainframe, text='Done '+title+'ing', bg=default_color).grid(row=5, column=3)

		if self.title == 'Add' or self.title == 'Edit':
			self.add()
		elif self.title == 'Delete':
			self.delete()
		else:
			self.view()

	def add(self):
		pass
		



if __name__ == '__main__':
	root = tkk.Tk()
	mainframeTest = tkk.LabelFrame(root)
	win1 = ExpenseRecord('Add', root, mainframeTest)
	root.mainloop()