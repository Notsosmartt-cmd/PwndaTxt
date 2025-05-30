import tkinter as tk
from tkinter import ttk

def find(text_area):
    def find_words():
        text_area.tag_remove('match', 1.0, tk.END)
        start_pos = '1.0'
        word = find_entry.get()
        if word:
            while True:
                start_pos = text_area.search(word, start_pos, stopindex=tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_area.tag_add('match', start_pos, end_pos)
                text_area.tag_config('match', foreground='red', background='yellow')
                start_pos = end_pos

    def replace_text():
        word = find_entry.get()
        replace_word = replace_entry.get()
        content = text_area.get(1.0, tk.END)
        new_content = content.replace(word, replace_word)
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, new_content)

    root = tk.Toplevel()
    root.title('Find')
    root.geometry('450x250+500+200')
    root.resizable(False, False)

    label_frame = ttk.LabelFrame(root, text='Find/Replace')
    label_frame.pack(pady=50)

    # Find
    ttk.Label(label_frame, text='Find:').grid(row=0, column=0, padx=5, pady=5)
    find_entry = ttk.Entry(label_frame)
    find_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(label_frame, text='FIND', command=find_words).grid(row=2, column=0, padx=5, pady=5)

    # Replace
    ttk.Label(label_frame, text='Replace:').grid(row=1, column=0, padx=5, pady=5)
    replace_entry = ttk.Entry(label_frame)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(label_frame, text='REPLACE', command=replace_text).grid(row=2, column=1, padx=5, pady=5)

    def on_close():
        text_area.tag_remove('match', 1.0, tk.END)
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()