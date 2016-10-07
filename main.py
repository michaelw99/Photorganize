from subprocess import call, check_output
import os
import shutil
import imghdr
import time
import datetime

# priority queue to keep sorted by time? 
# also add auto sorting
EXIF_INFO = {}
main_path = ''

def main():
	print("Welcome to exifSort! \nTo begin, input your image folder path: ")
	path = raw_input('> ')
	import_data(path)

	print("Import complete. You may now input commands. Enter 'help' for a list of commands.")
	while True:
		print('\nEnter a command.')
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
				continue
		elif command == 'shutter':
			# should probably add wrong input check too
			resp = raw_input('Automatically sort by shutter speed? (Y/N): ')
			if resp == 'Y':
				auto = True
			elif resp == 'N':
				auto = False
			else:
				print('Please only enter Y or N.')
				continue
			if not auto:
				def shutterkey(string):
					if '/' in string:
						num1, den1 = string.split('/')
						den1 = den1.strip()
						num1 = num1.strip()
						return float(num1) / float(den1)
					else:
						return float(string)
				inp = raw_input('Enter the speed(s) in seconds separated by "," to separate into, i.e 1/200,1/20,4: ')
				boundaries = inp.split(',')
				boundaries = sorted([val.strip() for val in boundaries], key=shutterkey)
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					shutter(auto, True, boundaries)
				elif copy == 'N':
					shutter(auto, False, boundaries)
				else:
					print('Please only enter Y or N.')
					continue
			else:
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					shutter(auto, True)
				elif copy == 'N':
					shutter(auto, False)
				else:
					print('Please only enter Y or N.')
					continue
		elif command == 'iso':
			resp = raw_input('Automatically sort by ISO? (Y/N): ')
			if resp == 'Y':
				auto = True
			elif resp == 'N':
				auto = False
			else:
				print('Please only enter Y or N.')
				continue
			if not auto:
				inp = raw_input('Enter the iso(s) separated by "," to separate into, i.e 100,200,800: ')
				boundaries = inp.split(',')
				boundaries = sorted([val.strip() for val in boundaries])
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					iso(auto, True, boundaries)
				elif copy == 'N':
					iso(auto, False, boundaries)
				else:
					print('Please only enter Y or N.')
					continue
			else:
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					iso(auto, True)
				elif copy == 'N':
					iso(auto, False)
				else:
					print('Please only enter Y or N.')
					continue
		elif command == 'aperture':
			resp = raw_input('Automatically sort by aperture? (Y/N): ')
			if resp == 'Y':
				auto = True
			elif resp == 'N':
				auto = False
			else:
				print('Please only enter Y or N.')
				continue
			if not auto:
				inp = raw_input('Enter the aperture(s) separated by "," to separate into, i.e 1.4,3.5,6,22: ')
				boundaries = inp.split(',')
				boundaries = sorted([val.strip() for val in boundaries], key=lambda x: float(x))
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					aperture(auto, True, boundaries)
				elif copy == 'N':
					aperture(auto, False, boundaries)
				else:
					print('Please only enter Y or N.')
					continue
			else:
				copy = raw_input('Keep copy of original files? (Y/N): ')
				if copy == 'Y':
					aperture(auto, True)
				elif copy == 'N':
					aperture(auto, False)
				else:
					print('Please only enter Y or N.')
					continue
		elif command == 'date':
			inp = raw_input('Enter "year", "month", or "day" to sort by: ')
			if inp != 'year' and inp != 'month' and inp != 'day':
				print('Please only enter "year", "month", or "day".')
				continue
			copy = raw_input('Keep copy of original files? (Y/N): ')
			if copy == 'Y':
				date(inp, True)
			elif copy == 'N':
				date(inp, False)
			else:
				print('Please only enter Y or N.')
		elif command == 'help':
			print("You're outta luck bub.")
		elif command == 'exit':
			return
		else:
			print("Please input a proper command.")

# gets all exif data from folder
def import_data(path):
	# weird input? Clarify. Right now, no home directory or beginning / needed.
	global main_path 
	main_path = os.path.expanduser("~") + '/' + path
	for file_name in os.listdir(main_path):
		try:
			if imghdr.what(main_path + '/' + file_name):
				exif = check_output(['exiv2', '-p', 's', main_path + '/' + file_name])
				one = exif.split('\n')
				# this may not be safe. Not sure if it's always 4 at the end. CHECK.
				two = one[:len(one) - 4]
				dic = {}
				for item in two:
					k, v = item.split(':', 1)
					dic[k.strip()] = v.strip()
				EXIF_INFO[file_name] = dic
		except:
			pass

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
	global EXIF_INFO
	main_path = os.path.expanduser("~") + '/' + path
	EXIF_INFO = {}
	import_data(path)
	print('Operation complete.')

# organize by image type, maybe allow more granularity (FINE, MEDIUM, etc.)
def type(copy):
	for image in EXIF_INFO:
		if imghdr.what(main_path + '/' + image) == 'jpeg':
			move_file(image, main_path + '/JPEG', copy)
		else:
			move_file(image, main_path + '/RAW', copy)
	print("Operation complete.")

# organize by shutter speed
def shutter(auto, copy, boundaries=None):
	for image in EXIF_INFO:
		shutter_speed = EXIF_INFO[image]["Exposure time"]
		if auto:
			move_file(image, main_path + '/' + 'SHUTTER' + shutter_speed.split(' ')[0].replace('/', 'x'), copy)
		else:
			if '/' in shutter_speed:
				num1, den1 = shutter_speed.split('/')
				den1 = den1.split(' ')[0].strip()
				num1 = num1.strip()
				speed1 = float(num1) / float(den1)
			else:
				speed1 = float(shutter_speed.split(' ')[0].strip())

			for i in range(len(boundaries)):
				if '/' in boundaries[i]:
					num2, den2 = boundaries[i].split('/')
					num2 = num2.strip()
					den2 = den2.strip()
					speed2 = float(num2) / float(den2)
				else:
					speed2 = float(boundaries[i].split('/')[0].strip())
				if speed1 <= speed2:
					move_file(image, main_path + '/' + 'SHUTTER' + boundaries[i].replace('/', 'x') + '-', copy)
					break
				if i == len(boundaries) - 1:
					move_file(image, main_path + '/' + 'SHUTTER' + boundaries[i].replace('/', 'x') + '+', copy)
	print("Operation complete.")

def iso(auto, copy, boundaries=None):
	for image in EXIF_INFO:
		iso = int(EXIF_INFO[image]["ISO speed"])
		if auto:
			move_file(image, main_path + '/' + 'ISO' + str(iso), copy)
		else:
			for i in range(len(boundaries)):
				bound_iso = boundaries[i]
				if iso <= int(bound_iso):
					move_file(image, main_path + '/' + 'ISO' + bound_iso + '-', copy)
					break
				if i == len(boundaries) - 1:
					move_file(image, main_path + '/' + 'ISO' + bound_iso + '+', copy)
	print("Operation complete.")

def aperture(auto, copy, boundaries=None):
	for image in EXIF_INFO:
		aperture = float(EXIF_INFO[image]["Aperture"].split('F')[1])
		if auto:
			move_file(image, main_path + '/F' + str(aperture), copy)
		else:
			for i in range(len(boundaries)):
				bound_aperture = float(boundaries[i])
				if aperture <= bound_aperture:
					move_file(image, main_path + '/F' + boundaries[i] + '-', copy)
					break
				if i == len(boundaries) - 1:
					move_file(image, main_path + '/F' + boundaries[i] + '+', copy)
	print("Operation complete.")

def date(time_type, copy):
	for image in EXIF_INFO:
		tim = time.strptime(EXIF_INFO[image]['Image timestamp'], '%Y:%m:%d %H:%M:%S')
		if time_type == 'year':
			move_file(image, main_path + '/' + str(tim.tm_year), copy)
		elif time_type == 'month':
			move_file(image, main_path + '/' + datetime.date(1900, tim.tm_mon, 1).strftime("%B") + str(tim.tm_year), copy)
			print(datetime.date(1900, tim.tm_mon, 1).strftime("%B"))
			print(tim.tm_mon)
		else:
			move_file(image, main_path + '/' + str(tim.tm_mday) + datetime.date(1900, 1, tim.tm_mon).strftime("%B") + str(tim.tm_year), copy)
	print("Operation complete.")

main()