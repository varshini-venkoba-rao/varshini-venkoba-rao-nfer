
import pandas as pd 
import glob, os
import shutil

df =pd.read_csv("/home/nference/Desktop/Book1.csv")
output_path = "/home/nference/new_images"
if not os.path.exists(output_path):
    os.makedirs(output_path)
input_path = '/home/nference/Desktop/Debris Classification/grid_1/raw_images'
# print(df)
for i in df['Class'].unique():
    # print(i)
    df2 = df[df['Class']== i]
    # print(df2)
    try:
        if i == "Background":
            for j in df2['aoi name']:
                # print(j)
                src1 = input_path + "/" + j + ".jpeg"
                dst1 = output_path + '/BG'
                # print(dst1)
                if not os.path.exists(dst1):
                    os.makedirs(dst1)
                shutil.copy(src1,dst1)
        elif i == "Debris":
            print(i)
            for k in df2['aoi name']:
                print(k)
                src2 = input_path + "/" + k + ".jpeg"
                dst2 = output_path + '/Debris'
                # print(dst2)
                if not os.path.exists(dst2):
                    os.makedirs(dst2)
                shutil.copy(src2,dst2)
        elif i == "Biopsy":
            for l in df2['aoi name']:
                src3 = input_path + "/" + l + ".jpeg"
                dst3 = output_path + '/Biopsy'
                # print(dst3)
                if not os.path.exists(dst3):
                    os.makedirs(dst3)
                shutil.copy(src3,dst3)
    except Exception as msg:
        print(msg)

            