import os
import glob
import time

import img2pdf
import pyperclip
import pyautogui as pgui
import cv2
import numpy as np

def write_ja(japanese): 
    """Write Japanese using pyautogui
    Parameter
    ----------------
    japanese: str
        String you want to write
    Return
    ---------------
    None
    """
    pyperclip.copy(japanese)
    pgui.hotkey('ctrl', 'v')
    time.sleep(1.3)
def press(button):
    """Press the button and timesleep
    
    Parameters
    ------------------
    button: str
        button name
    
    Return
    ------------------
    None
    """
    pgui.hotkey(button)
    time.sleep(1.0)
def launch_app(name_app):
    """Launch an application for Windows
    Parameter
    ----------------
    name_app: str
        Name of the application
    Return
    ----------------
    None
    """
    pgui.click(x=105, y=1070) #depending on your pc
    time.sleep(0.5)
    write_ja(name_app)
    time.sleep(0.5)
    press("enter")

def image2pdf(pdf_path, image_dir):
    """Change image into pdf
    
    Parameters
    ---------------------
    pdf_path: str
       path of pdf
    image_dir: str
       directory of image files
    
    Return
    --------------------
    None
    """
    files = os.listdir(image_dir)
    image_files = [os.path.join(image_dir,f) for f in files]
    #make pdf
    with open(pdf_path, "wb") as f:
        f.write(img2pdf.convert(image_files))

def kindle2pdf(book_name, way):
    """Change kindle into pdf
    
    Parameters
    -------------------
    book_name: str
        use for the names of pdf folder and image files
    way: str
        "left" or "right"
    
    Return
    -------------------
    None
    """
    # ready for pdf path, iamge directory and region of screenshot
    pdf_path = "../kindle/pdf_book/" + book_name + ".pdf"
    image_dir = "../kindle/image/" + book_name + "/"
    os.makedirs(image_dir, exist_ok=True)
    x, y, width, height = 700, 145, 600, 815 #depending on your pc
    # launch kindle
    launch_app("kindle")
    time.sleep(5.0)
    # position for click
    if way == "left":
        x1, y1 = 95, 615 #depending on your pc
    elif way == "right":
        x1, y1 = 1887, 609 #depending on your pc
    # first screenshot
    image_file_pre = image_dir + "{}_{:04d}".format(book_name, 1) + ".png"
    pgui.screenshot(image_file_pre, region=(x, y, width, height))
    image_pre = cv2.imread(image_file_pre)
    pgui.click(x1, y1)
    time.sleep(0.5)
    # second screenshot
    image_file = image_dir + "{}_{:04d}".format(book_name, 2) + ".png"
    pgui.screenshot(image_file, region=(x, y, width, height))
    image = cv2.imread(image_file)
    pgui.click(x1, y1)
    time.sleep(0.5)
    # screenshot from third page to last page
    i = 3
    while not (np.array_equal(image, image_pre)):
        # file names
        image_file_pre = image_dir + "{}_{:04d}".format(book_name, i-1) + ".png" 
        image_file = image_dir + "{}_{:04d}".format(book_name, i) + ".png"
        # screenshot
        pgui.screenshot(image_file, region=(x, y, width, height))
        # next page
        pgui.click(x1, y1)
        time.sleep(0.5)
        # read images
        image_pre = cv2.imread(image_file_pre)
        image = cv2.imread(image_file)
        i += 1
    # delete last screenshot
    os.remove(image_file)
    # make pdf
    image2pdf(pdf_path, image_dir)