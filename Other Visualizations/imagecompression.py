# import pandas as pd
# hadcrut = pd.read_csv(
#     '/home/nference/Desktop/mmm.csv',
#     delim_whitespace=True,
#     usecols=['R','G','B'],
# )
# hadcrut.head()

import cv2
import os

imgs_path = "/home/nference/Desktop/Annotations-Data/PPP5242/raw_images"
output_path = "/home/nference/Desktop/Annotations-Data/PPP5242/raw_images_compressed"
if not os.path.exists(output_path): os.mkdir(output_path)
for img_name in sorted(os.listdir(imgs_path)):
    aoi_name = img_name.split(".")[0]
    print(aoi_name)
    img = cv2.imread(os.path.join(imgs_path, img_name))
    cv2.imwrite(os.path.join(output_path, aoi_name+".jpeg"), img)