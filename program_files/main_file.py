import os
import shutil
from paddleocr import PaddleOCR
import logging
from sys import platform, prefix
from asyncio.log import logger
from PaddlePaddleSource import *

ocr = PaddleOCR(use_angle_cls=True, lang='en')

#getting info about system 
current_platform = platform.lower()
if current_platform == "windows" or current_platform == 'win32' or current_platform == 'win64':
    file_separrator = "\\"
else:
    file_separrator = "/"

#getting folder location
error_log = os.getcwd() + file_separrator + 'Error_log' + file_separrator
error_photos = os.getcwd() + file_separrator + 'Errors' + file_separrator
text_output = os.getcwd() + file_separrator + 'Output' + file_separrator
photos_for_scan = os.getcwd() + file_separrator + 'Photos_for_scan' + file_separrator
photos_output = os.getcwd() + file_separrator + 'Scaned' + file_separrator
prefixs_folder = os.getcwd() + file_separrator + "prefixs" + file_separrator

i = file_prefix_loading(prefixs_folder)
e = error_file_prefix(prefixs_folder)

while True:
    ImageReading(file_separrator, photos_for_scan, photos_output, text_output, error_log, error_photos, i, e, prefixs_folder)
