import os
import tempfile
import tkinter as tk
from tkinter import filedialog, messagebox
from processors.FileDecryptor import Decryptor
from utlities.Utf8Utils import Utf8Utils
from processors.FileEncryptor import FileProcessor


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

        # Decrypt file directly to string
        decrypted_content = decryptor.decrypt_file_to_string(url)

        # Insert decrypted content into text area
        text_area.insert(1.0, decrypted_content)
        app.root.title(f"{os.path.basename(url)} [Decrypted]")

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
        password = app.password_var.get()

        if password:
            # Save with encryption
            if save_encrypted(content, app.url, password):
                text_area.edit_modified(False)
        else:
            # Save without encryption
            try:
                with open(app.url, 'w', encoding='utf-8') as file:
                    file.write(content)
                text_area.edit_modified(False)
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")

def save_encrypted(content, file_path, password):
    try:
        # Convert password to UTF-8 code points
        utf8_values = Utf8Utils.convert_to_code_point_list(password)

        # Encrypt the temporary file to final location
        encryptor = FileProcessor(utf8_values)
        encrypted_content = encryptor.encrypt_string(content)

        # Save encrypted content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(encrypted_content)
        return True



    except Exception as e:
        messagebox.showerror("Encryption Error", f"Failed to encrypt file: {str(e)}")
        return False


def saveas_file(text_area, app):
    url = filedialog.asksaveasfilename(
        defaultextension='.txt',
        filetypes=(('Text File', '*.txt'), ('All Files', '*.*'))
    )

    if not url:
         return

    app.url = url
    content = text_area.get(1.0, tk.END)
    password = app.password_var.get()

    if password:
        # Save with encryption
        if save_encrypted(content, url, password):
            text_area.edit_modified(False)
            app.root.title(f"{os.path.basename(url)} [Encrypted]")
    else:
        # Save without encryption
        try:
            with open(url, 'w', encoding='utf-8') as file:
                file.write(content)
            text_area.edit_modified(False)
            app.root.title(os.path.basename(url))
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file: {str(e)}")


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