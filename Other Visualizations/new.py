from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl
fig = plt.figure(figsize = (10,7))
ax = fig.add_subplot(111, projection='3d')
ax.plot([-69,6],[95,77],[134,116],color='black')
ax.plot([134,126],[25,22],[32,25],color='black')
ax.plot([150,143],[50,35],[101,95],color='black')  
ax.plot([25,19],[114,109],[55,35],color='black')
ax.plot([219,190],[151,145],[-53,9],color='black')
ax.plot([-16,3],[47,39],[104,91],color='black')
ax.plot([62,54],[50,38],[73,67],color='black')
ax.plot([201,198],[202,197],[194,190],color='black')
ax.plot([166,165],[167,163],[159,152],color='black')
ax.plot([129,120],[135,130],[128,123],color='black')
ax.plot([153,138],[48,34],[60,52],color='black')
ax.plot([187,170],[86,77],[0,2],color='black')
ax.plot([202,109],[125,118],[-30,9],color='black')
ax.plot([138,120],[148,134],[28,19],color='black')
ax.plot([90,80],[98,82],[94,83],color='black')
ax.plot([55,35],[65,56],[61,57],color='black')
ax.plot([28,19],[37,25],[35,30],color='black')
ax.plot([25,18],[67,58],[126,119],color='black')
ax.plot([15,9],[153,124],[140,134],color='black')
ax.plot([95,88],[104,95],[137,120],color='black')
ax.plot([68,55],[85,79],[50,34],color='black')
ax.plot([47,34],[96,81],[120,112],color='black')
ax.plot([166,156],[115,110],[91,87],color='black')
ax.plot([89,69],[62,56],[48,40],color='black')
z = [134,32,101,55,-53,104,73,194,159,128,60,0,-30,28,94,61,35,126,140,137,50,120,91,48]    # Standard colors
x = [-69,134,150,25,219,-16,62,201,166,129,153,187,202,138,90,55,28,25,15,95,68,47,166,89]
y = [95,25,50,114,151,47,50,202,167,135,48,86,125,148,98,65,37,67,153,104,85,96,115,62]
z1 = [116,25,95,35,9,91,67,190,152,123,52,2,9,19,83,57,30,119,134,120,34,112,87,40]        # Measured colors
x1 = [6,126,143,19,190,3,54,198,165,120,138,170,109,120,80,35,19,18,9,88,55,34,156,69]
y1 = [77,22,35,109,145,39,38,197,163,130,34,77,118,134,82,56,25,58,124,95,79,81,110,56]
# ax.legend("Actual")
ax.text(-69, 95, 134, "A1", color='black')
ax.text(134, 25, 32, "A2", color='black')
ax.text(150, 50, 101, "A3", color='black')
ax.text(25, 114, 55, "A4", color='black')
ax.text(219, 151, -53, "A5", color='black')
ax.text(-16, 47, 104, "A6", color='black')
ax.text(62, 50, 73, "B1", color='black')
ax.text(201, 202, 194, "B2", color='black')
ax.text(166, 167, 159, "B3", color='black')
ax.text(129, 135, 128, "B4", color='black')
ax.text(153, 48, 60, "B5", color='black')
ax.text(187, 86, 0, "B6", color='black')
ax.text(202, 125, -30, "C1", color='black')
ax.text(138, 148, 28, "C2", color='black')
ax.text(90, 98, 94, "C3", color='black')
ax.text(55, 65, 61, "C4", color='black')
ax.text(28, 37, 35, "C5", color='black')
ax.text(25, 67, 126, "C6", color='black')
ax.text(15, 153, 140, "D1", color='black')
ax.text(95, 104, 137, "D2", color='black')
ax.text(68, 85, 50, "D3", color='black')
ax.text(47, 96, 120, "D4", color='black')
ax.text(166, 115, 91, "D5", color='black')
ax.text(89, 62, 48, "D6", color='black')
ax.scatter3D(x1, y1, z1, color = "red",s=30)
ax.scatter3D(x,y,z,color="green",s=30)
red_patch = mpatches.Patch(color='red', label='Measured')
green_patch = mpatches.Patch(color='green', label='Actual')
plt.legend(handles=[red_patch,green_patch])
ax.set_xlabel('Red')
ax.set_ylabel('Green')
ax.set_zlabel('Blue')
plt.title("Color Difference")
plt.show()




