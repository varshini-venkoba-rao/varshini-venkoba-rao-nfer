import cv2
import sqlite3
import numpy
import statistics 
import sys
import os
import json
import time
import sys
from numpy.lib.function_base import append
import xlsxwriter
import matplotlib.pyplot as plt
from os.path import join
import numpy as np
import pandas as pd
import math
from mpl_toolkits.mplot3d import Axes3D

def create_per_grid_image(_dbPath, input_updated_image_path, mask_path, item_location,aoi_name):
    try:
        image = cv2.imread(input_updated_image_path)
        mask = cv2.imread(mask_path)
        print(image.shape)
        connection = sqlite3.connect(_dbPath)
        cursor = connection.cursor()
        
        # get fov_width and fov height
        query = ("SELECT fov_width_pix, fov_height_pix FROM grid_info where grid_id = 1")
        print(query)
        cursor.execute(query)
        for i in cursor.fetchall():
            fov_width_pix = i[0]
            fov_height_pix = i[1]

        # get row and column count
        query = ("SELECT aoi_x, aoi_y FROM aoi where aoi_name = " + "'" + (aoi_name ) + "'")
        print(query)
        cursor.execute(query)
        for i in cursor.fetchall():
            start_x = i[0]
            start_y = i[1]
            end_x =  start_x + fov_width_pix
            end_y = start_y + fov_height_pix
            
            print(start_x, start_y, end_x, end_y)
            # represents the top left corner of rectangle
            start_point = ( int(start_x) , int(start_y) )

            # Ending coordinate, here (220, 220)
            # represents the bottom right corner of rectangle
            end_point = ( int(end_x) , int(end_y)  )

            # Blue color in BGR
            color1 = (255, 0,0)
            color2 = (0, 255, 255)

            # Line thickness of 2 px
            thickness = 2

            # Using cv2.rectangle() method
            # Draw a rectangle with blue line borders of thickness of 2 px
            image1 = image.copy()
            mask1 = mask.copy()
            image_1 = cv2.rectangle(image1, start_point, end_point, color1, thickness)
            mask_1 = cv2.rectangle(mask1, start_point, end_point, color2, thickness)
            path = item_location + "/debug"
            if not os.path.exists(path):
                os.mkdir(path)
            path1 = item_location + "/debug" + "/" + aoi_name + "_slide_grid_box.png"
            path2 = item_location + "/debug" + "/" + aoi_name +"_mask_grid_box.png"
            print("path1: ", path1)
            print("path2: ", path2)
            cv2.imwrite(path1, image_1)
            cv2.imwrite(path2, mask_1)
    except Exception as msg:
        print("[error]: ", msg)
        print(input_updated_image_path)


    
def main():
    if len(sys.argv)==3:
        slide_path = sys.argv[1]
        aoi_name = sys.argv[2]
    else:
        print("python3 put_box_on_aoi.py input_slide_path aoi_name")
        return
    
    all_aois = [
        "aoi0156",
"aoi0165",
"aoi2143",
"aoi2942",
"aoi2943",
"aoi2944",
"aoi2945",
"aoi2946",
"aoi2947",
"aoi2948",
"aoi2949",
"aoi2950",
"aoi2969",
"aoi2970",
"aoi2971",
"aoi2972",
"aoi2973",
"aoi2974",
"aoi2975",
"aoi2976",
"aoi2977",
"aoi2978",
"aoi2980",
"aoi2981",
"aoi2982",
"aoi2983",
"aoi2984",
"aoi3022",
"aoi3024",
"aoi3028",
"aoi3053",
"aoi3057",
"aoi3059",
"aoi3102",
"aoi3104",
"aoi3105",
"aoi3106",
"aoi3134",
"aoi3136",
"aoi3137",
"aoi3139",
"aoi3140",
"aoi3141",
"aoi3142",
"aoi3180",
"aoi3182",
"aoi3185",
"aoi3187",
"aoi3214",
"aoi3216",
"aoi3218",
"aoi3221",
"aoi3263",
"aoi3264",
"aoi3266",
"aoi3269",
"aoi3270",
"aoi3291",
"aoi3491",
"aoi3531",
"aoi3655",
"aoi3656",
"aoi3657",
"aoi3658",
"aoi3659",
"aoi3660",
"aoi3661",
"aoi3662",
"aoi3664",
"aoi3666",
"aoi3667",
"aoi3670",
"aoi3671",
"aoi3673",
"aoi3674",
"aoi3675",
"aoi3676",
"aoi3677",
"aoi3678",
"aoi3683",
"aoi3684",
"aoi3685",
"aoi3686",
"aoi3687",
"aoi3688",
"aoi3689",
"aoi3690",
"aoi3691",
"aoi3692",
"aoi3693",
"aoi3694",
"aoi3695",
"aoi3696",
"aoi3697",
"aoi3698",
"aoi3699",
"aoi3700",
"aoi3701",
"aoi3702",
"aoi3703",
"aoi3704",
"aoi3705",
"aoi3706",
"aoi3707",
"aoi3708",
"aoi3709",
"aoi3710",
"aoi3711",
"aoi3730",
"aoi3731",
"aoi3732",
"aoi3733",
"aoi3734",
"aoi3735",
"aoi3736",
"aoi3737",
"aoi3738",
"aoi3739",
"aoi3740",
"aoi3741",
"aoi3742",
"aoi3743",
"aoi3744",
"aoi3745",
"aoi3746",
"aoi3747",
"aoi3748",
"aoi3749",
"aoi3750",
"aoi3751",
"aoi3752",
"aoi3753",
"aoi3754",
"aoi3755",
"aoi3756",
"aoi3757",
"aoi3758",
"aoi3763",
"aoi3764",
"aoi3765",
"aoi3766",
"aoi3767",
"aoi3768",
"aoi3769",
"aoi3770",
"aoi3771",
"aoi3772",
"aoi3773",
"aoi3774",
"aoi3775",
"aoi3776",
"aoi3777",
"aoi3778",
"aoi3779",
"aoi3780",
"aoi3781",
"aoi3782",
"aoi3783",
"aoi3784",
"aoi3785",
"aoi3786",
"aoi3787",
"aoi3788",
"aoi3789",
"aoi3790",
"aoi3815",
"aoi3816",
"aoi3817",
"aoi3818",
"aoi3819",
"aoi3820",
"aoi3821",
"aoi3822",
"aoi3823",
"aoi3824",
"aoi3825",
"aoi3826",
"aoi3827",
"aoi3828",
"aoi3829",
"aoi3830",
"aoi3831",
"aoi3832",
"aoi3833",
"aoi3834",
"aoi3835",
"aoi3836",
"aoi3837",
"aoi3838",
"aoi3843",
"aoi3844",
"aoi3845",
"aoi3846",
"aoi3847",
"aoi3848",
"aoi3849",
"aoi3850",
"aoi3851",
"aoi3852",
"aoi3853",
"aoi3854",
"aoi3855",
"aoi3861",
"aoi3862",
"aoi3907",
"aoi3908",
"aoi3909",
"aoi3910",
"aoi3911",
"aoi3912",
"aoi3913",
"aoi3914",
"aoi3915",
"aoi3916",
"aoi3917",
"aoi4085",
"aoi4086",
"aoi4087",
"aoi4088",
"aoi4089",
"aoi4151",
"aoi4152",
"aoi4153",
"aoi4154",
"aoi4155",
"aoi4156",
"aoi4157",
"aoi4164",
"aoi4165",
"aoi4166",
"aoi4167",
"aoi4168",
"aoi4169",
"aoi4170",
"aoi4231",
"aoi4232",
"aoi4233",
"aoi4234",
"aoi4235",
"aoi4236",
"aoi4237",
"aoi4244",
"aoi4245",
"aoi4246",
"aoi4247",
"aoi4248",
"aoi4249",
"aoi4250",
"aoi4310",
"aoi4311",
"aoi4312",
"aoi4313",
"aoi4314",
"aoi4315",
"aoi4316",
"aoi4317",
"aoi4324",
"aoi4325",
"aoi4326",
"aoi4327",
"aoi4328",
"aoi4329",
"aoi4330",
"aoi4331",
"aoi4390",
"aoi4391",
"aoi4392",
"aoi4393",
"aoi4394",
"aoi4395",
"aoi4396",
"aoi4397",
"aoi4404",
"aoi4405",
"aoi4406",
"aoi4407",
"aoi4408",
"aoi4409",
"aoi4410",
"aoi4411",
"aoi4448",
"aoi4449",
"aoi4450",
"aoi4451",
"aoi4469",
"aoi4470",
"aoi4471",
"aoi4472",
"aoi4473",
"aoi4474",
"aoi4475",
"aoi4476",
"aoi4477",
"aoi4484",
"aoi4485",
"aoi4486",
"aoi4487",
"aoi4488",
"aoi4489",
"aoi4490",
"aoi4491",
"aoi4492",
"aoi4511",
"aoi4512",
"aoi4513",
"aoi4525",
"aoi4526",
"aoi4527",
"aoi4528",
"aoi4529",
"aoi4530",
"aoi4532",
"aoi4549",
"aoi4550",
"aoi4551",
"aoi4552",
"aoi4553",
"aoi4554",
"aoi4555",
"aoi4556",
"aoi4557",
    ]
    for aoi_idx in range(0,len(all_aois)):
        aoi_name = all_aois[aoi_idx]
        print("%"*20)
        print("aoi_name: ", aoi_name)
        head_tail = os.path.split(slide_path)
        item = head_tail[1]
        print("slide_name: ", item)
        image_path = slide_path+"/loc_output_data/updatedInputImage.png"
        mask_path = slide_path+"/loc_output_data/foregroundMask.png"
        if not os.path.exists(mask_path):
            mask_path = slide_path+"/loc_output_data/foregroundMask.jpeg"
        if not os.path.exists(image_path):
            image_path = slide_path+"/loc_output_data/updatedInputImage.jpeg"
        dbPath = slide_path+"/"+item+".db"  
        create_per_grid_image(dbPath, image_path, mask_path, slide_path,aoi_name)
    
if __name__ == "__main__":
    main()
