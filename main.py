#Main script file. Run this to run the program.

def install_deps():
	import os,sys
	os.system(sys.executable+" -m pip install -r requirements.txt")

def main():
	#Yes I'm importing within the main function don't judge
	#I'm doing this so the error handler catches it if it throws
	import ConfigurationFile
	config = ConfigurationFile.read_config_file()
	import Launchpad
	lp = Launchpad.Launchpad()
	import Emulation
	import time
	pcdisplay=config["Emulation options"]["Enable view on PC"].lower() in ("yes","true","1")
	lpdisplay=config["Emulation options"]["Enable view on Launchpad"].lower() in ("yes","true","1")
	crop=config["Technical options"]["Crop to bottom center"].lower() in ("yes","true","1")
	if pcdisplay:
		import pygame,NumpyImageOperations
		pygame.init()
		display=pygame.display.set_mode((256,256))
	emu = Emulation.Emulator()
	fast_forward=config["Technical options"]["Run as fast as possible"].lower() in ("yes","true","1")
	while True:
		if not fast_forward:
			s=time.time()
		inp = lp.get_input()
		emu.buttons=inp
		emu.process()
		if pcdisplay:
			# img2=NumpyImageOperations.scale(emu.screen,8,8)
			# img2=img2.astype(int)
			img2=emu.screen.astype(int).swapaxes(0,1)
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					return
			i=pygame.transform.scale(pygame.surfarray.make_surface(img2),(256,256))
			display.blit(i,(0,0))
			pygame.display.flip()
		if lpdisplay:
			sc = emu.screen
			if crop:
				sc = NumpyImageOperations.crop(sc,122,60,122,120)
			lp.display_image(sc)
		if not fast_forward:
			time.sleep(max(1/60-(time.time()-s),0))


status_OK = False
try:
	main()
	print("Finished OK")
	status_OK = True
finally:
	if not status_OK:
		import sys
		if "win" in sys.platform:
			import winsound # Standard Python library. I wonder why; this seems more like something you would find as an external package.
			winsound.MessageBeep(winsound.MB_ICONHAND) # Plays "SystemHand" sound.
		else:
			print("You're not on windows, so the winsound standard python package isn't available.\nInstead, just act like you just heard the system default critical error sound.")
		print("\nCritical error; The following exception was fatal and the program has to close.")
		print("If this seems weird, you might want to report this. (see https://github.com/CenTdemeern1/NESPad/issues - copy and paste this link into the URL bar of your browser of choice.)\n")
