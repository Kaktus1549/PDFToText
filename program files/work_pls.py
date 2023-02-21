try:
    pass
except:
        error_file = "error_log_" + str(e) + ".txt"        
        e = e + 1
        print("An error appeared while reading the image: " + photos[0])
        print("Moving photo into error file...")
        shutil.move(photos_for_scan + "\\" + photos[0], error_photos)
        print("Creating error log...")
        with open(os.path.join(error_log, error_file ), 'w') as err:
            err.write('Image name: ' + photos[0]) 
            #if traceback.print_exc != None:
                #err.write('Error: \n' + traceback.print_exc())
        photos.pop(0)