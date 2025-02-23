from tkinter import *

root=Tk()
root.title('PwndaTxt')
root.geometry('1200x620+10+10')
root.resizable(False,False)
#root.resizable(True,True)
menubar=Menu(root)
root.config(menu=menubar)
#tearoff causes dialogs or commands like save to detach from main frame
filemenu=Menu(menubar, tearoff=False)
menubar.add_cascade(label = 'File', menu=filemenu)

editmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label = 'Edit', menu=editmenu)

root.mainloop()
