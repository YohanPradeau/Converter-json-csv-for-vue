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
argparser.add_argument("source",  nargs='?', type=str, help="The source language (only used when you want to json to csv)" ,default="no_path")
argparser.add_argument("target", type=str, help="The file to convert")

args = argparser.parse_args()
path = os.path.dirname(__file__)
fullpathTarget = os.path.join(os.path.dirname(__file__), args.target)
fileTarget = args.target
if args.source != "no_path" :
    fullpathSource = os.path.join(os.path.dirname(__file__), args.source)
    fileSource = args.source

filename = os.path.basename(args.target)
type = fileTarget[fileTarget.rfind('.') + 1::]


def csv_to_json(): #Function for the csv to json conversion
    try:
        # READING JSON file
        data = {}
        with open(fullpathTarget, encoding='utf-8') as f:
            csv_dict_reader = csv.DictReader(f)
            for row in csv_dict_reader:
                data[row['Parent (do not edit)']] = row["Translation"]
            data = unflatten(data,'.')

        f.close()

        out_file = open(outputPath, "w", encoding='utf-8')
        json.dump(data, out_file, indent=4, ensure_ascii=False)
        out_file.close()
        
        print("Done ! \nYou can check the file at the following path : "+ outputPath)

    except Exception as e:
        print("Error : "+type(e))

def json_to_csv(): #Function for the json to csv conversion
    try:
        with open(fullpathSource,"r",encoding="utf-8") as f:
            fileSource = pandas.json_normalize(json.loads(f.read()))
        with open(fullpathTarget,"r",encoding="utf-8") as f:
            fileTarget = pandas.json_normalize(json.loads(f.read()))
        df = pandas.concat([fileTarget, fileSource], ignore_index=True)

        with open(path+"\convertedFiles\\"+filename+".csv", 'w', encoding="utf-8", newline='') as output:
            csvwriter = csv.writer(output)
            fr = ["Parent (do not edit)", "Source language" ,"Translation"]
            csvwriter.writerow(fr)

            pandas.set_option("display.max_rows", None, "display.max_columns", None)
            for elem in df:
                row = []
                parent = elem
                # print(df[elem])
                src = df[elem][1]
                tl = df[elem][0]
                row.append(parent)
                row.append(src)
                row.append(tl)
                csvwriter.writerow(row)
        print("Done ! \nYou can check the file at the following path : "+ path+"\convertedFiles\\"+filename+".csv")

            
    except Exception as e: print(repr(e))

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
    if args.source != "no_path":
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
        print("Source language argument is needed for the json -> csv operation.")
    
else:
    print("Only CSV and JSON file type are accepted.")
    sys.exit(1)