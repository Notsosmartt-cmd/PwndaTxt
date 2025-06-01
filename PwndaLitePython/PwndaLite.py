import subprocess
import sys
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import zipfile
import shutil

# Updated imports
from processors.FileEncryptor import FileProcessor
from processors.FileDecryptor import Decryptor  # Add Decryptor import
from utlities.Utf8Utils import Utf8Utils


class LiteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaussian Random Number Generator")
        self.root.geometry("600x550")  # Increased height for new button

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

        # Process buttons
        button_frame = tk.Frame(root)
        button_frame.place(x=50, y=180, width=500, height=40)

        self.encrypt_btn = tk.Button(button_frame, text="Encrypt", command=self.process_files)
        self.encrypt_btn.pack(side=tk.LEFT, padx=5)

        self.decrypt_btn = tk.Button(button_frame, text="Decrypt", command=self.decrypt_files)
        self.decrypt_btn.pack(side=tk.LEFT, padx=5)

        # Initialize state
        self.toggle_password_source()
        self.input_path = None
        self.is_directory = False
        self.password_file_path = None

        # Home button
        self.home_btn = tk.Button(root, text="🏠 Home", command=self.go_to_home)
        self.home_btn.place(x=400, y=230)

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

    def get_password(self):
        """Get password from either manual entry or file"""
        if self.password_source.get() == "manual":
            password = self.password_entry.get()
            if not password:
                messagebox.showerror("Error", "Please enter a password")
                return None
            return password
        else:
            if not self.password_file_path:
                messagebox.showerror("Error", "Please select a password file")
                return None
            try:
                with open(self.password_file_path, 'r') as f:
                    password = f.read().strip()
                if not password:
                    messagebox.showerror("Error", "Password file is empty")
                    return None
                return password
            except Exception as e:
                messagebox.showerror("Error", f"Error reading password file: {str(e)}")
                return None

    def process_files(self):
        """Encrypt files using FileEncryptor"""
        if not self.input_path:
            messagebox.showerror("Error", "Please select an input file or directory")
            return

        password = self.get_password()
        if password is None:
            return

        try:
            # Convert password to UTF-8 code points
            utf8_code_points = Utf8Utils.convert_to_code_point_list(password)

            # Create encryptor with code points
            encryptor = FileProcessor(utf8_code_points)

            if self.is_directory:
                for file in os.listdir(self.input_path):
                    if file.endswith(".txt"):
                        input_file = os.path.join(self.input_path, file)
                        output_file = os.path.join(self.input_path, f"(Pwnda){file}")
                        encryptor.process_file(input_file, output_file)
                messagebox.showinfo("Success", "Encryption complete for all files in directory!")
            else:
                output_file = os.path.join(os.path.dirname(self.input_path),
                                           f"(Pwnda){os.path.basename(self.input_path)}")
                encryptor.process_file(self.input_path, output_file)
                messagebox.showinfo("Success", "Encryption complete for file!")

        except Exception as e:
            messagebox.showerror("Error", f"Encryption error: {str(e)}")

    def decrypt_files(self):
        """Decrypt files using FileDecryptor"""
        if not self.input_path:
            messagebox.showerror("Error", "Please select an input file or directory")
            return

        password = self.get_password()
        if password is None:
            return

        try:
            # Convert password to UTF-8 code points
            utf8_code_points = Utf8Utils.convert_to_code_point_list(password)

            # Create decryptor with code points
            decryptor = Decryptor(utf8_code_points)

            if self.is_directory:
                for file in os.listdir(self.input_path):
                    if file.startswith("(Pwnda)") and file.endswith(".txt"):
                        input_file = os.path.join(self.input_path, file)
                        # Remove the prefix for decrypted file
                        original_name = file[len("(Pwnda)"):]
                        output_file = os.path.join(self.input_path, original_name)
                        decryptor.process_file(input_file, output_file)
                messagebox.showinfo("Success", "Decryption complete for all files in directory!")
            else:
                # For single file, remove prefix if present
                filename = os.path.basename(self.input_path)
                output_name = "(decrypted)" + filename
              #  if filename.startswith("(Pwnda)"):
             #       output_name = filename[len("(Pwnda)"):]
              #  else:
                   # output_name = "decrypted_" + filename

                output_file = os.path.join(os.path.dirname(self.input_path), output_name)
                decryptor.process_file(self.input_path, output_file)
                messagebox.showinfo("Success", "Decryption complete for file!")

        except Exception as e:
            messagebox.showerror("Error", f"Decryption error: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LiteApp(root)
    root.mainloop()