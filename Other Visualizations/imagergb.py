import numpy as np
from PIL import Image, ImageDraw
array = np.zeros([100, 200, 3], dtype=np.uint8)
array[:,:100] = [219,151,-53] 
array[:,100:] = [190, 145, 9]   
img = Image.fromarray(array)
draw = ImageDraw.Draw(img)
text = '    Standard        Measured'
draw.text((2,2),text, align = 'center')
img.show()
# img.save('A1.png')