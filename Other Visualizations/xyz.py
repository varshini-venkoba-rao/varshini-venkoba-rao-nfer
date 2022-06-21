import os
import pandas as pd
import glob
string1="Planarity of slide from triangulation: pln_variation:"
string2="Planarity of slide: pln_variation:"
string3="error_from_triangualtion"
a1=[]
b1=[]
c1=[]
Slide_name1=[]
for filename in glob.glob("/home/nference/Downloads/Log_folder/*.log",recursive=True):
    slide_name=filename.split('/')[-1].split('.')[0]
    Slide_name1.append(slide_name)
    for line in open(filename):
        if string1 in line:
            a = line.split(":")[-1]
            a1.append(a)
        elif string2 in line:
            b = line .split(":")[-1]
            b1.append(b)
        elif string3 in line:
            c = line.split(":")[-1]
            c1.append(c)
df = pd.DataFrame({"Slide Name":Slide_name1,
                    "Planarity of slide from triangulation":a1,
                    "Planarity of slide":b1,
                    "error_from_triangualtion":c1})
df1=df.replace('\n','',regex=True)
print(df1)
df1.to_csv("/home/nference/Downloads/planarity.csv",index = False)

