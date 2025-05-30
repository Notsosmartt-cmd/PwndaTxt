import os
import tempfile
from datetime import datetime
import tkinter as tk

def date_time(text_area):
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%d/%m/%Y %H:%M:%S')
    text_area.insert(tk.INSERT, formatted_datetime)

def printout(text_area):
    file = tempfile.mktemp('.txt')
    with open(file, 'w') as f:
        f.write(text_area.get(1.0, tk.END))
    os.startfile(file, 'print')

def statusBarFunction(event, text_area, status_bar):
    if text_area.edit_modified():
        content = text_area.get(1.0, 'end-1c')
        char_count = len(content)
        word_count = len(content.split())
        status_bar.config(text=f'Characters: {char_count} Words: {word_count}')
    text_area.edit_modified(False)