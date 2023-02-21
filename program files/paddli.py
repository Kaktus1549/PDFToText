from paddleocr import PaddleOCR
from sys import platform
import traceback
import os
import shutil
import re

ocr = PaddleOCR(use_angle_cls=True, lang='en')
x = 0
second_x = 0

#getting platform info
current_platform = platform.lower()

#file paths for windows
if current_platform == "windows" or current_platform == 'win32' or current_platform == 'win64':
    error_log = os.getcwd() + '\\Error_log'
    error_photos = os.getcwd() + '\\Errors'
    fontik = os.getcwd() + '\\Font'
    output = os.getcwd() + '\\Output'
    photos_for_scan = os.getcwd() + '\\Photos_for_scan'
    scanned = os.getcwd() + '\\Scaned'
    prefixs = os.getcwd() + '\\prefixs\\'
    
#file path for linux
if current_platform == "linux":
    error_log = os.getcwd() + '/Error_log'
    error_photos = os.getcwd() + '/Errors'
    fontik = os.getcwd() + '/Font'
    output = os.getcwd() + '/Output'
    photos_for_scan = os.getcwd() + '/Photos_for_scan'
    scanned = os.getcwd() + '/Scanned'
    prefixs = '/prefixs/'

#importing prefixs
try:
    with open(prefixs + 'prefix.txt', 'r') as prefi:
        for line in prefi:
            i = line
            i = int(i)
except:
    with open(prefixs + 'prefix.txt', 'w') as prefi:
        prefi.write("0")
        i = 0
try:
    with open(prefixs + 'error_prefix.txt', 'r') as err_prefi:
        for line in err_prefi:
            e = line
            e = int(e)
except:
    with open(prefixs + 'error_prefix.txt', 'w') as err_prefi:
        err_prefi.write("0")
        e = 0

#main loop
while True:
    photos = os.listdir(photos_for_scan)
    i = i + 1
    file = "Content_" + str(i) + ".txt" 
    if photos:
        imagee = photos_for_scan + '\\' + photos[0]
        if current_platform == "windows" or current_platform == 'win32' or current_platform == 'win64':
            result = ocr.ocr(imagee)
            with open(os.path.join(output, file), 'w') as save:
                for line in result:
                    for object in line:
                        x = x + 1
                        if not x % 2:
                            for another_object in object:
                                second_x = second_x + 1
                                if second_x %2:
                                    save.write(''.join(str(another_object)))
                                    save.write('\n')
                        
                        
            print("Successfuly scanned and moved photo: " + photos[0])
            shutil.move(photos_for_scan + '\\' + photos[0], scanned)
            photos.pop(0)
        if current_platform == "linux":
            result = ocr.ocr( imagee , det=False, cls=True)
            with open(os.path.join(output, file), 'w') as save:
                for line in result:
                    save.write(','.join(str(line)))
            print("Successfuly scanned and moved photo: " + photos[0])
            shutil.move(photos_for_scan + '/' + photos[0], scanned)
            photos.pop(0)
    if not photos:
        break
    

#ending message
print("All photos were scanned and moved!")

#saving prefixs
with open(prefixs + 'prefix.txt', 'w') as prefi:
    prefi.write(str(i))
with open(prefixs + 'error_prefix.txt', 'w') as error_prefi:
    error_prefi.write(str(e))

#end