from tkinter import *

root=Tk()
root.title('PwndaTxt')
root.geometry('1200x620+10+10')
root.resizable(False,False)
#root.resizable(True,True)
menubar=Menu(root)
root.config(menu=menubar)

#tearoff causes dialogs or commands like save to detach from main frame

#File Menu
filemenu=Menu(menubar, tearoff=False)
menubar.add_cascade(label = 'File', menu=filemenu)

newImage=PhotoImage(file='new.png')
filemenu.add_command(label='New',accelerator='Ctrl+N',image=newImage,compound=LEFT)

openImage=PhotoImage(file='open.png')
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=openImage,compound=LEFT)

saveImage=PhotoImage(file='save.png')
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=saveImage,compound=LEFT)

save_asImage=PhotoImage(file='save_as.png')
filemenu.add_command(label='Save As',accelerator='Ctrl+Alt+S',image=save_asImage,compound=LEFT)

filemenu.add_separator()

exitImage=PhotoImage(file='exit.png')
filemenu.add_command(label='Exit',accelerator='Ctrl+Q',image=exitImage,compound=LEFT)

#Edit Menu
editmenu=Menu(menubar,tearoff=False)

cutImage=PhotoImage(file='cut.png')
editmenu.add_command(label='Cut', accelerator='Ctrl+X',image=cutImage,compound=LEFT)

copyImage=PhotoImage(file='copy.png')
editmenu.add_command(label='Copy', accelerator='Ctrl+C',image=copyImage,compound=LEFT)

pasteImage=PhotoImage(file='paste.png')
editmenu.add_command(label='Paste', accelerator='Ctrl+V',image=pasteImage,compound=LEFT)

clearImage=PhotoImage(file='clear_all.png')
editmenu.add_command(label='Clear', accelerator='Ctrl+Alt+X',image=clearImage,compound=LEFT)

findImage=PhotoImage(file='find.png')
editmenu.add_command(label='Find', accelerator='Ctrl+F',image=findImage,compound=LEFT)

menubar.add_cascade(label = 'Edit', menu=editmenu)

#View Menu
show_toolbar = BooleanVar()
show_statusbar = BooleanVar()
statusImage=PhotoImage(file='status_bar.png');
toolbarImage=PhotoImage(file='tool_bar.png');

viewmenu=Menu(menubar, tearoff=False)
viewmenu.add_checkbutton(label='Toolbar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolbarImage, compound=LEFT)
viewmenu.add_checkbutton(label='Status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImage, compound=LEFT)

menubar.add_cascade(label='View', menu=viewmenu)

root.mainloop()
