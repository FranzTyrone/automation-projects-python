import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os
import re

# Function to format and rename files in the selected folder
def format_and_rename_files():
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        messagebox.showwarning("No Folder Selected", "Please select a folder to proceed.")
        return
    
    files = os.listdir(folder_selected)
    renamed_files = []
    
    for file in files:
        # Skip directories
        if os.path.isdir(os.path.join(folder_selected, file)):
            continue
        
        # Split filename and extension
        name, ext = os.path.splitext(file)

        # Process name: Replace non-alphanumeric separators with spaces, then split into words
        words = re.split(r'[\s\-_]+', name)

        # Rejoin with hyphens and convert to uppercase
        formatted_name = "-".join(words).upper()

        # Ensure numbers stay together with adjacent letters (e.g., 16OZ1990636 → 16OZ-1990636)
        formatted_name = re.sub(r'([A-Z]+)(\d+)', r'\1-\2', formatted_name)

        # Construct new file path
        old_path = os.path.join(folder_selected, file)
        new_path = os.path.join(folder_selected, formatted_name + ext)
        
        # Avoid overwriting existing files
        if os.path.exists(new_path):
            messagebox.showwarning("File Exists", f"Skipping {file}, renamed file already exists.")
            continue
        
        # Rename file
        try:
            os.rename(old_path, new_path)
            renamed_files.append(formatted_name + ext)
        except Exception as e:
            messagebox.showerror("Error Renaming File", f"Could not rename {file}: {e}")

    # Update output box with renamed files
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, "\n".join(renamed_files))
    output_box.config(state=tk.DISABLED)
    
    messagebox.showinfo("Renaming Complete", "Files have been renamed successfully.")

# Setup the GUI
root = tk.Tk()
root.title("Hyphen Formatter and Renamer")
root.geometry("600x450")

# Instructions Label
input_label = tk.Label(root, text="Select a folder to auto-rename files:")
input_label.pack(pady=5)

# Folder Selection and Rename Button
folder_button = tk.Button(root, text="Select Folder and Rename", command=format_and_rename_files)
folder_button.pack(pady=10)

# Output Box
output_label = tk.Label(root, text="Renamed Files:")
output_label.pack(pady=5)
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15, state=tk.DISABLED)
output_box.pack(padx=10, pady=5)

root.mainloop()
