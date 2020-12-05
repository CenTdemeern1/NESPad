import retro
import numpy
import sounddevice

import ConfigurationFile
config = ConfigurationFile.read_config_file()

class Emulator():
	def __init__(self):
		self.r = retro.RetroEmulator(config["Emulation options"]["ROM"])
		self.buttons=[0,0,0,0,0,0,0,0]#["b","a","select","start","ui_up","ui_down","ui_left","ui_right","a","b"]
		self.audiorate=self.r.get_audio_rate()
		self.stream=sounddevice.OutputStream(self.audiorate,dtype=numpy.int16)
		self.stream.start()
		self.screen=None
	
	def process(self):
		self.r.set_button_mask(self.buttons)
		self.r.step()
		# if not Input.is_action_pressed("ui_home"):
		self.display()
		# if not Input.is_action_pressed("ui_end"):
		self.playaudio()
	
	def display(self):
		data = self.r.get_screen()
		xres,yres = self.r.get_resolution()
		size = (yres,xres,3)
		self.screen = data.reshape(size)
		
	def playaudio(self):
		self.stream.write(self.r.get_audio())

if __name__=="__main__":
	import time
	emu = Emulator()
	while True:
		s=time.time()
		emu.process()
		time.sleep(max(1/60-(time.time()-s),0))

