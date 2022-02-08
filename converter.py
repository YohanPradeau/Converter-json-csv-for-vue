import json
import argparse
import csv
import os
import sys
from xml.dom import minidom
from io import BytesIO
from pathlib import Path
import pandas
from flatten_json import unflatten

#Arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("file", type=str, help="The file to convert")

args = argparser.parse_args()
path = os.path.dirname(__file__)
fullpath = os.path.join(os.path.dirname(__file__), args.file)
file = args.file
filename = os.path.basename(args.file)
type = file[file.rfind('.') + 1::]


def csv_to_json(): #Function for the csv to json conversion
    try:
        # READING JSON FILE
        data = {}
        with open(fullpath, encoding='utf-8') as f:
            csv_dict_reader = csv.DictReader(f)
            for row in csv_dict_reader:
                # print(row['Parent (do not edit)']+"."+row["Translation"])
                data[row['Parent (do not edit)']] = row["Translation"]
            data = unflatten(data,'.')

        f.close()

        out_file = open(outputPath, "w", encoding='utf-8')
        json.dump(data, out_file, indent=4, ensure_ascii=False)
        out_file.close()
        
        print("Done ! \nYou can check the file at the following path : "+ outputPath)

    except Exception:
        print("Error : "+Exception)

def json_to_csv(): #Function for the json to csv conversion
    try:
        with open(fullpath,"r",encoding="utf-8") as f:
            file = json.load(f)
        print(fullpath)
        with open(path+"\convertedFiles\\"+filename+".csv", 'w', encoding="utf-8", newline='') as output:
            csvwriter = csv.writer(output)
            fr = ["Parent (do not edit)", "Translation"]
            csvwriter.writerow(fr)

            df = pandas.json_normalize(file)
            for elem in df:
                row = []
                parent = elem
                tl = df[elem][0]
                row.append(parent)
                row.append(tl)
                csvwriter.writerow(row)
        print("Done ! \nYou can check the file at the following path : "+ path+"\convertedFiles\\"+filename+".csv")

            
    except Exception:
        print("File not found : "+fullpath)

#Prepare the folder for converted files
Path("./convertedFiles").mkdir(parents=True, exist_ok=True)


if type == "csv":
    outputPath=path+"\convertedFiles\\"+filename[:-4]
    fileExist = Path(outputPath).is_file()
    if fileExist:
        print("There is already a file at the output location with this exact same name and path ("+path+"\convertedFiles\\"+filename[:-4]+")")
        reply = str(input("Are you sure you wish to OVERWRITE it ? "+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            # print("TODO")
            csv_to_json()
        elif reply[0] == 'n':
            print("Task canceled")
        else:
            print('Invalid input, task canceled.\nPlease be sure to answer with "y" or "n"')
    else:
        csv_to_json()
elif type == "json":
    outputPath=path+"\convertedFiles\\"+filename+".csv"
    fileExist = Path(outputPath).is_file()
    if fileExist:
        print("There is already a file at the output location with this exact same name and path ("+path+"\convertedFiles\\"+filename[:-4]+")")
        reply = str(input("Are you sure you wish to OVERWRITE it ? "+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            json_to_csv()
        elif reply[0] == 'n':
            print("Task canceled")
        else:
            print('Invalid input, task canceled.\nPlease be sure to answer with "y" or "n"')
    else:
        json_to_csv()
    
else:
    print("Only CSV and JSON file type are accepted.")
    sys.exit(1)