import os
import glob
from bs4 import BeautifulSoup
import Tools



# Chimei_ECG_file = os.listdir(".\\test data")  # get list of dir path


xml_filename_list = []
for xml_filename in glob.glob("./test data/0103/**/*.xml", recursive=True):
    xml_filename_list.append(xml_filename)    # Get all xml files path in list


Leftstatement_dic = {}
error_filename = []
Study_id_error = 0
Severity_error = 0
date_error = 0

for filename in xml_filename_list:
    with open(filename, "r", encoding="UTF-16") as file:   # iterate all files
        data = file.read()
    bs_data = BeautifulSoup(data, "xml")

    Leftstatement = bs_data.find_all("Leftstatement")   # Put all the tag in the list 
    Leftstatement_list = []
    for element in Leftstatement:
        Leftstatement_list.append(str(element))

    try:    
        Study_id = str(bs_data.StudyUID.string)    # Get ID
    except (AttributeError, KeyError):
        Study_id = ""
        Study_id_error += 1
        error_filename.append(filename)
    try:
        Severity = str(bs_data.Severity.string)    # Get severity
    except (AttributeError, KeyError):
        Severity = ""        
        Severity_error += 1
        error_filename.append(filename)
    try:
        date = str(bs_data.StudyDate.string)    # Get date
    except (AttributeError, KeyError):
        date = ""        
        date_error += 1
        error_filename.append(filename)

    Leftstatement_dic[Study_id] = [Leftstatement_list, Severity, date]    # Creat a dictionary


CDV_name = ["Sinus tachycardia", "Ventriclar premature complex", "Atrial premature complex", "J premature complex", "Ventricular fibrillation", "Atrial fibrillation", "Left bundle branch block", "Right bundle branch block", "1st atrioventricular block", "2nd atrioventricular block type 1", "2nd atrioventricular block type 2", "Left ventricular hypertrophy", "Right ventricular hypertrophy", "ST elevation", "ST depression", "Long QT interval", "Sinus bradycardia", "Sinus arrhythmia"]
CDV_counting_dic = {}


for ids, report in Leftstatement_dic.items():   # report: [Leftstatement list, severity, date]
    leftstatement_list = report[0]    # Get the Leftstatement list
    Severity = report[1]
    date = report[2]

    ST_count = Tools.CDV_counter("SINUS TACHYCARDIA", leftstatement_list)
    VPC_count = Tools.CDV_counter("VENTRICULAR PREMATURE", leftstatement_list, other_name="VENT PREMATURE COMPLEXES")
    APC_count = Tools.CDV_counter("ATRIAL PREMATURE COMPLEX", leftstatement_list, other_name="MULTIPLE ATRIAL PREMATURE COMPLEXES")
    JPC_count = Tools.CDV_counter("-----", leftstatement_list)
    VF_count = Tools.CDV_counter("------", leftstatement_list)
    AF_count = Tools.CDV_counter("ATRIAL FIBRILLATION", leftstatement_list, other_name="ATRIAL FLUTTER/FIBRILLATION")
    LBBB_count = Tools.CDV_counter("LEFT BUNDLE BRANCH BLOCK", leftstatement_list)
    RBBB_count = Tools.CDV_counter("RIGHT BUNDLE BRANCH BLOCK", leftstatement_list, other_name="RBBB AND LPFB")
    firstAVB_count = Tools.CDV_counter("FIRST DEGREE AV BLOCK", leftstatement_list)
    secondtype1AVB_count = Tools.CDV_counter("------", leftstatement_list)
    secondtype2AVB_count = Tools.CDV_counter("------", leftstatement_list)
    LVH_count = Tools.CDV_counter("LEFT VENTRICULAR HYPERTROPHY", leftstatement_list, other_name="LVH WITH")
    RVH_count = Tools.CDV_counter("RIGHT VENTRICULAR HYPERTROPHY", leftstatement_list)
    STelevation_count = Tools.CDV_counter("ST ELEVATION", leftstatement_list, other_name="ST ELEV") 
    STdepression_count = Tools.CDV_counter("ST DEPRESSION", leftstatement_list)
    LongQT_count = Tools.CDV_counter("PROLONGED QT INTERVAL", leftstatement_list)
    SB_count = Tools.CDV_counter("SINUS BRADYCARDIA", leftstatement_list)
    SA_count = Tools.CDV_counter("SINUS ARRHYTHMIA", leftstatement_list)

    CDV_counting_value = [ST_count, VPC_count, APC_count, JPC_count, VF_count, AF_count, LBBB_count, RBBB_count, firstAVB_count, secondtype1AVB_count, secondtype2AVB_count, LVH_count, RVH_count, STelevation_count, STelevation_count, STdepression_count, LongQT_count, SB_count, SA_count]

    CDV_counting_nested_dic ={}
    for i in range(len(CDV_name)):
        CDV_counting_nested_dic[CDV_name[i]] = CDV_counting_value[i]
   
    CDV_counting_dic[ids] = [date, Severity, CDV_counting_nested_dic]

print("Counting finished")
print(f"Error number\n Study ID: {Study_id_error} \n Severity: {Severity_error}\n Data error: {date_error}")
for name_report in error_filename:
    print(f"The error file is: {name_report}")

new_file_name = "CDV counting data_20190103" + ".csv"
with open(new_file_name, "w") as file_object:
    file_object.write("ID" +","+ "Date" +","+ "Severity")    # Write the title
    for name in CDV_name:
        file_object.write(","+ name)
    file_object.write("\n")

    for ID, content in CDV_counting_dic.items():
        file_object.write(ID +","+ content[0] +","+ content[1])
        nested_dic = CDV_counting_dic[ID][2]
        for CDV_values in nested_dic.values():
            file_object.write(","+ str(CDV_values))
        file_object.write("\n")

print("Created a data file")