import numpy
import scipy.ndimage

import ConfigurationFile
config = ConfigurationFile.read_config_file()

if not config["Technical options"]["Force disable CV2"].lower() in ("yes","true","1"):
	try:
		import cv2
	except:
		cv2=None
		print("Could not import OpenCV. This will slow everything down considerably.")
else:
	cv2=None
	print("OpenCV was manually disabled. This will slow everything down considerably.")

"Library of quick shortcut functions to apply operations on images in the form of numpy arrays"

def crop(surface,x,y,width,height):
	"Crop a numpy image / take a subsurface."
	return surface[x:x+width,y:y+height]

if cv2==None:
	def scale(surface,width=8,height=8):#default values are 8 because of the Launchpad's 8x8 grid
		"Scale a numpy image."
		return scipy.ndimage.zoom(surface,(height/surface.shape[0],width/surface.shape[1],1))
else:
	def scale(surface,width=8,height=8):#default values are 8 because of the Launchpad's 8x8 grid
		"Scale a numpy image."
		return cv2.resize(surface,dsize=(width,height),interpolation=cv2.INTER_LANCZOS4)