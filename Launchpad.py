import MidiOperations
import NumpyImageOperations
import InputBindings
import numpy
# da=numpy.ones((8,8,3))*255
# da=numpy.arange(8*8*3).reshape((8,8,3))
class Launchpad():
	def __init__(self):
		self.midi = MidiOperations.init_midi_class_in_config()
		self.midi.system_reset()
	def create_test_image(self):
		da=[]
		for _ in range(8):
			da.append(numpy.flip(numpy.arange(8*3).reshape((8,3))))
		da=numpy.array(da)
		da[0,:,0]=0
		da[1,:,1]=0
		da[2,:,2]=0
		da[3,:,0]=0
		da[4,:,1]=0
		da[5,:,2]=0
		da[6,:,1]=0
		da[7,:,0]=0
		return da
	def display_image(self,img:numpy.ndarray):
		img2=NumpyImageOperations.scale(img,8,8)
		img2=img2.astype(int)#.swapaxes(0,1)
		self.midi.set_display(img2)
	def get_input(self):
		return InputBindings.convert_pressed_to_mask(self.midi.get_pressed())
