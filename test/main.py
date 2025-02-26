from tkinter import *
from tkinter.ttk import *
from tkinter import font,colorchooser,filedialog
import os

#Functionality part
url = ''
def new_file():
    textarea.delete(0.0,END)

def open_file():
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd(),title='Select File', filetypes=(('Text File','txt'), ('All Files','*.*')))
    # This prints the content from data to console
    # print(data.read())
    if url != '':
        textarea.delete(0.0, END)
        data = open(url, 'r') # 'r' is read mode
        textarea.insert(0.0,data.read())
        root.title(os.path.basename(url))

def save_file():
    if url =='':
        save_url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('Text File','txt'),
                                                                                    ('All Files','*.*')))
        content=textarea.get(0.0,END)
        save_url.write(content)
        save_url.close()
    else:
        content=textarea.get(0.0, END)
        file = open(url, 'w')
        file.write(content)

fontSize=12
fontStyle='Consolas'
def font_style(event):
    global fontStyle
    fontStyle=font_family_variable.get()
    textarea.config(font=(fontStyle,fontSize))

def font_size(event):
    global fontSize
    fontSize = size_variable.get()
    textarea.config(font=(fontStyle, fontSize))

def bold_text():
    text_property=font.Font(font=textarea['font']).actual()
    if text_property['weight']=='normal':
        textarea.config(font=(fontStyle,fontSize,'bold'))

    if text_property['weight']=='bold':
        textarea.config(font=(fontStyle,fontSize,'normal'))

def italic_text():
    text_property = font.Font(font=textarea['font']).actual()
    #print(text_property)
    if text_property['slant'] == 'roman':
        textarea.config(font=(fontStyle, fontSize, 'italic'))

    if text_property['slant'] == 'italic':
        textarea.config(font=(fontStyle, fontSize, 'roman'))

def underline_text():
    text_property = font.Font(font=textarea['font']).actual()
    if text_property['underline'] == 0:
        textarea.config(font=(fontStyle, fontSize, 'underline'))

    if text_property['underline'] == 1:
        textarea.config(font=(fontStyle, fontSize))

def color_select():
    color=colorchooser.askcolor()
    textarea.config(fg=color[1])

def align_right():
    data = textarea.get(0.0, END)
    textarea.tag_config('right', justify=RIGHT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'right')


def align_left():
    data = textarea.get(0.0, END)
    textarea.tag_config('left', justify=LEFT)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'left')

def align_center():
    data = textarea.get(0.0, END)
    textarea.tag_config('center', justify=CENTER)
    textarea.delete(0.0, END)
    textarea.insert(INSERT, data, 'center')


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
filemenu.add_command(label='New',accelerator='Ctrl+N',image=newImage,compound=LEFT,command=new_file)

openImage=PhotoImage(file='open.png')
filemenu.add_command(label='Open',accelerator='Ctrl+O',image=openImage,compound=LEFT,command=open_file)

saveImage=PhotoImage(file='save.png')
filemenu.add_command(label='Save',accelerator='Ctrl+S',image=saveImage,compound=LEFT,command=save_file)

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
#Fonts
fontfamily_Combobox=Combobox(tool_bar, width=30, values=font_families, state='readonly',textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Consolas')) #Default font
fontfamily_Combobox.grid(row=0,column=0,padx=5)
fontfamily_Combobox.bind('<<ComboboxSelected>>', font_style)

#Font sizes
size_variable=IntVar()
font_size_Combobox=Combobox(tool_bar,width=14,textvariable=size_variable,state='readonly',values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0,column=1,padx=5)
font_size_Combobox.bind('<<ComboboxSelected>>', font_size)


#buttons section

boldImage=PhotoImage(file= 'bold.png')
boldButton=Button(tool_bar, image=boldImage,command=bold_text)
boldButton.grid(row=0,column=2,padx=5)


italicImage=PhotoImage(file= 'italic.png')
italicButton=Button(tool_bar, image=italicImage,command=italic_text)
italicButton.grid(row=0,column=3,padx=5)

underlineImage=PhotoImage(file= 'underline.png')
underlineButton=Button(tool_bar, image=underlineImage,command=underline_text)
underlineButton.grid(row=0,column=4,padx=5)

fontColorImage=PhotoImage(file= 'font_color.png')
fontColorButton=Button(tool_bar, image=fontColorImage, command=color_select)
fontColorButton.grid(row=0,column=5,padx=5)

leftAlignImage=PhotoImage(file= 'left.png')
leftAlignButton=Button(tool_bar, image=leftAlignImage, command=align_left)
leftAlignButton.grid(row=0,column=6,padx=5)

centerAlignImage=PhotoImage(file= 'center.png')
centerAlignButton=Button(tool_bar, image=centerAlignImage, command=align_center)
centerAlignButton.grid(row=0,column=7,padx=5)

rightAlignImage=PhotoImage(file= 'right.png')
rightAlignButton=Button(tool_bar, image=rightAlignImage, command=align_right)
rightAlignButton.grid(row=0,column=8,padx=5)

scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

textarea=Text(root, yscrollcommand=scrollbar.set, font=('Consolas',12))
textarea.pack(fill=BOTH,expand=True)
scrollbar.config(command=textarea.yview)

status_bar=Label(root, text='Status Bar')
status_bar.pack(side=BOTTOM)


root.mainloop()
