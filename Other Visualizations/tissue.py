import sqlite3, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
db_path = '/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/JR-20-93-B10-1_H01BBB16P-7974.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
query = "select aoi_name, aoi_class, hue_histogram from aoi where focus_metric > 10 and color_metric>60 and biopsy_ratio>15 and annotation_presence=0"
c.execute(query)
aoi_info = c.fetchall()
for i in range(0, len(aoi_info)):
    aoi_details = aoi_info[i]
    aoi_name = aoi_details[0]
    aoi_class = aoi_details[1]
    hue_hist = aoi_details[2]
df=pd.DataFrame(aoi_info)
print (df)
df[['hist1','hist2','hist3','hist4','hist5','hist6','hist7','hist8']] = df[2].str.split(',', expand=True)
df = df.rename(columns={0: 'aoi_name'})
df = df.rename(columns={1: 'aoi_class'})
df.drop(['hist8',2],axis =1,inplace = True)
print(df)
tissue= df.to_csv('/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/Tissues.csv')
d={}
df= pd.read_csv('/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/Tissues.csv')
Brown = 0
Yellow = 0
Green = 0
Cyan = 0
Blue = 0
Pink = 0
Red = 0
for i in df.index:
    temp = df.iloc[i]
    title = temp[1]
    temp2 = temp[3:]
    print(temp2)
    if temp2[0] is max(temp[3:]):
        status = "Brown"
        Brown += 1
    elif temp2[1] is max(temp[3:]):
        status ="Yellow"
        Yellow += 1
    elif temp2[2] is max(temp[3:]):
        status ="Green"
        Green += 1
    elif temp2[3] is max(temp[3:]):
        status ="Cyan"
        Cyan += 1
    elif temp2[4] is max(temp[3:]):
        status ="Blue"
        Blue += 1
    elif temp2[5] is max(temp[3:]):
        status ="Pink"
        Pink += 1
    elif temp2[6] is max(temp[3:]):
        status ="Red"
        Red += 1
    d[title] = status
    print(d)
    input(" ")
tissues_color= pd.DataFrame(d.items(),columns=["aoi_name","status"]) 
tissues_color.to_csv('/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/Tissuescolor.csv',index=False)
# print(df)
# Total_count= Brown + Yellow + Green + Cyan + Blue + Pink + Red
# print(Total_count)
# Percent_brown = (Brown/Total_count)*100
# Percent_yellow = (Yellow/Total_count)*100
# Percent_green = (Green/Total_count)*100
# Percent_cyan= (Cyan/Total_count)*100
# Percent_blue= (Blue/Total_count)*100
# Percent_pink = (Pink/Total_count)*100
# Percent_red = (Red/Total_count)*100
# print("Brown: ", Brown, round(Percent_brown))
# print("Yellow: ", Yellow, round(Percent_yellow))  
# print("Green: ", Green, round(Percent_green))
# print("Cyan: ", Cyan, round(Percent_cyan))
# print("Blue: ", Blue,round(Percent_blue))
# print("Pink: ", Pink,round(Percent_pink))
# print("Red: ", Red, round(Percent_red))
# d[title] = status
# print(d)
# input(" ")
# df = pd.DataFrame(d.items(),columns=["aoi_name","status"]) 
# df.to_csv("/home/nference/Downloads/status3.csv",index=False)
