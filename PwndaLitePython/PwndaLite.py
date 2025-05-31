import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import shutil

from PwndaLitePython.FileProcessor import FileProcessor


class LiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaussian Random Number Generator")
        self.root.geometry("600x500")

        # Password source selection
        self.password_source = tk.StringVar(value="manual")
        self.manual_radio = tk.Radiobutton(root, text="Enter Password", variable=self.password_source,
                                           value="manual", command=self.toggle_password_source)
        self.file_radio = tk.Radiobutton(root, text="Load Password from File", variable=self.password_source,
                                         value="file", command=self.toggle_password_source)

        # Password input components
        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root, width=30)

        # File selection components
        self.password_file_btn = tk.Button(root, text="Select Password File", command=self.select_password_file)
        self.password_file_label = tk.Label(root, text="No password file selected")

        # Input selection components
        self.file_btn = tk.Button(root, text="Select Input File", command=self.select_input_file)
        self.dir_btn = tk.Button(root, text="Select Input Directory", command=self.select_input_dir)
        self.selected_path_label = tk.Label(root, text="No file or directory selected.")

        # Process button
        self.process_btn = tk.Button(root, text="Process", command=self.process_files)

        # Layout
        self.manual_radio.place(x=50, y=20)
        self.file_radio.place(x=200, y=20)
        self.password_label.place(x=50, y=60)
        self.password_entry.place(x=150, y=60)
        self.password_file_btn.place(x=150, y=60)
        self.password_file_label.place(x=410, y=60)
        self.file_btn.place(x=50, y=100)
        self.dir_btn.place(x=210, y=100)
        self.selected_path_label.place(x=50, y=140)
        self.process_btn.place(x=100, y=180)

        # Initialize state
        self.toggle_password_source()
        self.input_path = None
        self.is_directory = False
        self.password_file_path = None
        # Home button
        self.home_btn = tk.Button(root, text="🏠 Home", command=self.go_to_home)
        # adjust x/y to wherever you want it in the window
        self.home_btn.place(x=400, y=180)

    def go_to_home(self):
        """Close LiteApp and launch the main homepage script."""
        try:
            # two levels up from this file to the project root
            current_file = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file))
            homepage_path = os.path.join(project_root, "HomePage.py")  # adjust filename as needed

            if not os.path.exists(homepage_path):
                messagebox.showerror("Error", f"Cannot find homepage at:\n{homepage_path}")
                return

            # destroy this window
            self.root.destroy()

            # launch homepage with the same python interpreter
            subprocess.Popen([sys.executable, homepage_path])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to return home: {e}")


    def toggle_password_source(self):
        if self.password_source.get() == "manual":
            self.password_entry.place(x=150, y=60)
            self.password_file_btn.place_forget()
        else:
            self.password_entry.place_forget()
            self.password_file_btn.place(x=150, y=60)

    def select_password_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if file_path.lower().endswith('.zip'):
                try:
                    temp_dir = tempfile.mkdtemp()
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        for file in zip_ref.namelist():
                            if file.lower().endswith('.txt') and not file.endswith('/'):
                                zip_ref.extract(file, temp_dir)
                                self.password_file_path = os.path.join(temp_dir, file)
                                self.password_file_label.config(text=f"File (from zip): {os.path.basename(file)}")
                                break
                        else:
                            messagebox.showerror("Error", "No password file found in the zip")
                            self.password_file_path = None
                except Exception as e:
                    messagebox.showerror("Error", f"Error reading zip file: {str(e)}")
                    self.password_file_path = None
            else:
                self.password_file_path = file_path
                self.password_file_label.config(text=f"File: {os.path.basename(file_path)}")

    def select_input_file(self):
        self.input_path = filedialog.askopenfilename()
        if self.input_path:
            self.is_directory = False
            self.selected_path_label.config(text=f"File: {os.path.basename(self.input_path)}")

    def select_input_dir(self):
        self.input_path = filedialog.askdirectory()
        if self.input_path:
            self.is_directory = True
            self.selected_path_label.config(text=f"Directory: {os.path.basename(self.input_path)}")

    def process_files(self):
        # Validation
        if not self.input_path:
            messagebox.showerror("Error", "Please select an input file or directory")
            return

        # Get password
        password = ""
        if self.password_source.get() == "manual":
            password = self.password_entry.get()
            if not password:
                messagebox.showerror("Error", "Please enter a password")
                return
        else:
            if not self.password_file_path:
                messagebox.showerror("Error", "Please select a password file")
                return
            try:
                with open(self.password_file_path, 'r') as f:
                    password = f.read().strip()
                if not password:
                    messagebox.showerror("Error", "Password file is empty")
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Error reading password file: {str(e)}")
                return

        # Process files
        try:
            utf8_values = list(password)
            processor = FileProcessor(utf8_values)

            if self.is_directory:
                for file in os.listdir(self.input_path):
                    if file.endswith(".txt"):
                        input_file = os.path.join(self.input_path, file)
                        output_file = os.path.join(self.input_path, f"(Pwnda){file}")
                        processor.process_file(input_file, output_file)
                messagebox.showinfo("Success", "Processing complete for all files in directory!")
            else:
                output_file = os.path.join(os.path.dirname(self.input_path),
                                           f"(Pwnda){os.path.basename(self.input_path)}")
                processor.process_file(self.input_path, output_file)
                messagebox.showinfo("Success", "Processing complete for file!")

        except Exception as e:
            messagebox.showerror("Error", f"Processing error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LiteApp(root)
    root.mainloop()

