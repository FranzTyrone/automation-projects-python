import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from urllib.parse import urlparse
import os

class S3URLFormatter:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 URL Formatter")
        self.root.geometry("800x500")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="S3 URL Formatter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # S3 Base URL (editable)
        ttk.Label(main_frame, text="S3 Base URL:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.base_url_var = tk.StringVar(value="https://grandwine-product-images.s3.us-east-1.amazonaws.com/")
        self.base_url_entry = ttk.Entry(main_frame, textvariable=self.base_url_var, width=80)
        self.base_url_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Input section
        ttk.Label(main_frame, text="Image Filenames (one per line):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Input text area with scrollbar
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.input_text = tk.Text(input_frame, height=4, wrap=tk.WORD, font=("Arial", 10))
        input_scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=input_scrollbar.set)
        
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        input_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Format button
        format_btn = ttk.Button(main_frame, text="Format URLs", command=self.format_url)
        format_btn.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Output section
        ttk.Label(main_frame, text="Formatted URLs:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        
        # Output text with scrollbar
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(output_frame, height=8, wrap=tk.WORD, font=("Courier", 10))
        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Copy button
        copy_btn = ttk.Button(button_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # History section
        ttk.Label(main_frame, text="Recent URLs:", font=("Arial", 10, "bold")).grid(row=8, column=0, sticky=tk.W, pady=(20, 5))
        
        # History listbox with scrollbar
        history_frame = ttk.Frame(main_frame)
        history_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)
        
        self.history_listbox = tk.Listbox(history_frame, height=4, font=("Courier", 9))
        history_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=history_scrollbar.set)
        
        self.history_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        history_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(6, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        # Bind events
        self.input_text.bind('<Control-Return>', lambda event: self.format_url())
        self.history_listbox.bind('<Double-Button-1>', self.load_from_history)
        
        # History storage
        self.url_history = []
        
        # Focus on input
        self.input_text.focus()
    
    def format_url(self):
        input_content = self.input_text.get(1.0, tk.END).strip()
        base_url = self.base_url_var.get().strip()
        
        if not input_content:
            messagebox.showwarning("Warning", "Please enter image filenames")
            return
        
        if not base_url:
            messagebox.showwarning("Warning", "Please enter a base URL")
            return
        
        # Ensure base URL ends with /
        if not base_url.endswith('/'):
            base_url += '/'
        
        # Split input into lines and process each
        lines = input_content.split('\n')
        formatted_urls = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove surrounding quotes, commas, and other punctuation
            filename = line.strip('"\'`,;')
            
            # If it's still a URL, extract filename
            if filename.startswith('http://') or filename.startswith('https://'):
                parsed_url = urlparse(filename)
                filename = os.path.basename(parsed_url.path)
                # Also clean the extracted filename
                filename = filename.strip('"\'`,;')
                if not filename:
                    continue
            
            # Create the formatted URL
            formatted_url = base_url + filename
            formatted_urls.append(formatted_url)
            
            # Add to history
            if formatted_url not in self.url_history:
                self.url_history.insert(0, formatted_url)
        
        if not formatted_urls:
            messagebox.showerror("Error", "No valid filenames found")
            return
        
        # Display the results
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, '\n'.join(formatted_urls))
        
        # Keep only last 20 items in history
        if len(self.url_history) > 20:
            self.url_history = self.url_history[:20]
        
        # Update history display
        self.update_history_display()
        
        messagebox.showinfo("Success", f"Formatted {len(formatted_urls)} URL(s)")
    
    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for url in self.url_history:
            # Truncate long URLs for display
            display_url = url if len(url) <= 80 else url[:77] + "..."
            self.history_listbox.insert(tk.END, display_url)
    
    def load_from_history(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            selected_url = self.url_history[selection[0]]
            current_content = self.output_text.get(1.0, tk.END).strip()
            if current_content:
                self.output_text.insert(tk.END, '\n' + selected_url)
            else:
                self.output_text.insert(1.0, selected_url)
    
    def copy_to_clipboard(self):
        output_content = self.output_text.get(1.0, tk.END).strip()
        if output_content:
            try:
                pyperclip.copy(output_content)
                messagebox.showinfo("Success", "All URLs copied to clipboard!")
            except:
                # Fallback if pyperclip is not available
                self.root.clipboard_clear()
                self.root.clipboard_append(output_content)
                messagebox.showinfo("Success", "All URLs copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No URLs to copy")
    
    def clear_all(self):
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.input_text.focus()

def main():
    root = tk.Tk()
    app = S3URLFormatter(root)
    root.mainloop()

if __name__ == "__main__":
    main()