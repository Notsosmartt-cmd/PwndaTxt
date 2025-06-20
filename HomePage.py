# ─── HomePage.py ──
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("PwndaApps Home")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 14), foreground='#7f8c8d')
        style.configure('App.TButton', font=('Arial', 12), padding=10)
        style.configure('Footer.TLabel', font=('Arial', 10), foreground='#95a5a6')

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        header = ttk.Label(main_frame, text="PwndaTxt", style='Title.TLabel')
        header.pack(pady=(10, 5))

        subtitle = ttk.Label(
            main_frame,
            text="Select an application to launch",
            style='Subtitle.TLabel'
        )
        subtitle.pack(pady=(0, 20))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)

        # ─── Text Editor Button ───
        editor_btn = ttk.Button(
            button_frame,
            text="Text Editor",
            style='App.TButton',
            command=self.launch_editor
        )
        editor_btn.pack(fill=tk.X, pady=5)

        # ─── Encryption App Button ───
        encryption_btn = ttk.Button(
            button_frame,
            text="Encryption Tool",
            style='App.TButton',
            command=self.launch_encryption
        )
        encryption_btn.pack(fill=tk.X, pady=5)

        # ─── Exit Button ───
        exit_btn = ttk.Button(
            button_frame,
            text="Exit",
            style='App.TButton',
            command=self.root.destroy
        )
        exit_btn.pack(fill=tk.X, pady=5)

        footer = ttk.Label(main_frame, text="© 2023 PwndaApps", style='Footer.TLabel')
        footer.pack(side=tk.BOTTOM, pady=10)

    def launch_editor(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            editor_dir = os.path.join(base_dir, "PwndaTxt")
            editor_file = os.path.join(editor_dir, "pwndatxtMain.py")

            if not os.path.exists(editor_file):
                messagebox.showerror("Error", "Editor not found!")
                return

            # FIX: Capture output for debugging
            with open(os.path.join(editor_dir, "editor_log.txt"), "w") as log_file:
                self.root.destroy()
                subprocess.Popen(
                    [sys.executable, editor_file],
                    cwd=editor_dir,
                    stdout=log_file,
                    stderr=log_file
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch editor: {e}")

    def launch_encryption(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            encryptor_dir = os.path.join(base_dir, "PwndaLitePython")  # FIXED: Corrected variable name
            encryptor_path = os.path.join(encryptor_dir, "PwndaLite.py")

            if not os.path.exists(encryptor_path):
                messagebox.showerror(
                    "Error",
                    f"Encryption tool not found at:\n{encryptor_path}"
                )
                return

            # FIX: Set working directory and capture output
            with open(os.path.join(encryptor_dir, "encryptor_log.txt"), "w") as log_file:
                self.root.destroy()
                subprocess.Popen(
                    [sys.executable, encryptor_path],
                    cwd=encryptor_dir,  # FIXED: Set working directory
                    stdout=log_file,
                    stderr=log_file
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch encryption tool: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomePage(root)
    root.mainloop()