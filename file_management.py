from mp3_tagger import *
import os
import eyed3

def valid_audio_file(file_to_open):
	audio = MP3File(str(file_to_open))
	audio.set_version(VERSION_1)
	if(audio == None):
		print("File is corrupt or not openable.")
		print("file_to_open: " + str(file_to_open))
		return False
	return True

def create_album_folder(artist, album, output_folder):
	temp = artist + " - " + album
	save_to_folder = output_folder / artist / temp
	if not os.path.isdir(save_to_folder):
		os.makedirs(save_to_folder)
	return save_to_folder

def create_new_file(artist ,title, file_to_open, save_to_folder, number=-1):
	if(number != -1):
		file_name = str(number) + ". " + artist + " - " + title + ".mp3"
	else:
		file_name = artist + " - " + title + ".mp3"
	new_file = save_to_folder / file_name
	if os.path.exists(new_file):
		guess = ""
		while(guess != "n" and guess != "y"):
			guess = input("The file: " + str(new_file)+ " already exists, do you want to continue and override? (y/n)")
			if guess == "y":
				os.remove(new_file)
				os.rename(file_to_open,new_file)
			elif guess == "n":
				print("skipping file, changes not saved")
			else:
				print("y or n expected")
	else: 
		os.rename(file_to_open,new_file)




def assign_audio_tags(audio, album, title, artist, number=-1):
	audio.set_version(VERSION_1)
	audio.album = album
	audio.song = title
	audio.artist = artist
	audio.year = "" #clear year entry, leftover data from MediaHuman we don't want.
	audio.set_version(VERSION_2)
	audio.song = title #apply title to both versions to ensure it actually "sets"
	audio.band = artist
	audio.comment = "" #previous deleted, but that might've done some weird things to file
	audio.genre = ""
	audio.set_version(VERSION_1)
	if number != -1:
		audio.track = str(number)
	else:
		del audio.track
	audio.save()