import sqlite3, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df= pd.read_csv('/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/Tissues.csv')
output_path = '/home/nference/Music/JR-20-93-B10-1_H01BBB16P-7974/Annotations_plot'
index= ["0-20","20-35","35-75","75-95","95-140","140-160","160-180"]
temp = df.iloc[1:,[2,3,4,5,6,7,8]]
lst1 = [df['hist1'].sum(), df['hist2'].sum(), df['hist3'].sum(), df['hist4'].sum(), df['hist5'].sum(),
df['hist6'].sum(), df['hist7'].sum()]
lst2 =[]
for i in lst1:
    per = (i/sum(lst1))*100
    lst2.append(per)
print(lst2)
def addtext(x,y):
    for i in range(len(lst2)):
        plt.text(index[i],y[i],y[i])

plt.title("Annotation")
fig= plt.bar(index, lst2, color=['brown', 'yellow', 'green', 'cyan', 'blue' , 'pink', 'red'])
addtext(index,[round(elem, 3) for elem in lst2])  
plt.savefig(output_path)
plt.show()
plt.clf()
  
