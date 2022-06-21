import numpy as np
import skimage.color
import skimage.io
import matplotlib.pyplot as plt


# read the image of a plant seedling as grayscale from the outset
image = skimage.io.imread(fname='/home/nference/Desktop/Color Calibration - Mayo/April_1_2022/Set 2/H01BBB22P-3610/0_0.jpeg', as_gray=True)

# display the image
fig, ax = plt.subplots()
plt.imshow(image)
plt.show()
colors = ("red", "green", "blue")
channel_ids = (0, 1, 2)

# create the histogram plot, with three lines, one for
# each color
plt.figure()
plt.xlim([0, 256])
for channel_id, c in zip(channel_ids, colors):
    histogram, bin_edges = np.histogram(
        image[:, :, channel_id], bins=256, range=(0, 256)
    )
    plt.plot(bin_edges[0:-1], histogram, color=c)

plt.title("Color Histogram")
plt.xlabel("Color value")
plt.ylabel("Pixel count")

plt.show()
list1 = (1, 2, 3, 4, 5)
list2 = ("a", "b", "c", "d", "e")

for x in zip(list1, list2):
    print(x)

