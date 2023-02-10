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
    Severity = str(bs_data.Severity.string)
    Leftstatement_dic[Study_id] = [Leftstatement_list, Severity]    # Creat a dictionary
    
Tools.print_type(Leftstatement_dic)

print("--------------------------------")



for ids, report in Leftstatement_dic.items():   # report: [Leftstatement list, severity]
    leftstatement_list = report[0]
    ST_count = 0
    VPC_count = 0
    APC_count = 0
    JPC_count = 0
    VF_count = 0
    LBBB_count = 0
    RBBB_count = 0
    firstAVB_count = 0
    secondtype1AVB_count = 0
    secondtype2AVB_count = 0
    LVH_count = 0
    RVH_count = 0
    STelevation_count = 0
    STdepression_count = 0
    LongQT_count = 0
    SB_count = 0
    for element in leftstatement_list:
        ST_count += element.count("SINUS TACHYCARDIA")
        VPC_count += element.count("VENTRICULAR PREMATURE COMPLEX")
        APC_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        JPC_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        VF_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        LBBB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        RBBB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        firstAVB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        secondtype1AVB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        secondtype2AVB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        LVH_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        RVH_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        STelevation_count += element.count("ST ELEVATION")
        STdepression_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        LongQT_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
        SB_count += element.count("VENTRICULAR PREMATURE COMPLEXES")
    print(f"The ID is {ids}. The status is {Severity}. The VPC number is {VPC_count}. The ST number is {ST_count}")
    # write in the CSV file
        


# 輸出成檔案