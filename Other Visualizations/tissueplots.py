# PLOTS OF HUE_HISTOGRAM WITH FM > 7
import sqlite3, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df= pd.read_csv('/home/nference/Desktop/Annotations-Data/H01CBA05P-14/tissues.csv')
output_path = '/home/nference/Desktop/Annotations-Data/H01CBA05P-14/tissues_plots'
if not os.path.exists(output_path):
    os.makedirs(output_path)
for i in df.index:
    # print('i ', i)
    hue_bins=np.array([0.2, 0.15, 0.4, 0.2, 0.45, 0.2, 0.2])*2
    index = [1, 2, 3, 4, 5, 6, 7]
    temp = df.iloc[i]
    title = temp[0]
    temp2 = temp[2:9]
    print(temp2)
    plt.title(title)
    fig= plt.bar(index, temp2, width=hue_bins, color=['brown', 'yellow', 'green', 'cyan', 'blue' , 'pink', 'red'])
    plt.savefig(output_path+ "/" +'.png')
    # print(output_path+ "/" + "PLot"+ str(title)+'.png')
    # plt.show()
    # plt.clf()
    # break
