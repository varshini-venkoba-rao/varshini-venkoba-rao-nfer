import sqlite3, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
        # print("Brown")
        status = "Brown"
        Brown += 1
    elif temp2[1] is max(temp[3:]):
        # print("Yellow")
        status ="Yellow"
        Yellow += 1
    elif temp2[2] is max(temp[3:]):
        # print("Green")
        status ="Green"
        Green += 1
    elif temp2[3] is max(temp[3:]):
        # print("Cyan")
        status ="Cyan"
        Cyan += 1
    elif temp2[4] is max(temp[3:]):
        # print("Blue")
        status ="Blue"
        Blue += 1
    elif temp2[5] is max(temp[3:]):
        # print("Pink")
        status ="Pink"
        Pink += 1
    elif temp2[6] is max(temp[3:]):
        # print("Red")
        status ="Red"
        Red += 1
    d[title] = status
    print(d)
    input(" ")
df = pd.DataFrame(d.items(),columns=["aoi_name","status"]) 
df.to_csv('/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/varsh.csv',index=False)
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

