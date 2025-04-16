import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("400x300")

        self.images = []
        
        self.create_widgets()
    
    def create_widgets(self):
        self.select_button = tk.Button(self.root, text="Select Images", command=self.select_images)
        self.select_button.pack(pady=20)

        self.resize_button = tk.Button(
            self.root, text="Resize to 600x600 (Fit & Pad, Save as WebP)", 
            state=tk.DISABLED, command=self.resize_images
        )
        self.resize_button.pack(pady=20)

        self.image_list_label = tk.Label(self.root, text="Selected Images will appear here.", wraplength=380)
        self.image_list_label.pack(pady=10)
    
    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Images", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp;*.avif")]
        )
        
        if file_paths:
            self.images = file_paths
            self.update_image_list_label()
            self.resize_button.config(state=tk.NORMAL)
        else:
            messagebox.showwarning("No files selected", "Please select at least one image.")
    
    def update_image_list_label(self):
        file_names = "\n".join([os.path.basename(file) for file in self.images])
        self.image_list_label.config(text=f"Selected Images:\n{file_names}")
    
    def resize_images(self):
        target_size = (600, 600)

        for image_path in self.images:
            try:
                with Image.open(image_path) as img:
                    # Convert image to RGBA to properly handle transparency
                    img = img.convert("RGBA")

                    # Calculate new dimensions while maintaining aspect ratio
                    img_ratio = img.width / img.height
                    target_ratio = target_size[0] / target_size[1]

                    if img_ratio > target_ratio:
                        new_width = target_size[0]
                        new_height = int(target_size[0] / img_ratio)
                    else:
                        new_height = target_size[1]
                        new_width = int(target_size[1] * img_ratio)

                    img = img.resize((new_width, new_height), Image.LANCZOS)

                    # Create a white background image
                    new_img = Image.new("RGBA", target_size, (255, 255, 255, 255))

                    # Paste the resized image onto the white background using alpha transparency
                    new_img.paste(img, ((target_size[0] - new_width) // 2, (target_size[1] - new_height) // 2), img)

                    # Convert back to RGB to remove alpha channel and ensure a white background
                    new_img = new_img.convert("RGB")

                    # Save as WebP
                    new_path = os.path.splitext(image_path)[0] + ".webp"
                    new_img.save(new_path, "WEBP", quality=95)

                    print(f"Resized and saved as WebP: {new_path}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to resize {image_path}: {e}")
                return

        messagebox.showinfo("Success", "All images resized to 600x600 with a white background and saved as WebP.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
