#If you are looking for the actual configuration file, it's configuration.ini. This is just the parser :)

import configparser # Default python library
def read_config_file():
	configurationfile = configparser.ConfigParser()
	configurationfile.read("./configuration.ini") # Ok Linux here you go here is your ./ because you like it so much - happy "Sinterklaas", here is your present.
	return configurationfile
