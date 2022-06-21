# EXTRACTING THE DATA
import sqlite3, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
db_path = "/home/nference/Desktop/Hue_Histogram/302968/302968.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
query = "select aoi_name, hue_histogram from aoi where focus_metric > 7 and LENGTH(hue_bins) > 0 order by aoi_name"
c.execute(query)
aoi_info = c.fetchall()
for i in range(0, len(aoi_info)):
    aoi_details = aoi_info[i]
    aoi_name = aoi_details[0]
    hue_bins = aoi_details[1]
df=pd.DataFrame(aoi_info)
df[['hist1','hist2','hist3','hist4','hist5','hist6','hist7','hist8']] = df[1].str.split(',', expand=True)
df = df.rename(columns={0: 'aoi_name'})
df.drop(['hist8',1],axis =1,inplace = True)
print(df)
df.to_csv("/home/nference/Desktop/Hue_Histogram/302968/status242.csv",index=False)

