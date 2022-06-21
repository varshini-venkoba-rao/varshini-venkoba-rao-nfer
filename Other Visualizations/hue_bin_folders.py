import pandas as pd 
import glob, os
import shutil

df =pd.read_csv('/home/nference/Desktop/Annotations-Data/PPP5242/tissues.csv')
output_path = '/home/nference/Desktop/Annotations-Data/PPP5242/blueplots'
input_path = '/home/nference/Desktop/Annotations-Data/PPP5242/raw_images_compressed'
# print(df)
for i in df['status'].unique():
    # print(i)
    df2 = df[df['status']== i]
    # print(df2)
    try:
        if i == "Red":
            for j in df2['aoi_name']:
                print(j)
                src1 = input_path + "/" + j + '.jpeg'
                dst1 = output_path + '/Red' 
                # print(src)
                if not os.path.exists(dst1):
                    os.makedirs(dst1)
                shutil.copy(src1,dst1)
        elif i == "Pink":
            for k in df2['aoi_name']:
                src2 = input_path + "/" + k + '.jpeg'
                dst2 = output_path + '/Pink' 
                # print(dst2)
                if not os.path.exists(dst2):
                    os.makedirs(dst2)
                shutil.copy(src2,dst2)
        elif i == "Brown":
            for l in df2['aoi_name']:
                src3 = input_path + "/" + l + '.jpeg'
                dst3 = output_path + '/Brown' 
                if not os.path.exists(dst3):
                    os.makedirs(dst3)
                shutil.copy(src3,dst3)
        elif i == "Blue":
            for m in df2['aoi_name']:
                # print(k)
                src4 = input_path + "/" + m + '.jpeg'
                dst4 = output_path + '/Blue' 
                # print(dst2)
                if not os.path.exists(dst4):
                    os.makedirs(dst4)
                shutil.copy(src4,dst4)
        elif i == "Yellow":
            for n in df2['aoi_name']:
                src5 = input_path + "/" + n + '.jpeg'
                dst5 = output_path + '/Yellow' 
                if not os.path.exists(dst5):
                    os.makedirs(dst5)
                shutil.copy(src5,dst5)
        elif i == "Cyan":
            for o in df2['aoi_name']:
                # print(k)
                src6 = input_path + "/" + o + '.jpeg'
                dst6 = output_path + '/Cyan' 
                # print(dst2)
                if not os.path.exists(dst6):
                    os.makedirs(dst6)
                shutil.copy(src6,dst6)
        elif i == "Green":
            for p in df2['aoi_name']:
                src7 = input_path + "/" + p + '.jpeg'
                dst7 = output_path + '/Green' 
                if not os.path.exists(dst3):
                    os.makedirs(dst7)
                shutil.copy(src7,dst7)

    except Exception as msg:
        print(msg)