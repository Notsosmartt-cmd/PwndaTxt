import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk, Menu, font, colorchooser, messagebox
import os
import sys
import subprocess
from . import file_operations, formatting, search, utilities


class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('PwndaTxt')
        self.root.geometry('1200x620+10+10')
        self.root.resizable(False, False)

        self.url = ''
        self.font_size = 12
        self.font_style = 'Consolas'
        self.show_toolbar = tk.BooleanVar(value=True)
        self.show_statusbar = tk.BooleanVar(value=True)

        self.password_var = tk.StringVar()
        self.load_menu_images()
        self.setup_menus()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        self.setup_bindings()

    def load_menu_images(self):
        """Load all images for menu items"""
        # Menu Images
        self.new_image = PhotoImage(file='../photos/new.png')
        self.open_image = PhotoImage(file='../photos/open.png')
        self.save_image = PhotoImage(file='../photos/save.png')
        self.save_as_image = PhotoImage(file='../photos/save_as.png')
        self.print_image = PhotoImage(file='../photos/print.png')
        self.exit_image = PhotoImage(file='../photos/exit.png')
        self.cut_image = PhotoImage(file='../photos/cut.png')
        self.copy_image = PhotoImage(file='../photos/copy.png')
        self.paste_image = PhotoImage(file='../photos/paste.png')
        self.select_image = PhotoImage(file='../photos/checked.png')
        self.clear_image = PhotoImage(file='../photos/clear_all.png')
        self.find_image = PhotoImage(file='../photos/find.png')
        self.datetime_image = PhotoImage(file='../photos/calender.png')
        self.status_image = PhotoImage(file='../photos/status_bar.png')
        self.toolbar_image = PhotoImage(file='../photos/tool_bar.png')
        self.light_image = PhotoImage(file='../photos/light_default.png')
        self.dark_image = PhotoImage(file='../photos/dark.png')
        self.red_image = PhotoImage(file='../photos/red.png')
        self.monokai_image = PhotoImage(file='../photos/monokai.png')
        self.home_image = PhotoImage(file='../photos/undo.png')  # Added home image

        # Toolbar images
        self.bold_image = PhotoImage(file='../photos/bold.png')
        self.italic_image = PhotoImage(file='../photos/italic.png')
        self.underline_image = PhotoImage(file='../photos/underline.png')
        self.font_color_image = PhotoImage(file='../photos/font_color.png')
        self.left_align_image = PhotoImage(file='../photos/left.png')
        self.center_align_image = PhotoImage(file='../photos/center.png')
        self.right_align_image = PhotoImage(file='../photos/right.png')

    def setup_menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu - with images like original
        file_menu = Menu(menubar, tearoff=False)
        menubar.add_cascade(label='File', menu=file_menu)

        file_menu.add_command(
            label='New',
            accelerator='Ctrl+N',
            image=self.new_image,
            compound=LEFT,
            command=lambda: file_operations.new_file(self.text_area, self)
        )

        file_menu.add_command(
            label='Open',
            accelerator='Ctrl+O',
            image=self.open_image,
            compound=LEFT,
            command=lambda: file_operations.open_file(self.text_area, self)
        )

        file_menu.add_command(
            label='Save',
            accelerator='Ctrl+S',
            image=self.save_image,
            compound=LEFT,
            command=lambda: file_operations.save_file(self.text_area, self)
        )

        file_menu.add_command(
            label='Save As',
            accelerator='Ctrl+Alt+S',
            image=self.save_as_image,
            compound=LEFT,
            command=lambda: file_operations.saveas_file(self.text_area, self)
        )

        file_menu.add_command(
            label='Print',
            accelerator='Ctrl+P',
            image=self.print_image,
            compound=LEFT,
            command=lambda: utilities.printout(self.text_area)
        )

        file_menu.add_separator()

        file_menu.add_command(
            label='Exit',
            accelerator='Ctrl+Q',
            image=self.exit_image,
            compound=LEFT,
            command=lambda: file_operations.iexit(self.text_area, self.root, self)
        )

        # Edit Menu - with images like original
        edit_menu = Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Edit', menu=edit_menu)

        edit_menu.add_command(
            label='Cut',
            accelerator='Ctrl+X',
            image=self.cut_image,
            compound=LEFT,
            command=lambda: self.text_area.event_generate('<<Cut>>')
        )

        edit_menu.add_command(
            label='Copy',
            accelerator='Ctrl+C',
            image=self.copy_image,
            compound=LEFT,
            command=lambda: self.text_area.event_generate('<<Copy>>')
        )

        edit_menu.add_command(
            label='Paste',
            accelerator='Ctrl+V',
            image=self.paste_image,
            compound=LEFT,
            command=lambda: self.text_area.event_generate('<<Paste>>')
        )

        edit_menu.add_command(
            label='Select All',
            accelerator='Ctrl+A',
            image=self.select_image,
            compound=LEFT,
            command=lambda: self.text_area.event_generate('<<SelectAll>>')
        )

        edit_menu.add_command(
            label='Clear',
            accelerator='Ctrl+Alt+X',
            image=self.clear_image,
            compound=LEFT,
            command=lambda: self.text_area.delete(1.0, tk.END)
        )

        edit_menu.add_command(
            label='Find',
            accelerator='Ctrl+F',
            image=self.find_image,
            compound=LEFT,
            command=lambda: search.find(self.text_area)
        )

        edit_menu.add_command(
            label='Time/Date',
            accelerator='Ctrl+D',
            image=self.datetime_image,
            compound=LEFT,
            command=lambda: utilities.date_time(self.text_area)
        )

        # View Menu - with images like original
        view_menu = Menu(menubar, tearoff=False)
        menubar.add_cascade(label='View', menu=view_menu)

        view_menu.add_checkbutton(
            label='Toolbar',
            variable=self.show_toolbar,
            onvalue=True,
            offvalue=False,
            image=self.toolbar_image,
            compound=LEFT,
            command=self.toggle_toolbar
        )

        view_menu.add_checkbutton(
            label='Status Bar',
            variable=self.show_statusbar,
            onvalue=True,
            offvalue=False,
            image=self.status_image,
            compound=LEFT,
            command=self.toggle_statusbar
        )

        # Themes Menu - with images like original
        themes_menu = Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Themes', menu=themes_menu)

        themes_menu.add_radiobutton(
            label='LightDefault',
            image=self.light_image,
            compound=LEFT,
            command=lambda: formatting.change_theme('white', 'black', self.text_area)
        )

        themes_menu.add_radiobutton(
            label='Dark',
            image=self.dark_image,
            compound=LEFT,
            command=lambda: formatting.change_theme('gray20', 'white', self.text_area)
        )

        themes_menu.add_radiobutton(
            label='Red',
            image=self.red_image,
            compound=LEFT,
            command=lambda: formatting.change_theme('pink', 'blue', self.text_area)
        )

        themes_menu.add_radiobutton(
            label='Monokai',
            image=self.monokai_image,
            compound=LEFT,
            command=lambda: formatting.change_theme('orange', 'white', self.text_area)
        )

        # Add Home option to File menu
        file_menu.add_separator()
        file_menu.add_command(
            label='Home',
            accelerator='Ctrl+H',
            image=self.home_image,
            compound=LEFT,
            command=self.go_to_home
        )

    def create_toolbar(self):
        # Use Label instead of Frame to match original
        self.tool_bar = Label(self.root)
        self.tool_bar.pack(side=tk.TOP, fill=tk.X)

        # Font selector
        font_families = font.families()
        self.font_var = tk.StringVar()
        font_combo = Combobox(
            self.tool_bar,
            width=30,
            values=font_families,
            state='readonly',
            textvariable=self.font_var
        )
        # Set default font to Consolas
        try:
            default_index = font_families.index('Consolas')
            font_combo.current(default_index)
        except ValueError:
            font_combo.current(0)
        font_combo.grid(row=0, column=0, padx=5)
        font_combo.bind('<<ComboboxSelected>>',
                        lambda e: formatting.font_style(self.font_var.get(), self.font_size, self.text_area))

        # Font size selector
        self.size_var = tk.IntVar()
        size_combo = Combobox(
            self.tool_bar,
            width=14,
            textvariable=self.size_var,
            state='readonly',
            values=tuple(range(8, 81))
        )
        size_combo.current(4)  # Default to 12 (index 4: 8,9,10,11,12)
        size_combo.grid(row=0, column=1, padx=5)
        size_combo.bind('<<ComboboxSelected>>',
                        lambda e: formatting.font_size(self.font_style, self.size_var.get(), self.text_area))

        # Formatting buttons with images
        bold_btn = Button(self.tool_bar, image=self.bold_image,
                          command=lambda: formatting.bold_text(self.font_style, self.font_size, self.text_area))
        bold_btn.grid(row=0, column=2, padx=5)

        italic_btn = Button(self.tool_bar, image=self.italic_image,
                            command=lambda: formatting.italic_text(self.font_style, self.font_size, self.text_area))
        italic_btn.grid(row=0, column=3, padx=5)

        underline_btn = Button(self.tool_bar, image=self.underline_image,
                               command=lambda: formatting.underline_text(self.font_style, self.font_size,
                                                                         self.text_area))
        underline_btn.grid(row=0, column=4, padx=5)

        font_color_btn = Button(self.tool_bar, image=self.font_color_image,
                                command=lambda: formatting.color_select(self.text_area))
        font_color_btn.grid(row=0, column=5, padx=5)

        left_align_btn = Button(self.tool_bar, image=self.left_align_image,
                                command=lambda: formatting.align_left(self.text_area))
        left_align_btn.grid(row=0, column=6, padx=5)

        center_align_btn = Button(self.tool_bar, image=self.center_align_image,
                                  command=lambda: formatting.align_center(self.text_area))
        center_align_btn.grid(row=0, column=7, padx=5)

        right_align_btn = Button(self.tool_bar, image=self.right_align_image,
                                 command=lambda: formatting.align_right(self.text_area))
        right_align_btn.grid(row=0, column=8, padx=5)

        # Home button
        home_btn = Button(self.tool_bar, image=self.home_image,
                          command=self.go_to_home)
        home_btn.grid(row=0, column=9, padx=5)

        # NEW PASSWORD INPUT
        # Password label
        ttk.Label(self.tool_bar, text="Password:").grid(row=0, column=10, padx=(20, 5))

        # Password entry (shows * for characters)
        self.password_entry = ttk.Entry(
            self.tool_bar,
            textvariable=self.password_var,
            show="*",  # Masks input with asterisks
            width=15
        )
        self.password_entry.grid(row=0, column=11, padx=5)

        # Reveal/hide toggle button
        self.show_password = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            self.tool_bar,
            text="👁️",
            command=self.toggle_password_visibility,
            variable=self.show_password
        ).grid(row=0, column=12, padx=5)

    def create_text_area(self):
        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            self.root,
            yscrollcommand=self.scrollbar.set,
            font=(self.font_style, self.font_size),
            undo=True
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_area.yview)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text='Status Bar')
        self.status_bar.pack(side=tk.BOTTOM)
        self.text_area.bind('<<Modified>>',
                            lambda e: utilities.statusBarFunction(e, self.text_area, self.status_bar))

    def toggle_toolbar(self):
        if self.show_toolbar.get():
            self.tool_bar.pack(side=tk.TOP, fill=tk.X)
        else:
            self.tool_bar.pack_forget()

    def toggle_statusbar(self):
        if self.show_statusbar.get():
            self.status_bar.pack(side=tk.BOTTOM)
        else:
            self.status_bar.pack_forget()

    def setup_bindings(self):
        self.root.bind("<Control-o>", lambda e: file_operations.open_file(self.text_area, self))
        self.root.bind("<Control-n>", lambda e: file_operations.new_file(self.text_area, self))
        self.root.bind("<Control-s>", lambda e: file_operations.save_file(self.text_area, self))
        self.root.bind("<Control-Alt-s>", lambda e: file_operations.saveas_file(self.text_area, self))
        self.root.bind("<Control-q>", lambda e: file_operations.iexit(self.text_area, self.root, self))
        self.root.bind("<Control-p>", lambda e: utilities.printout(self.text_area))
        self.root.bind("<Control-d>", lambda e: utilities.date_time(self.text_area))
        self.root.bind("<Control-h>", lambda e: self.go_to_home())  # Add keyboard shortcut

    def go_to_home(self):
        """Return to the homepage application"""
        try:
            # three levels up from gui.py → your project root
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

            # point this at whatever your actual homepage file is,
            # e.g. HomePage.py or pwndatxtMain.py
            homepage_path = os.path.join(project_root, "HomePage.py")

            # if we can’t find it, show an error and bail out
            if not os.path.exists(homepage_path):
                messagebox.showerror("Error", "Homepage application not found!")
                return  # <-- only return on error

            # otherwise, close this window and launch the homepage
            self.root.destroy()
            subprocess.Popen([sys.executable, homepage_path])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return to homepage: {e}")

    def toggle_password_visibility(self):
        """Toggle between showing password text and asterisks"""
        if self.show_password.get():
            self.password_entry.config(show="")  # Show plain text
        else:
            self.password_entry.config(show="*")  # Show asterisks

    def run(self):
        self.root.mainloop()