binds = {
	11:"left",
	21:"left",
	12:"down",
	13:"right",
	23:"right",
	22:"up",
	32:"up",
	17:"b",
	18:"a",
	59:"select",
	69:"start",
}

def convert_pressed_to_mask(buttons):
	buttons_by_name = []
	for button in buttons:
		if button in binds:
			buttons_by_name.append(binds[button])
		else:
			print("Unbound button:",button)
	indexed_buttons = []
	for button in ["b","a","select","start","up","down","left","right","a","b"]:
		if button in buttons_by_name:
			indexed_buttons.append(1)
		else:
			indexed_buttons.append(0)
	return indexed_buttons

if __name__=="__main__":
	x=convert_pressed_to_mask([11,23,17,81,22,32])
	print(x)
	assert x==[1,0,0,0,1,0,1,1,0,1]
	print("Test OK")