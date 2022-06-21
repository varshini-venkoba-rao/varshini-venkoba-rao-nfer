import glob
import cv2,os
import pandas as pd
input_path =("/home/nference/Desktop/raw_images.bmp")
output_path = ("/home/nference/Desktop/raw_images.jpeg")
if not os.path.exists(output_path):
        os.makedirs(output_path)
# files = (glob.glob(input_path + '/*.bmp'))
for filename in glob.glob("/home/nference/Desktop/raw_images.bmp/*.bmp",recursive=True):
    print(filename)
    aoi = filename.split('/')[-1].split('.')[0]
    img= cv2.imread(filename)
    cv2.imwrite(output_path + "/" + str(aoi) + '.jpeg',img)