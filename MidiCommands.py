# class BaseMidiMessage():
# 	def __init__():
# 		pass

# class splitMessage():
# 	def __init__(self,func):
# 		self.func=func
# 		self.__doc__=func.__doc__
# 	def __call__(self,*args,**kwargs):
# 		func=self.func
# 		return applySplitMessage(func(*args,**kwargs))

def splitMessage(msg):
	nmsg=[]
	for p in msg.split(" "):
		nmsg.append(int(p,base=2))
	return bytes(nmsg)

def system_exclusive(data:bytes):
	return b'\xF0'+data+b'\xF7'

def note_on(channel:int=0,note:int=60,velocity:int=127):
	return splitMessage('1001{:0>4b} 0{:0>7b} 0{:0>7b}'.format(channel,note,velocity))

def note_off(channel:int=0,note:int=60,velocity:int=127):
	return splitMessage('1000{:0>4b} 0{:0>7b} 0{:0>7b}'.format(channel,note,velocity))

def poly_pressure(channel:int=0,note:int=60,velocity:int=127):
	return splitMessage('1010{:0>4b} 0{:0>7b} 0{:0>7b}'.format(channel,note,velocity))

def controller_change(channel:int=0,controller:int=0,value:int=0):
	return splitMessage('1011{:0>4b} 0{:0>7b} 0{:0>7b}'.format(channel,controller,value))

def program_change(channel:int=0,program:int=0):
	return splitMessage('1100{:0>4b} 0{:0>7b}'.format(channel,program))

def mono_pressure(channel:int=0,pressure:int=0):
	return splitMessage('1101{:0>4b} 0{:0>7b}'.format(channel,pressure))

def pitch_bend(channel:int=0,lo:int=0,hi:int=127):
	return splitMessage('1110{:0>4b} 0{:0>7b} 0{:0>7b}'.format(channel,lo,hi))
