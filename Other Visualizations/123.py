from matplotlib import colors
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
data = pd.read_excel("/home/nference/Videos/Book2.xlsx")
for i in data['Char. No/ Balloon Number'].unique():
     df =  data[data['Char. No/ Balloon Number'] == i]
     df.drop(df.columns[[0,1,2,3,4,5]], axis = 1,inplace = True)
     dff = df.transpose()
     lst = dff.iloc[2:].values.tolist()
     lsl = dff.iloc[0,0]
     usl = dff.iloc[1,0]
     df_data = pd.DataFrame(lst)
     # print(df_data)
     sigma = 3
     # If the lower limit is 0, use the upper limit reverse negative value instead
     if int(lsl) == 0:
          lsl = 0 - usl
     u = df_data.mean()[0]
     stdev = np.std(df_data.values, ddof=1)
     # Generate average distribution of horizontal axis data
     x1 = np.linspace(u - sigma * stdev, u + sigma * stdev, 1000)
     # Calculate the normal distribution curve
     y1 = np.exp(-(x1 - u) ** 2 / (2 * stdev ** 2)) / (math.sqrt(2 * math.pi) * stdev)
     cpu = ((usl - u) / (3 * stdev))
     cpl = ((u - lsl) / (3 * stdev))
     cpk = min(cpu,cpl)
     print(cpk)
     plt.xlim(x1[0] - 0.5, x1[-1] + 0.5)
     plt.plot(x1, y1)
     plt.axvline(usl, color = "red",label = 'USL',linestyle='solid')
     plt.axvline(lsl, color = "red",label = 'LSL',linestyle='solid')
     usl1 = df_data.mean()[0] + (sigma * np.std(df_data.values, ddof=1))
     lsl1 = df_data.mean()[0] - (sigma * np.std(df_data.values, ddof=1))
     plt.axvline(x = usl1, color = "green",label = '3-sigma UCL',linestyle='--')
     plt.axvline(x = lsl1, color = "green",label = '3-sigma LCL',linestyle='--')
     plt.legend(loc="upper left")
     plt.hist(df_data.values, 15, density=True)
     plt.title(str(data['Reference Location'])+ " " + "cpk={0}".format(cpk))
     plt.show()


