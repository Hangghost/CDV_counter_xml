
import os
import glob
# print(os.getcwd())  # get working path

Chimei_ECG_file = os.listdir(".\\test data")  # get list of dir path

xml_filename_list = []
for xml_filename in glob.glob("./test data/**/*.xml", recursive=True):
    xml_filename_list.append(xml_filename)
print(xml_filename_list)