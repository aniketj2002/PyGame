from PIL import Image
import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

i=0
for a in files:
    if a.endswith('.png'):
        # Opens a image in RGB mode
        im = Image.open(a)
        
        # Size of the image in pixels (size of original image)
        # (This is not mandatory)
        width, height = im.size
        
        # Setting the points for cropped image
        left = 0
        top = 0
        right = 700
        bottom = 500
        
        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))
        
        # Shows the image in image viewer
        im1.save(a)