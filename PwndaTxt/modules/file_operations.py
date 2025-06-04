import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from processors.FileDecryptor import Decryptor
from utlities.Utf8Utils import Utf8Utils



def new_file(text_area, app):
    app.url = ''
    text_area.delete(1.0, tk.END)


def open_file(text_area, app):
    url = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title='Select File',
        filetypes=(('Text File', '*.txt'), ('All Files', '*.*'))
    )
    if not url:
        return

    # Convert to absolute path immediately
    url = os.path.abspath(url)
    app.url = url
    text_area.delete(1.0, tk.END)

    password = app.password_var.get()
   #print(password)

    if not password:
        # Show encrypted content with warning
        try:
            with open(url, 'r', encoding='utf-8') as file:
                text_area.insert(1.0, file.read())
            messagebox.showwarning(
                "No Password",
                "File is encrypted. Please enter password to decrypt."
            )
        except Exception as e:
            messagebox.showerror("Read Error", f"Failed to read file: {str(e)}")
        return

    try:
        # Convert password to UTF-8 code points
        utf8_values = Utf8Utils.convert_to_code_point_list(password)

        # Create decryptor with password
        decryptor = Decryptor(utf8_values)

        # Create temporary output file with absolute path
        temp_dir = os.path.abspath(tempfile.gettempdir())
        temp_path = os.path.join(temp_dir, f"pwnda_decrypted_{os.getpid()}.txt")

        # Decrypt file to temporary location
        decryptor.process_file(url, temp_path)

        # Read decrypted content from temp file
        with open(temp_path, 'r', encoding='utf-8') as decrypted_file:
            decrypted_content = decrypted_file.read()

        # Insert decrypted content into text area
        text_area.insert(1.0, decrypted_content)

        # Clean up temporary file
        os.unlink(temp_path)

    except Exception as e:
        # Log detailed error
        error_msg = f"Decryption failed: {str(e)}"
        if hasattr(e, 'args') and e.args:
            error_msg += f"\nDetails: {e.args[0]}"
        messagebox.showerror("Decryption Error", error_msg)

        # Fallback to showing encrypted content
        try:
            with open(url, 'r', encoding='utf-8') as file:
                text_area.insert(1.0, file.read())
        except Exception as e:
            messagebox.showerror("Read Error", f"Failed to read file: {str(e)}")

    app.root.title(f"{os.path.basename(url)} [Decrypted]")


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