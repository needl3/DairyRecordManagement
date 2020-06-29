from GUI import mainWindow
from tkinter import *


if __name__ == '__main__':
    root = Tk()
    # root.wm_geometry(
    #     str(root.winfo_screenwidth())+'x'+str(root.winfo_screenheight())+'+'+'0+0'
    #     )
    win1 = mainWindow(root)
    win1.placeGuiMain()
    root.mainloop()
