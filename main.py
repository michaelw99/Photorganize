from subprocess import call, check_output
from os.path import expanduser
import os

EXIF_INFO = {}

def main():
	print("Welcome to exifSort! \nTo begin, input your image folder: ")
	path = raw_input()
	import_data(path)

	print("Import complete. You may now input commands. Enter 'help' for a list of commands.")
	while True:
		command = raw_input('>')

		pass

def import_data(path):
	# weird input? Clarify. Right now, no home directory or beginning / needed.
	edit_path = expanduser("~") + '/' + path
	for filename in os.listdir(edit_path):
		exif = check_output(['exiv2', '-p', 's', edit_path + '/' + filename])
		one = exif.split('\n')
		# this may not be safe. Not sure if it's always 4 at the end. CHECK.
		two = one[:len(one) - 4]
		dic = {}
		for item in two:
			k, v = item.split(':', 1)
			dic[k.strip()] = v.strip()
		EXIF_INFO[filename] = dic
	# print(EXIF_INFO)

# THIS IS THE MOTHERLOAD
def split_files():
	pass

def type():
	pass

def shutter():
	pass

def iso():
	pass

def aperture():
	pass

def date():
	pass

main()