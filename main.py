from subprocess import call, check_output
from os.path import expanduser
import os
import shutil

EXIF_INFO = {}
main_path = ''

def main():
	print("Welcome to exifSort! \nTo begin, input your image folder path: ")
	path = raw_input('> ')
	import_data(path)

	print("Import complete. You may now input commands. Enter 'help' for a list of commands.")
	while True:
		command = raw_input('> ')
		if command == 'swap':
			new_path = raw_input('Please enter the new folder path to sort: ')
			swap(new_path)
		elif command == 'type':
			copy = raw_input('Keep copy of original files? (Y/N): ')
			if copy == 'Y':
				x = True
				type(x)
			elif copy == 'N':
				x = False
				type(x)
			else:
				print('Please only enter Y or N.')
		elif command == 'help':
			print("You're outta luck bub.")
		else:
			print("Please input a proper command.")

# gets all exif data from folder
def import_data(path):
	# weird input? Clarify. Right now, no home directory or beginning / needed.
	global main_path 
	main_path = expanduser("~") + '/' + path
	for file_name in os.listdir(main_path):
		if os.path.isfile(main_path + '/' + file_name):
			exif = check_output(['exiv2', '-p', 's', main_path + '/' + file_name])
			one = exif.split('\n')
			# this may not be safe. Not sure if it's always 4 at the end. CHECK.
			two = one[:len(one) - 4]
			dic = {}
			for item in two:
				k, v = item.split(':', 1)
				dic[k.strip()] = v.strip()
			EXIF_INFO[file_name] = dic

# moves file to folder, creates folder if necessary
# maybe add feature to create folder in new destination. Currently creates in place.
def move_file(file_name, dest_name, copy):
	if not os.path.exists(dest_name):
		os.makedirs(dest_name)
	if copy:
		shutil.copy2(main_path + '/' + file_name, dest_name + '/' + file_name)
	else:
		shutil.move(main_path + '/' + file_name, dest_name + '/' + file_name)

# changes the folder that the program is sorting
def swap(path):
	global main_path
	main_path = expanduser("~") + '/' + path

# organize by image type, maybe allow more granularity (FINE, MEDIUM, etc.)
def type(copy):
	for image in EXIF_INFO:
		if EXIF_INFO[image]['Image quality'] == 'RAW':
			move_file(image, main_path + '/RAW', copy)
		else:
			move_file(image, main_path + '/JPEG', copy)

def shutter(boundaries, copy):
	pass


def iso():
	pass

def aperture():
	pass

def date():
	pass

main()