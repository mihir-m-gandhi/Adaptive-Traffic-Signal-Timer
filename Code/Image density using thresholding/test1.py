import os
import skimage
from skimage import io
from skimage.color import rgb2gray
from skimage.viewer import ImageViewer

try:
	img = io.imread('test2.jpg')
	print("OK")
	gray = rgb2gray(img)
	io.imshow(gray)
	io.show()
except IOError:
	pass

