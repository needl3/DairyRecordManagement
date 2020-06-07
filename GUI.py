# Ask in stackoverflow
# How to automatically catch the calendar data in tkinter whenever user chooses a date without using seperate button to fetch that data?


from tkinter import *
import functions

default_color = '#d1fcf1'
# default_color = 'black'

class mainWindow:
    def __init__(self):
        # GUI
        root = Tk()
        root.title('Diary Income Management System(Personal Use)')
        root.configure(background=default_color)

        # Global Heading
        globalTitle = Label(root, text='DAIRY MILK MANAGEMENT SYSTEM', bg='black', fg='white', font=('Bold', '30'))
        globalTitle.grid(row=0, column=0, columnspan=100, padx=10)

        # Main Frame Window
        self.mainframe = LabelFrame(root, bg=default_color, border=0)

        # Left Child Frame-----------------------------------------------------------------------
        leftFrame = LabelFrame(self.mainframe, bg=default_color, border=0)

        # SubChild Frames
        # Milk Frames
        milkframe = LabelFrame(leftFrame, bg=default_color)

        # Milk Frame's elements
        milkLabel1 = Label(milkframe, text = 'MILK RECORD', height=2, bg=default_color)

        addButtonM = Button(milkframe, text='ADD RECORD', height = 2, width=15, border=1, command = lambda: functions.milkRecord('Add').placeGui(), bg=default_color)
        editButtonM = Button(milkframe, text='EDIT RECORD', height = 2, width=15, border=1, command = lambda: functions.milkRecord('Edit').placeGui(), bg=default_color)
        deleteButtonM = Button(milkframe, text='DELETE RECORD', height = 2, width=15, border=1, bg=default_color, command = lambda: functions.milkRecord('Delete').placeGui())
        viewButtonM = Button(milkframe, text='VIEW RECORD', height = 2, width=15, border=1, bg=default_color, command = self.forgetMainFrame)

        # Milk Frame's elements placement
        milkLabel1.grid(row=1, column=1, columnspan=2)

        addButtonM.grid(row=2, column=1, padx=10, pady=10)
        editButtonM.grid(row=2, column=2, padx=10, pady=10)
        deleteButtonM.grid(row=3, column=1, padx=10, pady=10)
        viewButtonM.grid(row=3, column=2, padx=10, pady=10)

        # Expenses Frame
        expensesframe = LabelFrame(leftFrame, bg=default_color)

        # Expenses Frame's Elements
        expensesLabel1 = Label(expensesframe, text = 'EXPENSES RECORD', height=2, bg=default_color)
        addButtonE = Button(expensesframe, text='ADD RECORD', height = 2, width=15, border=1, bg=default_color)
        editButtonE = Button(expensesframe, text='EDIT RECORD', height = 2, width=15, border=1, bg=default_color)
        deleteButtonE = Button(expensesframe, text='DELETE RECORD', height = 2, width=15, border=1, bg=default_color)
        viewButtonE = Button(expensesframe, text='VIEW RECORD', height = 2, width=15, border=1, bg=default_color)

        # Expenses Frame's elements placement
        expensesLabel1.grid(row=1, column=1, columnspan=2)
        addButtonE.grid(row=2, column=1, padx=10, pady=10)
        editButtonE.grid(row=2, column=2, padx=10, pady=10)
        deleteButtonE.grid(row=3, column=1, padx=10, pady=10)
        viewButtonE.grid(row=3, column=2, padx=10, pady=10)

        # Placing SubChild Frames
        milkframe.grid(row=1, column=1, pady=10)
        expensesframe.grid(row=2, column=1, pady=10)

        netIncomeButton = Button(leftFrame, text = 'SHOW NET INCOME', width=20, height=4, bg=default_color)

        netIncomeButton.grid(row=3,column=1, pady=5)

        # Placing Child Frames
        leftFrame.grid(row = 1, column = 1, padx=10, pady=10)
        # -------------------------------------------------------------------------------------

        # Right Child Frame--------------------------------------------------------------------
        rightFrame = LabelFrame(self.mainframe, bg=default_color)

        # Graph Title
        graphTitleLabel = Label(rightFrame, text='GRAPHICAL INTERPRETATION', bg=default_color, font=('25'))
        graphTitleLabel.grid(row=1,column=1,padx=5,pady=5)

        # Milk Graph Section ......................................
        milkGraphTitle = Label(rightFrame, text='MILK STATUS', bg=default_color)
        milkGraphTitle.grid(row=2, column=1, pady=5)


        # Replace label with graph
        Label(rightFrame, text='GRAPH AREA', width=100, bg=default_color).grid(row=3, column=1, pady=5)
        # .........................................................

        # Expenses Graph Section ......................................
        milkGraphTitle = Label(rightFrame, text='EXPENSES STATUS', bg=default_color)
        milkGraphTitle.grid(row=4, column=1, pady=5)


        # Replace label with graph
        Label(rightFrame, text='GRAPH AREA', width=100, bg=default_color).grid(row=5, column=1, pady=5)
        # .........................................................


        rightFrame.grid(row=1, column=2, padx=10, pady=10)
        # -------------------------------------------------------------------------------------
        # Placed MainFrame
        self.mainframe.grid(pady=10, padx=10)

        root.mainloop()

    def forgetMainFrame(self):
        self.mainframe.destroy()

if __name__ == '__main__':
    win1 = mainWindow()