import tkinter as tk
from tkinter import font, colorchooser

def change_theme(bg_color, fg_color, text_area):
    text_area.config(bg=bg_color, fg=fg_color)

def font_style(style, size, text_area):
    text_area.config(font=(style, size))

def font_size(style, size, text_area):
    text_area.config(font=(style, size))

def bold_text(style, size, text_area):
    text_property = font.Font(font=text_area['font']).actual()
    weight = 'bold' if text_property['weight'] == 'normal' else 'normal'
    text_area.config(font=(style, size, weight))

def italic_text(style, size, text_area):
    text_property = font.Font(font=text_area['font']).actual()
    slant = 'italic' if text_property['slant'] == 'roman' else 'roman'
    text_area.config(font=(style, size, slant))

def underline_text(style, size, text_area):
    text_property = font.Font(font=text_area['font']).actual()
    underline = 1 if text_property['underline'] == 0 else 0
    text_area.config(font=(style, size), underline=underline)

def color_select(text_area):
    color = colorchooser.askcolor()
    if color[1]:
        text_area.config(fg=color[1])

def align_left(text_area):
    data = text_area.get(1.0, tk.END)
    text_area.tag_config('left', justify=tk.LEFT)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, data, 'left')

def align_center(text_area):
    data = text_area.get(1.0, tk.END)
    text_area.tag_config('center', justify=tk.CENTER)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, data, 'center')

def align_right(text_area):
    data = text_area.get(1.0, tk.END)
    text_area.tag_config('right', justify=tk.RIGHT)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.INSERT, data, 'right')