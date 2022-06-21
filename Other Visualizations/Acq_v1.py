import sqlite3
import os, glob,cv2,sys
from dask.delayed import right
from numba.core.callconv import Status
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from matplotlib import pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

# |----------------------------------------------------------------------------|
# showImage
# |----------------------------------------------------------------------------|
def showImage(image, name):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 600, 600)
    cv2.imshow(name, image)
    cv2.waitKey(0)
# |----------------------------------------------------------------------------|



# ==============================================================================
# DatabaseParsing
# ==============================================================================

class DatabaseParsing():
    '''
    This class is to read the values from the database
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
# no class variables

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        self.bestz_list = []
        self.slide_path = ""
# |----------------------------------------------------------------------------|
# get_aoi_info
# |----------------------------------------------------------------------------|
    def get_aoi_info(self, db_path):
        '''
            To do the preprocessing required to detect the bounidng boxes and
            to compute the scan area coordinates with respect to slot.
            @param db_path: Data base path
            @param db_path2: 
        '''
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        query = "SELECT aoi_x, aoi_y, aoi_name, point_type, status FROM focus_sampling_info JOIN aoi USING (aoi_name)"
        # print(query)
        cursor.execute(query)

        aoi_data = cursor.fetchall()
        aoi_info_list = []
        for i in range(0, len(aoi_data)):
            x_pos = aoi_data[i][0]
            y_pos = aoi_data[i][1]
            aoi_name = aoi_data[i][2]
            point_type = aoi_data[i][3]
            status = aoi_data[i][4]
            # print(point_type)

            aoi_info_list.append([x_pos, y_pos, aoi_name, point_type, status])

        query = "SELECT aoi_x, aoi_y, aoi_name, point_type FROM focus_sampling_info JOIN aoi USING (aoi_name) WHERE point_type = 0"
        # print(query)
        cursor.execute(query)
        z_data = cursor.fetchall()
        bestz_list = []
        for i in range(0, len(z_data)):
            x_pos = z_data[i][0]
            y_pos = z_data[i][1]
            aoi_name = z_data[i][2]
            # print(aoi_name)

            bestz_list.append([x_pos, y_pos, aoi_name])
        return aoi_info_list , bestz_list
# |----------------------------------------------------------------------------|
    

# |----------------------------------------------------------------------------|
# grid_info
# |----------------------------------------------------------------------------|
    def grid_info(self, db_path):
        conn = sqlite3.connect(db_path)
        df_grid = pd.read_sql_query("select grid_id, row_count, column_count, best_rows_ima,\
         fs_time, acq_time, grid_status from grid_info ;", conn)
        return df_grid
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# aoi_fs
# |----------------------------------------------------------------------------|
    def aoi_fs(self, db_path):
        conn = sqlite3.connect(db_path)
        df_fs = pd.read_sql_query("select aoi_name, x_pos, y_pos, ref_aoi, ref_z, best_z, stack_size,\
         best_index, focus_metric, color_metric, status, process_time, is_sampled, valid_blobs_count,\
         extended_direction, point_type,row_index,column_index, grid_id from focus_sampling_info ;", conn)
        return df_fs
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# aoi_table
# |----------------------------------------------------------------------------|
    def aoi_table(self, db_path):
        conn = sqlite3.connect(db_path)
        # print(db_path)
        df_aoi = pd.read_sql_query("select aoi_name, aoi_x, aoi_y, aoi_x_mic, aoi_y_mic, aoi_row_idx,\
         aoi_col_idx, aoi_class, bg_state_acq, focus_metric, color_metric, hue_metric, best_idx,\
         ref_z, ref_z_method, stack_size, best_z, grid_id, slide_col_idx, slide_row_idx, bg_state_fs, capture_status  from aoi ;", conn)

        return df_aoi
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# image_area_df
# |----------------------------------------------------------------------------|
    def image_area_df(self, db_path):
        conn = sqlite3.connect(db_path)
        df_image_area = pd.read_sql_query("select aoi_name, aoi_x, aoi_y, aoi_x_mic, aoi_y_mic, aoi_row_idx,\
         aoi_col_idx, aoi_class, bg_state_acq, focus_metric, color_metric, hue_metric, best_idx,\
         ref_z, ref_z_method, stack_size, best_z, annotation_presence, coverslip_presence, z_class_type, material_type from imaging_area_aois ;", conn)

        return df_image_area
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# map_aois_to_1x
# |----------------------------------------------------------------------------|
    def map_aois_to_1x(self, aoi_info_list, bestz_list, onex_img):
        fov_width = aoi_info_list[1][0] - aoi_info_list[0][0]
        fov_height = aoi_info_list[1][1] - aoi_info_list[0][1]
        
        for j in range(0,len(aoi_info_list)):
            x_pos = int(aoi_info_list[j][0])
            y_pos = int(aoi_info_list[j][1])
            x2 = int(x_pos + fov_width)
            y2 = int(y_pos + fov_height)
            # cv2.rectangle(onex_img, (x_pos, y_pos),(x2, y2),(0,0,255),4)

            point = int(aoi_info_list[j][3])
            status = int(aoi_info_list[j][4])
            if (point == 0 and status == 1):
                cv2.circle(onex_img,(x_pos,y_pos),1,(0,255,0),8)
            elif (point == 1 and status == 1):
                cv2.circle(onex_img,(x_pos,y_pos),1,(0,0,255),8)
            elif (point == 2 and status == 1):
                cv2.circle(onex_img,(x_pos,y_pos),1,(255,0,0),8)
            else:
                cv2.circle(onex_img,(x_pos,y_pos),1,(0,255,255),8)
        

        return onex_img
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# plot_Z
# |----------------------------------------------------------------------------|
    def plot_z(self, db_path):
        try:
            df = self.aoi_fs(db_path)
            df = df[(df['is_sampled'] == 1) & (df['status'] == 1) & (df['point_type'] >= 1)]
            df = df.drop_duplicates('aoi_name',keep='last')
            df['Z_upper'] = df['ref_z'] + (1.875 * ((df['stack_size']-1)/2).astype(int))
            df['Z_lower'] = df['ref_z'] - (1.875 * ((df['stack_size']-1)/2).astype(int))
            df['upper'] = df['Z_upper'] - df['ref_z']
            df['lower'] = df['ref_z'] - df['Z_lower']

            fig = go.Figure(data=go.Scatter(
                    x=df['aoi_name'],
                    y=df['ref_z'],name = "Reference Z's",mode = "markers+text",
                    text=(df['best_z'] - df['ref_z']),
                    textposition="top right",
                    textfont=dict(
                    family="sans serif",
                    size=9,
                    color="crimson"),
                    error_y=dict(
                        type='data',
                        array=df['upper'],
                        arrayminus=df['lower'])
                    ))


            fig.add_trace(go.Scatter(
            x = df['aoi_name'] , y = df['best_z'], name = "Best Z Obtained" ,text = df['ref_aoi'],textposition="top left",
                            textfont=dict(
                    family="sans serif",
                    size=7,
                    color="blue"),mode = 'markers + text',marker=dict(color='purple', size=8)))

            fig.update_yaxes(title = "Z Range, uM",title_font_family="Arial")
            fig.update_xaxes(title = "Fs AOI",title_font_family="Arial",showticklabels=True)
            fig.update_layout(title = "Ordered FS AOI's ")
            #|----------------------------------------------------------------------------|

            df_1 = self.grid_info(db_path)
            df_1 = df_1[(df_1['grid_status'] == 10)]

            df_1['best_rows_ima'] = df_1['best_rows_ima'].astype(int)
            df_2 = self.aoi_table(db_path)

            df_2 = df_2[(df_2['bg_state_acq'] == 0) & (df_2['capture_status'] == 1)]

            df_aoi = df_2[df_2['ima_row_idx'].isin(df_1['best_rows_ima'].to_list())]
            
            df_aoi['Z_upper'] = df_aoi['ref_z'] + (1.875 * ((df_aoi['stack_size']-1)/2).astype(int))
            df_aoi['Z_lower'] = df_aoi['ref_z'] - (1.875 * ((df_aoi['stack_size']-1)/2).astype(int))
            df_aoi['upper'] = df_aoi['Z_upper'] - df_aoi['ref_z']
            df_aoi['lower'] = df_aoi['ref_z'] - df_aoi['Z_lower']

            fig1 = go.Figure(data=go.Scatter(
                    x=df_aoi['aoi_name'],
                    y=df_aoi['ref_z'],name = "Reference Z's",mode = "markers+text",
                    text=(df_aoi['best_z'] - df_aoi['ref_z']),
                    textposition="top right",
                    textfont=dict(
                    family="sans serif",
                    size=4,
                    color="crimson"),
                    error_y=dict(
                        type='data',
                        array=df_aoi['upper'],
                        arrayminus=df_aoi['lower'])
                    ))


            fig1.add_trace(go.Scatter(
            x = df_aoi['aoi_name'] , y = df_aoi['best_z'], name = "Best Z Obtained" ,text = " ",textposition="top left",
                            textfont=dict(
                    family="sans serif",
                    size=7,
                    color="blue"),mode = 'markers + text',marker=dict(color='purple', size=4)))

            fig1.update_yaxes(title = "Z Range, uM",title_font_family="Arial")
            fig1.update_xaxes(title = "Fs AOI",title_font_family="Arial",showticklabels=False)
            fig1.update_layout(title = "Ordered FS AOI's During ACQ ")

            return fig, fig1
        except Exception as msg:
            print(msg)
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# fs_order
# |----------------------------------------------------------------------------|
    def fs_order(self, db_path):
        df = self.aoi_fs(db_path)
        df = df[(df['is_sampled'] == 1) & (df['status'] == 1)]
        df = df.drop_duplicates('aoi_name',keep='last')
        df1 = df[(df['is_sampled'] == 1) & (df['point_type'] == 1) & (df['status'] == 1)]
        df1 = df1.drop_duplicates('aoi_name',keep='last')

        fig = px.line(df, y =  df['best_z'],
                    text = "C : " + df["column_index"].astype(str) + "<br>R : " + df["row_index"].astype(str),)
        fig.add_traces(px.scatter(df1,
                    y = df1['best_z']).update_traces(marker_size=5, marker_color="green").data)

        fig.update_traces(textposition="top left")
        fig.update_yaxes(title = "Best Z",title_font_family="Arial")
        fig.update_xaxes(title = "AOI Col, uM",title_font_family="Arial",showticklabels=False)
        fig.update_layout(title = "Ordered FS AOI's from same Row")
        

        # Create figure with secondary y-axis
        fig1 = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig1.add_trace(
            go.Bar(x = df['aoi_name'], y = df['valid_blobs_count'], text = df['valid_blobs_count'],
                textposition="auto",
                textfont=dict(
                family="sans serif",
                size=9,
                color="crimson"), name="Valid Block Count"),
            secondary_y=False,
        )

        fig1.add_trace(
            go.Scatter(x = df['aoi_name'], y = df['process_time'], text = round(df['process_time'],2),mode = "markers+text+lines",
                textposition = "top right" ,
                textfont=dict(
                family="sans serif",
                size=9,
                color="crimson"), name="Process Time"),
            secondary_y=True,
        )

        # Add figure title
        fig1.update_layout(
            title_text="Valid Blocks and Process time"
        )

        # Set x-axis title
        fig1.update_xaxes(title_text="Aoi name")

        # Set y-axes titles
        fig1.update_yaxes(title_text="<b>Valid Blocks</b>", secondary_y=False)
        fig1.update_yaxes(title_text="<b>Process time (s)</b>", secondary_y=True)

        return fig , fig1
#|----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# resizeImage
# |----------------------------------------------------------------------------|

    def resizeImage(self, image, rowCount, colCount):
        try:
            factor = 7000//rowCount
            dim = ((colCount)*factor, (rowCount) * factor)
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            return resized
        
        except Exception as msg:
            exc_tb = sys.exc_info()[2]
            fname = os.path.join(
                os.getcwd(), os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
            print("Exception occured at ", exc_tb.tb_lineno, " in ", fname,
                  "Error is ", msg)

# # |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# aoi_class_map Generation
# |----------------------------------------------------------------------------|

    def aoi_class_map(self, db_path):
        aoi_map = None
        try:
            print("Inside heat map")
            df = self.aoi_table(db_path)
            aoi_name = [item for item in df['aoi_name']]
            aoi_class = [item for item in df['aoi_class']]
            slide_row_idx = [item for item in df['slide_row_idx']]
            slide_col_idx = [item for item in df['slide_col_idx']]

            row  = max(df['slide_row_idx']) +1
            col  = max(df['slide_col_idx']) +1
            aoi_class_map = np.zeros((row*40, col*40, 3))
            
            for i in range(len(aoi_name)):
                tempCol = slide_col_idx[i]
                tempRow = slide_row_idx[i]

                startX = tempCol*40
                endX = tempCol*40 + 40
                # if endX > aoi_class_map.shape[1] -1:
                #     endX = aoi_class_map.shape[1] -1

                startY = tempRow * 40
                endY = tempRow*40 + 40
                # if endY > aoi_class_map.shape[0]-1:
                #     endY = aoi_class_map.shape[0]-1

                if aoi_class[i] == 4:
                    aoi_class_map[startY+1:endY-1, startX+1:endX-1] = (255,255,255)
                if aoi_class[i] == 3:
                    aoi_class_map[startY+1:endY-1, startX+1:endX-1] = (225,225,225)
                if aoi_class[i] == 2:
                    aoi_class_map[startY+1:endY-1, startX+1:endX-1] = (150,150,150)
                if aoi_class[i] == 1:
                    aoi_class_map[startY+1:endY-1, startX+1:endX-1] = (128,128,128)
                if aoi_class[i] == 0:
                    aoi_class_map[startY+1:endY-1, startX+1:endX-1] = (0,0,0)
            print("OUt of the loop")
            aoi_map = self.resizeImage(aoi_class_map,row,col)
        except Exception as msg:
            exc_tb = sys.exc_info()[2]
            fname = os.path.join(
                os.getcwd(), os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
            print("Exception occured at ", exc_tb.tb_lineno, " in ", fname,
                  "Error is ", msg)


        return aoi_map
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# Heatmap Generation
# |----------------------------------------------------------------------------|

    def heat_map(self, db_path):
        best_z_hm = None
        fm_heatmap = None
        cm_heatmap = None
        try:
            print("Inside heat map")
            df = self.aoi_table(db_path)
            df = df[(df['bg_state_acq'] == 0) & (df['capture_status'] == 1)]
            aoi_name = [item for item in df['aoi_name']]
            focus_metric = [item for item in df['focus_metric']]
            color_metric = [item for item in df['color_metric']]
            best_z = [item for item in df['best_z']]
            slide_row_idx = [item for item in df['slide_row_idx']]
            slide_col_idx = [item for item in df['slide_col_idx']]
            
            resize_factor = 40
            image = np.zeros(((max(slide_row_idx) + 1)*resize_factor , (max(slide_col_idx)+ 1) *resize_factor) , np.float32)
            # print(image.shape)
            best_z_image = image.copy() 

            for i in range(len(aoi_name)):
                best_z_image[slide_row_idx[i]*resize_factor:slide_row_idx[i]*resize_factor + resize_factor, 
                             slide_col_idx[i]*resize_factor:slide_col_idx[i]*resize_factor + resize_factor] = best_z[i]
                # print(rowCount[i], colCount[i], best_z[i])
            unique_values = np.unique(best_z_image[best_z_image != 0])
            # print(unique_values, unique_values[0])
            best_z_image[best_z_image == 0] = unique_values[0]
            best_z_image = cv2.normalize(best_z_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            # print("Uniques: ", np.unique(best_z_image))
            best_z_hm = cv2.applyColorMap(best_z_image, cv2.COLORMAP_JET)
            #########################################################################

            print("Inside heat map")

            fm_image = image.copy() 

            for i in range(len(aoi_name)):
                fm_image[slide_row_idx[i]*resize_factor:slide_row_idx[i]*resize_factor + resize_factor, 
                             slide_col_idx[i]*resize_factor:slide_col_idx[i]*resize_factor + resize_factor] = focus_metric[i]
                # print(rowCount[i], colCount[i], best_z[i])

            unique_values = np.unique(fm_image[fm_image != 0])
            # print(unique_values, unique_values[0])
            fm_image[fm_image == 0] = unique_values[0]
            fm_image = cv2.normalize(fm_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            # print("Uniques: ", np.unique(fm_image))
            fm_heatmap = cv2.applyColorMap(fm_image, cv2.COLORMAP_JET)

            #########################################################################

            print("Inside heat map")

            cm_image = image.copy() 

            for i in range(len(aoi_name)):
                cm_image[slide_row_idx[i]*resize_factor:slide_row_idx[i]*resize_factor + resize_factor, 
                             slide_col_idx[i]*resize_factor:slide_col_idx[i]*resize_factor + resize_factor] = color_metric[i]
                # print(rowCount[i], colCount[i], best_z[i])

            unique_values = np.unique(cm_image[cm_image != 0])
            # print(unique_values, unique_values[0])
            cm_image[cm_image == 0] = unique_values[0]
            cm_image = cv2.normalize(cm_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            # print("Uniques: ", np.unique(cm_image))
            cm_heatmap = cv2.applyColorMap(cm_image, cv2.COLORMAP_JET)


        except Exception as msg:
            exc_tb = sys.exc_info()[2]
            fname = os.path.join(
                os.getcwd(), os.path.split(exc_tb.tb_frame.f_code.co_filename)[1])
            print("Exception occured at ", exc_tb.tb_lineno, " in ", fname,
                  "Error is ", msg)


        return best_z_hm , fm_heatmap, cm_heatmap
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# write_img 
# |----------------------------------------------------------------------------|
    def write_img(self,img_name, img):
        cv2.imwrite(self.slide_path + '/' + img_name, img)

# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# delete_img 
# |----------------------------------------------------------------------------|
    def delete_img(self,img_name):
        os.remove(self.slide_path + '/' + img_name)

# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# Read_image Subplot
# |----------------------------------------------------------------------------|

    def read_image(self, db_path):
        # create figure
        print("Inside Function : ")
        fig = plt.figure(figsize=(40, 40))

        # setting values to rows and column variables
        rows = 3
        columns = 3

        # reading images


        Image1 = cv2.imread(self.slide_path + '/mapped_img.png')
        Image2 = cv2.imread(self.slide_path + '/aoi_map.png' )
        Image3 = cv2.imread(self.slide_path + '/fs.png')
        Image4 = cv2.imread(self.slide_path + '/fs_order.png')
        Image5 = cv2.imread(self.slide_path + '/fs_block.png')
        Image6 = cv2.imread(self.slide_path + '/fs_acq.png')
        Image7 = cv2.imread(self.slide_path + '/fm_hm.png')
        Image8 = cv2.imread(self.slide_path + '/cm_hm.png')
        Image9 = cv2.imread(self.slide_path + '/hm_Z.png')

        # Adds a subplot at the 1st position
        fig.add_subplot(rows, columns, 1)

        # showing image
        plt.imshow(cv2.cvtColor(Image1, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Mapped Image")

        # Adds a subplot at the 2nd position
        fig.add_subplot(rows, columns, 2)

        # showing image
        plt.imshow(cv2.cvtColor(Image2, cv2.COLOR_BGR2RGB)) 
        plt.axis('off')
        plt.title("Classfication points")

        # Adds a subplot at the 3rd position
        fig.add_subplot(rows, columns, 3)

        # showing image
        plt.imshow(cv2.cvtColor(Image3, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Focus Sampling points")

        # Adds a subplot at the 4th position
        fig.add_subplot(rows, columns, 4)

        # showing image
        plt.imshow(cv2.cvtColor(Image4, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Focus Sampling Order")

        # Adds a subplot at the 5th position
        fig.add_subplot(rows, columns, 5)

        # showing image
        plt.imshow(cv2.cvtColor(Image5, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Focus Sampling Block Validation and Process Time")

        # Adds a subplot at the 6th position
        fig.add_subplot(rows, columns, 6)

        # showing image
        plt.imshow(cv2.cvtColor(Image6, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Best Row Focus Sampling During ACQ")

        # Adds a subplot at the 7th position
        fig.add_subplot(rows, columns, 7)

        # showing image
        plt.imshow(cv2.cvtColor(Image7, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Focus Metric HeatMap")

        # Adds a subplot at the 4th position
        fig.add_subplot(rows, columns, 8)

        # showing image
        plt.imshow(cv2.cvtColor(Image8, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Color Metric HeatMap")

        # Adds a subplot at the 4th position
        fig.add_subplot(rows, columns, 9)

        # showing image
        plt.imshow(cv2.cvtColor(Image9, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Best Z HeatMap")
        return fig
# |----------------------------------------------------------------------------|


# |----------------------------------------------------------------------------|
# main
# |----------------------------------------------------------------------------|
def main(slide_path):
    txt = glob.glob(slide_path+'/*')
    obj_parsing = DatabaseParsing()
    for slide in txt:
        try:
            slide_name = slide.split("/")[-1]
            db_path = os.path.join(slide, slide_name + ".db")
            print("DB path: ", db_path)
            # Connect to db and get aoi data.
            aoi_info_list, bestz_list = obj_parsing.get_aoi_info(db_path)
            # Map the aois to 1x image.
            onex_img_path = os.path.join(slide, "loc_output_data", "updatedInputImage.png")        
            onex_img = cv2.imread(onex_img_path)

            obj_parsing.slide_path = slide

            ########################### GET FS IMAGE ##############################################################################
            # mapped_img = obj_parsing.map_aois_to_1x(aoi_info_list, bestz_list, onex_img)
            # obj_parsing.write_img("mapped_img.png", mapped_img)

            aoi_map = obj_parsing.aoi_class_map(db_path)
            obj_parsing.write_img("aoi_map.png", aoi_map)

            # hm_Z , fm_hm, cm_hm= obj_parsing.heat_map(db_path)
            # obj_parsing.write_img("hm_Z.png", hm_Z)
            # obj_parsing.write_img("fm_hm.png", fm_hm)
            # obj_parsing.write_img("cm_hm.png", cm_hm)

            fig_fs_points, fig_fs_acq = obj_parsing.plot_z(db_path)
            fig_fs_points.write_image(slide + '/fs.png')
            fig_fs_acq.write_image(slide + '/fs_acq.png')

            fig_fs_order, fs_block = obj_parsing.fs_order(db_path)
            fig_fs_order.write_image(slide + '/fs_order.png')
            fs_block.write_image(slide + '/fs_block.png')

            # sub_img = obj_parsing.read_image(db_path)
            # sub_img.savefig(slide + '/sub_img.png')

            # lst = ['mapped_img.png', 'aoi_map.png', 'hm_Z.png', 'fm_hm.png', 'cm_hm.png', 'fs.png', 'fs_order.png', 'fs_block.png', 'fs_acq.png']
            # for i in lst:
            #     obj_parsing.delete_img(i)


        except Exception as msg:
            print(msg)
# |----------------------------------------------------------------------------|





if __name__ == '__main__':
    if len(sys.argv) > 1:
        slide_path = sys.argv[1]
        main(slide_path)
    else:
        print("Usage:\npython3 \t", sys.argv[0], "\n1.Slide Path")
    

