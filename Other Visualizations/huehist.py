import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

df= pd.read_csv('/home/nference/Desktop/try.csv')
output_path ='/home/nference/Desktop/try_plots'
if not os.path.exists(output_path):
    os.makedirs(output_path)
for i in df.index:
    hue_bins=np.array([0.2, 0.15, 0.4, 0.2, 0.45, 0.2, 0.2])*2
    index = [1, 2, 3, 4, 5, 6, 7]
    temp = df.iloc[i]
    title = temp[0]
    temp2= temp[1:]
    print(temp2)
    fig= plt.hist(index, temp2, width=hue_bins, color=['brown', 'yellow', 'green', 'cyan', 'blue' , 'pink', 'red'])
    plt.show()
    plt.savefig(output_path+ "/" + str(title)+'.png')
    plt.clf()
    break

