import os
from tkinter import filedialog, messagebox

from PIL._tkinter_finder import tk


def new_file(text_area, app):
    app.url = ''
    text_area.delete(1.0, tk.END)

def open_file(text_area, app):
    url = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select File',
        filetypes=(('Text File', '*.txt'), ('All Files', '*.*'))
    )
    if url:
        app.url = url
        text_area.delete(1.0, tk.END)
        with open(url, 'r') as file:
            text_area.insert(1.0, file.read())
        app.root.title(os.path.basename(url))

def save_file(text_area, app):
    if not app.url:
        saveas_file(text_area, app)
    else:
        content = text_area.get(1.0, tk.END)
        with open(app.url, 'w') as file:
            file.write(content)
        text_area.edit_modified(False)

def saveas_file(text_area, app):
    url = filedialog.asksaveasfile(
        mode='w',
        defaultextension='.txt',
        filetypes=(('Text File', '*.txt'), ('All Files', '*.*'))
    )
    if url:
        content = text_area.get(1.0, tk.END)
        url.write(content)
        url.close()
        app.url = url.name
        app.root.title(os.path.basename(url.name))

def iexit(text_area, root, app):
    if text_area.edit_modified():
        result = messagebox.askyesnocancel('Warning', 'Do you want to save the file?')
        if result is True:
            if app.url:
                save_file(text_area, app)
                root.destroy()
            else:
                saveas_file(text_area, app)
                root.destroy()
        elif result is False:
            root.destroy()
    else:
        root.destroy()