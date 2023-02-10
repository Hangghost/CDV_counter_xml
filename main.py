import os
import glob
from bs4 import BeautifulSoup
import Tools


# 讀取所有檔案

Chimei_ECG_file = os.listdir(".\\test data")  # get list of dir path

xml_filename_list = []
for xml_filename in glob.glob("./test data/**/*.xml", recursive=True):
    xml_filename_list.append(xml_filename)    # Get all xml files path in list


Leftstatement_dic = {}

for filename in xml_filename_list:
    with open(filename, "r", encoding="UTF-16") as file:   # iterate all files
        data = file.read()
    bs_data = BeautifulSoup(data, "xml")
    Leftstatement = bs_data.find_all("Leftstatement")   # Put all the tag in the list 
    Leftstatement_list = []
    for element in Leftstatement:
        Leftstatement_list.append(str(element))
    Study_id = str(bs_data.StudyUID.string)
    Leftstatement_dic[Study_id] = Leftstatement_list    # Creat a dictionary
    
Tools.print_type(Leftstatement_dic)

print("--------------------------------")

for id, leftstatement_list in Leftstatement_dic.items():
    for element in leftstatement_list:
        count = element.count("VENTRICULAR PREMATURE COMPLEXES")
        print(f"The ID is {id}. The count is {count}")
        


# 輸出成檔案