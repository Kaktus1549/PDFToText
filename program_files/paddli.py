from asyncio.log import logger
from paddleocr import PaddleOCR
from sys import platform
import os
import shutil
import logging

#creating objects for OCR 
ocr = PaddleOCR(use_angle_cls=True, lang='en')

#error handling
error_logger = logging.getLogger('Error_logger')
logger.setLevel(logging.ERROR)
logging.basicConfig(level=logging.DEBUG, format='\nTime: %(asctime)s \nType of event: %(levelname)s \nError message: %(message)s')



x = 0
second_x = 0

#getting platform info
current_platform = platform.lower()
if current_platform == "windows" or current_platform == 'win32' or current_platform == 'win64':
    file_separrator = "\\"
else:
    file_separrator = "/"


error_log = os.getcwd() + file_separrator + 'Error_log'
error_photos = os.getcwd() + file_separrator + 'Errors'
fontik = os.getcwd() + file_separrator + 'Font'
output = os.getcwd() + file_separrator + 'Output'
photos_for_scan = os.getcwd() + file_separrator + 'Photos_for_scan'
scanned = os.getcwd() + file_separrator + 'Scaned'
prefixs = os.getcwd() + file_separrator + 'prefixs' + file_separrator 



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
        try:
            imagee = photos_for_scan + file_separrator  + photos[0]
            result = ocr.ocr(imagee)
            
            #PaddleOCR output has a lot of unnecessary information stored in multipel tuples in tuples
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
                            
                #after scan, picutre is moved into 'Scaned' folder            
                print("Successfuly scanned and moved photo: " + photos[0])
                shutil.move(photos_for_scan + file_separrator + photos[0], scanned)
                photos.pop(0)

        except Exception as error:
            #getting name of error output
            error_file = "error_log_" + str(e) + ".log"        
            e = e + 1

            #telling user something went wrong
            print("An error appeared while reading the image: " + photos[0])
            print("Moving photo into error file...")
            
            #moving picture into 'Errors' folder, so he can later rescan it
            shutil.move(photos_for_scan + file_separrator + photos[0], error_photos)
            
            #creating error log
            print("Creating error log...")
            
            with open(os.path.join(error_log, error_file ), 'w') as err:
                err.write('Image name: ' + photos[0]) 
                err.write('\nError log: ')
            
            file_handler = logging.FileHandler(error_log + file_separrator + error_file )
            logger.addHandler(file_handler)
            formatter = logging.Formatter('\n\n    Time: %(asctime)s \n    Logger Name: %(name)s \n    Logger type: %(levelname)s \n    Error message: %(message)s')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.ERROR)
            logger.error(str(error))
            
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