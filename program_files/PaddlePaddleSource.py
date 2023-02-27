import os
import shutil
from paddleocr import PaddleOCR
import logging
from sys import platform
from asyncio.log import logger
from time import sleep

ocr = PaddleOCR(use_angle_cls=True, lang='en')

def file_prefix_loading(prefixs):
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
    return i
def prefixs_saving(prefixs, i, e):
    #saving prefixs
    with open(prefixs + 'prefix.txt', 'w') as prefi:
        prefi.write(str(i))
    with open(prefixs + 'error_prefix.txt', 'w') as error_prefi:
        error_prefi.write(str(e))
def error_file_prefix(prefixs):
    try:
        with open(prefixs + 'error_prefix.txt', 'r') as err_prefi:
            for line in err_prefi:
                e = line
                e = int(e)
    except:
        with open(prefixs + 'error_prefix.txt', 'w') as err_prefi:
            err_prefi.write("0")
            e = 0
    return e
def ImageReading(file_separrator, target_files_dir, file_output_dir, text_output, error_log, error_photos, file_index, error_index, prefixs):    
    #error handling
    error_logger = logging.getLogger('Error_logger')
    logger.setLevel(logging.ERROR)

    photos = os.listdir(target_files_dir)
    file_index = file_index + 1
    file = "Content_" + str(file_index) + ".txt" 

    if photos:
        try:
            imagee = target_files_dir + file_separrator  + photos[0]
            result = ocr.ocr(imagee)

            x = 0
            second_x = 0
            third_x = 0
            #PaddleOCR output has a lot of unnecessary information stored in multipel tuples in tuples
            with open(os.path.join(text_output, file), 'w') as save:
                for line in result:
                    for id in result:
                        for yes in id:     
                            for help in yes:
                                for gay in yes:
                                    x = x +1
                                    if not x%2:
                                        for final_string in gay:
                                            second_x = second_x + 1
                                            if second_x % 2:
                                                third_x = third_x + 1
                                                if third_x%2:
                                                    save.write(final_string + "\n")
                            
                #after scan, picutre is moved into 'Scaned' folder            
                print("Successfuly scanned and moved photo: " + photos[0])
                shutil.move(target_files_dir + file_separrator + photos[0], file_output_dir)
                photos.pop(0)

        except Exception as error:
            #getting name of error output
            error_index = error_index + 1
            error_file = "error_log_" + str(error_index) + ".log"        
            

            #telling user something went wrong
            print("An error appeared while reading the image: " + photos[0])
            print("Moving photo into error file...")
            
            #moving picture into 'Errors' folder, so he can later rescan it
            shutil.move(target_files_dir + file_separrator + photos[0], error_photos)
            
            #creating error log
            print("Creating error log...")
            
            with open(os.path.join(error_log, error_file ), 'w') as err:
                err.write('Image name: ' + photos[0]) 
            
            file_handler = logging.FileHandler(error_log + file_separrator + error_file )
            logger.addHandler(file_handler)
            formatter = logging.Formatter('\n\nTime: %(asctime)s \nFile name: %(filename)s \nLine number: %(lineno)s \nError message: \n')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.ERROR)
            logger.error(str(error), exc_info=True)
            
            photos.pop(0)

    if not photos:
        print("No photos for scan")
        prefixs_saving(prefixs, file_index, error_index)
        sleep(5)
