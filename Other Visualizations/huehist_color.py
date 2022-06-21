from unittest.mock import patch
import cv2
import colour
import numpy as np
from collections import defaultdict
import os
import statistics
class color_error:
    def __init__(self, file_ext_type, gamma) -> None:
        self.delta_E = {}
        self.lab_patch = {}
        self._file_ext_type = file_ext_type
        self.reference = defaultdict(dict)
        self.patch_name_list = []
        self.gamma_val = gamma
    def get_ref_value(self):
        #RGB values
        self.reference["A1"]["value"] = [-69, 95,  134]
        self.reference["A2"]["value"] = [134, 25,  32]
        self.reference["A3"]["value"] = [150, 50,  101]
        self.reference["A4"]["value"] = [25,  114, 55]
        self.reference["A5"]["value"] = [219, 151, -53]
        self.reference["A6"]["value"] = [-16,47,104]
        self.reference["B1"]["value"] = [62,  50,  73]
        self.reference["B2"]["value"] = [201, 202, 194]
        self.reference["B3"]["value"] = [166, 167, 159]
        self.reference["B4"]["value"] = [129, 135, 128]
        self.reference["B5"]["value"] = [153, 48, 60]
        self.reference["B6"]["value"] = [187, 86, 0]
        self.reference["C1"]["value"] = [202, 125,-30]
        self.reference["C2"]["value"] = [138, 148, 28]
        self.reference["C3"]["value"] = [90,  98,  94]
        self.reference["C4"]["value"] = [55,  65,  61]
        self.reference["C5"]["value"] = [28, 37,35]
        self.reference["C6"]["value"] = [25,67,126]
        self.reference["D1"]["value"] = [15,  153, 140]
        self.reference["D2"]["value"] = [95,  104, 137]
        self.reference["D3"]["value"] = [68,  85,  50]
        self.reference["D4"]["value"] = [47,  96,  120]
        self.reference["D5"]["value"] = [166,115,91]
        self.reference["D6"]["value"] = [89,62,48]
    def get_color_patch_name(self):
        char_array = ["A", "B", "C", "D"]
        num_array = ["1","2","3","4","5","6"]
        for _char in char_array:
            for _num in num_array:
                _name = str(_char + _num)
                self.reference[_name]["sRGB_value"]  = [0,0,0]
                self.reference[_name]["file_name"] = (_name + self._file_ext_type)
                self.patch_name_list.append(_name)
        print(self.patch_name_list)
    def get_color_error_patch(self, color_patch_lab_ref, color_patch_lab_in):
        delta_E_CIE1976 = colour.difference.delta_E_CIE1976(color_patch_lab_ref, color_patch_lab_in)
        delta_E_CIE1994 = colour.difference.delta_E_CIE1994(color_patch_lab_ref, color_patch_lab_in)
        delta_E_CIE2000 = colour.difference.delta_E_CIE2000(color_patch_lab_ref, color_patch_lab_in)
        delta_E_CMC = colour.difference.delta_E_CMC(color_patch_lab_ref, color_patch_lab_in)
        self.delta_E["delta_E_CIE1976"] = delta_E_CIE1976
        self.delta_E["delta_E_CIE1994"] = delta_E_CIE1994
        self.delta_E["delta_E_CIE2000"] = delta_E_CIE2000
        self.delta_E["delta_E_CMC"] = delta_E_CMC
    def get_lab_value_img(self, image_path, new_path):
        _rgb_image = cv2.imread(image_path)
        b_mean, b_std = cv2.meanStdDev(_rgb_image[:,:,0])
        g_mean, g_std = cv2.meanStdDev(_rgb_image[:,:,1])
        r_mean, r_std = cv2.meanStdDev(_rgb_image[:,:,2])
        print(r_mean,r_std)
        print(g_mean,g_std)
        print(b_mean,b_std)
        result = self.adjust_gamma(_rgb_image, self.gamma_val)
        cv2.imwrite(new_path, result)
        _lab_image = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
        _l_mean = np.mean(_lab_image[:,:,0]) * (100/255)
        _a_mean = np.mean(_lab_image[:,:,1]) - 128
        _b_mean = np.mean(_lab_image[:,:,2]) - 128
        return [_l_mean, _a_mean, _b_mean]
    def get_lab_value(self, _rgb):
        _rgb_image = np.zeros((1,1,3), dtype=np.uint8)
        _rgb_image[:,:,0] = _rgb[0]
        _rgb_image[:,:,1] = _rgb[1]
        _rgb_image[:,:,2] = _rgb[2]
        _lab_image = cv2.cvtColor(_rgb_image, cv2.COLOR_RGB2LAB)
        _l_mean = np.mean(_lab_image[:,:,0]) * (100/255)
        _a_mean = np.mean(_lab_image[:,:,1]) - 128
        _b_mean = np.mean(_lab_image[:,:,2]) - 128
        return [_l_mean, _a_mean, _b_mean]
    def adjust_gamma(self, image, gamma=1.0):
        # build a lookup table mapping the pixel values [0, 255] to
        # their adjusted gamma values
        invGamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")
        # apply gamma correction using the lookup table
        return cv2.LUT(image, table)
    def get_lab_patch(self, image_path, patch):
        _lab_patch_mean = self.get_lab_value(image_path)
        self.lab_patch[patch] = np.mean(_lab_patch_mean)
    def get_deltaE_using_RGBValue(self, RGB_ref, RGB_in):
        _lab_ref = color_error_obj.get_lab_value(RGB_ref)
        _lab_in = color_error_obj.get_lab_value(RGB_in)
        # print("_lab_ref", _lab_ref)
        # print("_lab_in", _lab_in)
        delta_E_CIE1976 = colour.difference.delta_E_CIE1976(_lab_ref, _lab_in)
        delta_E_CIE1994 = colour.difference.delta_E_CIE1994(_lab_ref, _lab_in)
        delta_E_CIE2000 = colour.difference.delta_E_CIE2000(_lab_ref, _lab_in)
        delta_E_CMC = colour.difference.delta_E_CMC(_lab_ref, _lab_in)
        self.delta_E["delta_E_CIE1976"] = delta_E_CIE1976
        self.delta_E["delta_E_CIE1994"] = delta_E_CIE1994
        self.delta_E["delta_E_CIE2000"] = delta_E_CIE2000
        self.delta_E["delta_E_CMC"] = delta_E_CMC
if __name__ == '__main__':
  PATCH_REF_AVAILABLE = 0
  RGB_REF_AVAILABLE = 1
if PATCH_REF_AVAILABLE == 1:
    file_ext_type = ".bmp"
    gamma = 2.2
    color_error_obj = color_error(file_ext_type, gamma)
    path = '/home/nference/Desktop/Color Calibration/17P scanner/Exposure_0.0610/'
    color_error_obj.get_color_patch_name()
    patch_name_list = color_error_obj.patch_name_list
    color_error_obj.get_ref_value()
    reference_list = color_error_obj.reference
    new_path_write = os.path.join(path, "with_gamma")
    os.mkdir(new_path_write)
    error1976 = []
    error1994 = []
    error2000 = []
    errorCMC = []
    for patch_name in patch_name_list:
        file_name = reference_list[patch_name]["file_name"]
        patch_value = reference_list[patch_name]["value"]
        print(file_name)
        print(path + file_name)
        print('patch Reference sRGB ', patch_name, patch_value)
        _lab_image = color_error_obj.get_lab_value_img(path + file_name, new_path_write + file_name)
        _lab_ref = color_error_obj.get_lab_value(patch_value)
        print('_lab_ref, _lab_input_image for', patch_name, ":", _lab_ref, _lab_image)
        color_error_obj.get_color_error_patch(_lab_ref, _lab_image)
        print(color_error_obj.delta_E)
        error1976.append(color_error_obj.delta_E['delta_E_CIE1976'])
        error1994.append(color_error_obj.delta_E['delta_E_CIE1994'])
        error2000.append(color_error_obj.delta_E['delta_E_CIE2000'])
        errorCMC.append(color_error_obj.delta_E['delta_E_CMC'])
        m76= statistics.mean(error1976)
        m94= statistics.mean(error1994)
        m20= statistics.mean(error2000)
        mcmc=statistics.mean(errorCMC)
    # print("error: ", error1976)
    # print(m76)
    print("error: ", error1994)
    # print(m94)
    # print("error: ", error2000)
    # print(m20)
    # print("error: ", errorCMC)
    # print(mcmc)`
if RGB_REF_AVAILABLE == 1:
    gamma = 2.2
    file_ext_type = '.bmp'
    color_error_obj = color_error(file_ext_type, gamma)
    RGB_ref = [224.40,214.80,221.79]
    RGB_in = [222.66,211.71,217.22]
    color_error_obj.get_deltaE_using_RGBValue(RGB_ref, RGB_in)
    print(color_error_obj.delta_E)