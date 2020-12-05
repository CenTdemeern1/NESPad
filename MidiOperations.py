import ConfigurationFile
import MidiCommands
import numpy
import math
from typing import TypeVar,ByteString,Sequence

AnyBytes = TypeVar('AnyBytes', Sequence[int], ByteString) # Define "AnyBytes" Type Hinting, see PEP 483 for a simple explanation, and PEP 484 and PEP 526 for more details.

config = ConfigurationFile.read_config_file()
midilib = config["MIDI options"]["MIDI library"]

MIDILIB_RTMIDI = "rtmidi"
MIDILIB_PYGAME = "pygame"

if midilib == MIDILIB_RTMIDI:
	try:
		import rtmidi
	except:
		print("Could not import RtMidi!") # Why is the name capitalization like this?
		raise
elif midilib == MIDILIB_PYGAME:
	try:
		import pygame.midi
	except:
		print("Could not import Pygame!")
		raise



class BaseMIDI():
	def __init__(self):
		self.buttons=[]
	def send_bytes(self,bytedata:AnyBytes):
		pass
	def send_byte(self,byte:int):
		self.send_bytes([byte])
	def note_on(self,channel=0,note=60,velocity=127):
		self.send_bytes(MidiCommands.note_on(channel,note,velocity))
	def note_off(self,channel=0,note=60,velocity=127):
		self.send_bytes(MidiCommands.note_off(channel,note,velocity))
	def system_reset(self):
		self.send_bytes(MidiCommands.controller_change(0,0x7B,0))#All notes off
		self.send_bytes(MidiCommands.system_exclusive(bytes([0,32,41,2,24,14,0])))#All lights off
		self.send_byte(0xFF)#Reset
	def set_display(self,a:numpy.ndarray):
		command=[0, 32, 41, 2, 24, 11]
		reshaped=numpy.flip(a,0).reshape(-1,3)
		for i in range(60):
			led_id=((math.floor(i/8)+1)*10)+(i%8)+1
			command.append(led_id)
			# print(led_id)
			for c in reshaped[i]:
				command.append(c>>2)
		command=MidiCommands.system_exclusive(bytes(command))
		# print(list(command))
		self.send_bytes(command)
		command=[0, 32, 41, 2, 24, 11]
		for i in range(60,64):
			led_id=((math.floor(i/8)+1)*10)+(i%8)+1
			command.append(led_id)
			# print(led_id)
			for c in reshaped[i]:
				command.append(c>>2)
		command=MidiCommands.system_exclusive(bytes(command))
		# print(list(command))
		self.send_bytes(command)
	def get_pressed(self):
		self.process_input_events()
		return self.buttons
	def process_input_events(self):
		pass



class RtMidiMIDI(BaseMIDI):
	def __init__(self):
		super().__init__()
		self.midiout=rtmidi.MidiOut()
		if self.midiout.get_port_count()==0:
			raise IOError("No MIDI output devices found.")
		launchpadFound=False
		for lpid,name in enumerate(self.midiout.get_ports()):
			if "Launchpad MK2" in name:
				launchpadFound=True
				break
		if not launchpadFound:
			raise IOError("Launchpad not plugged in. (Launchpad MK2 output device not found)")
		self.midiout.open_port(lpid)
		self.midiin=rtmidi.MidiIn()
		if self.midiin.get_port_count()==0:
			raise IOError("No MIDI input devices found.")
		launchpadFound=False
		for lpid,name in enumerate(self.midiin.get_ports()):
			if "Launchpad MK2" in name:
				launchpadFound=True
				break
		if not launchpadFound:
			raise IOError("Launchpad not plugged in????? (Launchpad MK2 input device not found?????) - Sanity check failed HARD.") # This should never happen because the output was found if this part of the code was even reached. Of course, there may always be the microsecond perfect timing unplug
		self.midiin.open_port(lpid)
	def send_bytes(self,bytedata:AnyBytes):
		self.midiout.send_message(bytedata)
	def process_input_events(self):
		msg=()
		while msg!=None:
			msg=self.midiin.get_message()
			if msg==None:
				continue
			event,time=msg
			event=list(event)
			if not (event[0]&0b11110000) in (128,144):
				continue
			if (event[0]&0b11110000)==128 or ((event[0]&0b11110000)==144 and event[2]==0): #Note off
				if not event[1] in self.buttons:
					print("Sanity check failed: Tried to release button that was never pressed.")
					continue
				self.buttons.remove(event[1])
				# print("Button {} released".format(event[1]))
			elif (event[0]&0b11110000)==144: #Note on
				if event[1] in self.buttons:
					print("Sanity check failed: Tried to press button that was already pressed.")
					continue
				self.buttons.append(event[1])
				# print("Button {} pressed".format(event[1]))

#class PygameMIDI

def init_midi_class_in_config():
	if midilib==MIDILIB_RTMIDI:
		return RtMidiMIDI()
	elif midilib==MIDILIB_PYGAME:
		pass
