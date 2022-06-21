import cv2
import numpy as np
from PIL import Image
import os,glob
import sys
from unittest.mock import patch
import colour
from collections import defaultdict
import glob, os

# for filename in sorted(glob.glob("/home/adminspin/Downloads/Slide 2/*.png",recursive=True)):
input_img = cv2.imread('/home/nference/Desktop/Color Calibration - Mayo/Data/Slide 1/16P.png')
# name = .split('/')[-1].split('.')[0]
blue_image = input_img[:,:,0]
green_image = input_img[:,:,1]
red_image = input_img[:,:,2]
mask_img=np.zeros(green_image.shape, np.uint8)
mask_img[green_image < 210] = 255
Final = cv2.bitwise_and(input_img,input_img, mask= mask_img)
cv2.imshow("Final img",Final)
cv2.waitKey(0)
# cv2.imwrite("/home/adminspin/Downloads/Slide 2/pics/" + name + ".png",Final)
cv2.destroyAllWindows()

# def get_lab_value(_rgb):
#         _rgb_image = np.zeros((1,1,3), dtype=np.uint8)
#         _rgb_image[:,:,0] = _rgb[0]
#         _rgb_image[:,:,1] = _rgb[1]
#         _rgb_image[:,:,2] = _rgb[2]
#         _lab_image = cv2.cvtColor(_rgb_image, cv2.COLOR_RGB2LAB)
#         _l_mean = np.mean(_lab_image[:,:,0]) * (100/255)
#         _a_mean = np.mean(_lab_image[:,:,1]) - 128
#         _b_mean = np.mean(_lab_image[:,:,2]) - 128
#         return [_l_mean, _a_mean, _b_mean]

# def color_diff(RGB_ref,RGB_in):
#     _lab_ref = get_lab_value(RGB_ref)
#     _lab_in = get_lab_value(RGB_in)
#     delta_E_CIE1994 = colour.difference.delta_E_CIE1994(_lab_ref, _lab_in)
#     return delta_E_CIE1994



# input_path = glob.glob("/home/adminspin/Downloads/Slide 2/pics/*.png")
# def cropping(input_path):

#     for i in sorted(input_path)[::-1]:
#         dst_img = os.path.split(i)[0]+"/pics"
# #         print(dst_img)
#         if not os.path.exists(dst_img):
#             os.makedirs(dst_img)
#         img_raw = cv2.imread(i)
# #         roi = cv2.selectROI(img_raw)
# #         roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
        
#         cv2.imwrite(dst_img+"/crop_"+i.split('/')[-1].split('.')[0]+".jpeg",img_raw)
# #         cv2.destroyAllWindows()
#     list_img = os.listdir(dst_img) # iterating over dst_image to get the images as arrays

#     lst = []
#     for image in sorted(list_img):

#         [file_name, ext] = os.path.splitext(image) #splitting file name from its extension
#         arr = np.array(Image.open(os.path.join(dst_img, image))) #creating arrays for all the images
#         [h, w] = np.shape(arr)[0:2]#calculating height and width for each image
#         arr_dim = arr.ndim #calculating the dimension for each array
#         arr_shape = arr.shape #calculating the shape for each array
#         arr_mean = np.mean(arr, axis=(0,1))
# #         print([arr_mean[0],  arr_mean[1], arr_mean[2]])
#         lst.append([arr_mean[0],  arr_mean[1], arr_mean[2]])

                
#     # print(lst)
#     print("Color diff(22P-20P) : ",color_diff(lst[0],lst[1]))
#     print("Color diff(22P-18P) : ",color_diff(lst[0],lst[2]))
#     print("Color diff(22P-16P) : ",color_diff(lst[0],lst[3]))

# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         path = sys.argv[1]
    
#     cropping(input_path)