from skimage.morphology import (erosion, dilation, opening, closing,  # noqa
                                white_tophat)
from skimage.io import imread, imsave
from skimage.morphology import watershed, disk
import matplotlib.pyplot as plt

image = imread('endo_cells_screen.png')
img=image[:,:,0]
img.shape
footprint = disk(3)
eroded = erosion(img,footprint)
plt.imshow(eroded)
plt.show()
