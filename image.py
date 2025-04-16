from PIL import Image
import IPython.display as display

# Open and display the image
image_path = 'C:\Users\Franz Tyrone\Downloads\test\image.jpg'
img = Image.open(image_path)
display.display(img)