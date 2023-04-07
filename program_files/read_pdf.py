import PyPDF2
import os 
import csv
#####config
outputfile="output.csv"

header_text="Date,Price"

def write_to_csv(file_path, addthis):
    new_row_list = addthis.split(',')
    with open(file_path, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row == new_row_list:
                print("Duplicate row found. Skipping.")
                return
    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(new_row_list)


def add_header_to_empty_csv():
    program_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(program_dir, '..', 'Output',outputfile)

    is_empty = os.stat(file_path).st_size == 0
    if is_empty:
        with open(file_path, mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header_text.split(','))
    return file_path
            
def get_pdf_files_path():
    program_dir = os.path.dirname(os.path.abspath(__file__))
    scanned_dir = os.path.join(program_dir, '..', 'Photos_for_scan')
    pdf_files = []
    for file in os.listdir(scanned_dir):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(scanned_dir, file)
            pdf_files.append(pdf_path)
    return pdf_files

def load_data(path):
    path=path
    reader = PyPDF2.PdfReader(path)
    ToBeparse=reader.pages[0].extract_text()
    separted_data =ToBeparse=reader.pages[0].extract_text().split('\n')
    #print(separted_data)
    return separted_data


def checker(items):
    date=""
    shoes=""
    entry_fee=""
    price_sum=0
    for i, item in enumerate(items):
        if "Datum" in item:
            if i+1 < len(items):
                date = items[i+1]
        elif "Rozpis přijatých plateb" in item:
            if i-1 < len(items):
                price_sum =items[i-1]
                price_sum=price_sum[:-3]
      
        elif "Lezečky - příplatek vstup" in item:
            if i+1 < len(items):
                shoes =items[i+1]
        elif "Vstupné" in item:
            if i+1 < len(items):
                entry_fee =items[i+1]

    output=date+","+price_sum
    return output
    
csv_path=add_header_to_empty_csv()
i=0
paths = get_pdf_files_path()
while i+1 <= len(paths):
    content =checker(load_data(paths[i]))
    write_to_csv(csv_path,content)
    i=i+1
