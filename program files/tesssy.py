import shutil
import os
from pytesseract import *
from PIL import *
from sys import platform
import traceback
from PIL import Image

pytesseract.tesseract_cmd = r''

image = os.getcwd() + "/Photos_for_scan/207-OZP-back-old.gif"
text = pytesseract.image_to_string(image)
print(text)