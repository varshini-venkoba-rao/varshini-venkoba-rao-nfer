import sqlite3, os,glob,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def tissue(input_path):
    
    db_path = input_path
    #db_path = glob.glob(input_path+"/*.db")[0]
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
    
    df[['hist1','hist2','hist3','hist4','hist5','hist6','hist7','hist8']] = df[2].str.split(',', expand=True)
    df = df.rename(columns={0: 'aoi_name'})
    df = df.rename(columns={1: 'aoi_class'})
    df.drop(['hist8',2],axis =1,inplace = True)
    # print(df)

    return df

def annotation(input_path):
    db_path = input_path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = "select aoi_name, aoi_class, hue_histogram from aoi where is_out_of_focus = 1"
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
    return df
def plots(input_path,df,title):

    output_path = os.path.split(input_path)[0] +"/"+input_path.split("/")[-1].split("_")[-1].split(".")[0]+".png"
    slide_name = path.split("/")[-2]
    print(output_path+"/"+title+".png")

    index= ["0-20","20-35","35-75","75-95","95-140","140-160","160-180"]
    temp = df.iloc[1:,[2,3,4,5,6,7,8]]
    
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except:
            print('no: ',col)


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

    plt.title(input_path.split("/")[-1].split("_")[-1].split(".")[0])

    fig= plt.bar(index, lst2, color=['brown', 'yellow', 'green', 'cyan', 'blue' , 'pink', 'red'])
    addtext(index,[round(elem, 3) for elem in lst2])  
    plt.savefig(output_path)
    # plt.show()
    # plt.clf()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    plots(path,tissue(path),"Tissue")
    plots(path,annotation(path),"Annotation")