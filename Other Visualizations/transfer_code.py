import pandas as pd 
import glob, os
import shutil

df =pd.read_csv("/home/nference/Output.csv")
output_path = "/home/nference/images_output"
input_path = '/home/nference/Desktop/dataset_debris/consolidated_inputs'
# print(df)
for i in df['Class'].unique():
    # print(i)
    df2 = df[df['Class']== i]
    # print(df2)
    try:
        if i == 1:
            for j in df2['Slide Names']:
                print(j)
                src1 = input_path + "/" + j
                dst1 = output_path + '/debris'
                # print(src)
                if not os.path.exists(dst1):
                    os.makedirs(dst1)
                shutil.copy(src1,dst1)
        elif i == 2:
            for k in df2['Slide Names']:
                # print(k)
                src2 = input_path + "/" + k
                dst2 = output_path + '/Biopsy'
                # print(dst2)
                if not os.path.exists(dst2):
                    os.makedirs(dst2)
                shutil.copy(src2,dst2)
        elif i == 3:
            for l in df2['Slide Names']:
                src3 = input_path + "/" + l
                dst3 = output_path + '/BG'
                if not os.path.exists(dst3):
                    os.makedirs(dst3)
                shutil.copy(src3,dst3)
    except Exception as msg:
        print(msg)

            