from tkinter import *
from tkinter.ttk import *
from tkinter import font

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
statusImage=PhotoImage(file='status_bar.png')
toolbarImage=PhotoImage(file='tool_bar.png')

viewmenu=Menu(menubar, tearoff=False)
viewmenu.add_checkbutton(label='Toolbar', variable=show_toolbar, onvalue=True, offvalue=False, image=toolbarImage, compound=LEFT)
viewmenu.add_checkbutton(label='Status Bar', variable=show_statusbar, onvalue=True, offvalue=False, image=statusImage, compound=LEFT)

menubar.add_cascade(label='View', menu=viewmenu)

#Themes menu
themesmenu=Menu(menubar,tearoff=False)
menubar.add_cascade(label = 'Themes', menu=themesmenu)
theme_choice=StringVar()

lightImage=PhotoImage(file='light_default.png')
themesmenu.add_radiobutton(label='LightDefault',image=lightImage,variable=theme_choice,compound=LEFT)

darkImage=PhotoImage(file='dark.png')
themesmenu.add_radiobutton(label='dark',image=darkImage,variable=theme_choice,compound=LEFT)

pinkImage=PhotoImage(file='red.png')
themesmenu.add_radiobutton(label='red',image=pinkImage,variable=theme_choice,compound=LEFT)

monokaiImage=PhotoImage(file='monokai.png')
themesmenu.add_radiobutton(label='monokai',image=monokaiImage,variable=theme_choice,compound=LEFT)

#toolbar section

tool_bar = Label(root)
tool_bar.pack(side=TOP, fill=X)
font_families=font.families()
font_family_variable=StringVar()

fontfamily_Combobox=Combobox(tool_bar, width=30, values=font_families, state='readonly',textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial')) #Default font
fontfamily_Combobox.grid(row=0,column=0,padx=5)

size_variable=IntVar()
font_size_Combobox=Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=5)

#buttons section

boldImage=PhotoImage(file= 'bold.png')
boldButton=Button(tool_bar, image=boldImage)
boldButton.grid(row=0,column=2,padx=5)

italicImage=PhotoImage(file= 'italic.png')
italicButton=Button(tool_bar, image=italicImage)
italicButton.grid(row=0,column=3,padx=5)

underlineImage=PhotoImage(file= 'underline.png')
underlineButton=Button(tool_bar, image=underlineImage)
underlineButton.grid(row=0,column=4,padx=5)

fontColorImage=PhotoImage(file= 'font_color.png')
fontColorButton=Button(tool_bar, image=fontColorImage)
fontColorButton.grid(row=0,column=5,padx=5)

leftAlignImage=PhotoImage(file= 'left.png')
leftAlignButton=Button(tool_bar, image=leftAlignImage)
leftAlignButton.grid(row=0,column=6,padx=5)

centerAlignImage=PhotoImage(file= 'center.png')
centerAlignButton=Button(tool_bar, image=centerAlignImage)
centerAlignButton.grid(row=0,column=7,padx=5)

rightAlignImage=PhotoImage(file= 'right.png')
rightAlignButton=Button(tool_bar, image=rightAlignImage)
rightAlignButton.grid(row=0,column=8,padx=5)

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

textarea=Text(root, yscrollcommand=scrollbar.set, font=('arial',12))
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)

status_bar=Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)


root.mainloop()
