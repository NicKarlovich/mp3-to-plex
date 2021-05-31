import os
from pathlib import Path
import add_track_numbers as atn
import csv_handler as csv
import file_fixes as ff
import file_management as fm
from mutagen.easyid3 import EasyID3
from tinytag import TinyTag
from mp3_tagger import *
import eyed3
'''
TESTING = True

if TESTING:
	data_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/raw-songs/")
	output_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/output/")
else:
	data_folder = Path("H:/Plex/TestSongs/")
	output_folder = Path("H:/Plex/Media/Music/")
'''


#artist = "None"
#title = "None"
#album = "None"

SONG_TITLE_HELPER = True
ALPHABET = csv.get_contents_of_file("C:/Users/nick4/Desktop/SongFixes/alphabet.csv")



 #os.walk returns 3 lists, root, dirs and files

#Expects file naming scheme of Artist - Title, if song number is included it will be wrong.
# If value does have song number use parse_album_song_text instead
def parse_song_text(filename):
	filename = ff.remove_mp3_file_extension(filename)
	if(filename.count("-") > 0):
		dash_idx = filename.index("-")
		guess_artist = (str(filename))[:dash_idx - 1]
		guess_title = (str(filename))[dash_idx + 2:]
	else:
		guess_artist = "Couldn't Guess Artist"
		guess_title = filename
	return guess_title, guess_artist

#attempts to figure out album and artist by album folder, if not in standard organization returns false and no info.
def parse_album(foldername):
	dash_idx = foldername.find("-")
	if dash_idx < 0:
		print("couldn't find album, doesn't follow standards, try again")
		return False, None, None
	else:
		album = (str(foldername))[dash_idx + 2:]
		artist = (str(foldername))[:dash_idx - 1]
		return True, artist, album

def check_artist(guess_artist, previous_artist):
	guess = ""
	stage = 0
	#while(guess != "n" and guess != "y"):
	guess = input("Is this the artist you expect? `" + str(guess_artist) + "` (y/n)")
	while(stage < 2):
		if guess == "n":
			if stage == 0:
				if previous_artist == "None":
					artist = input("Enter Artist Name: ")
					stage = 2
				else:
					guess = input("Use Previous Artist? `" + str(previous_artist) + " `(y/n)")
					stage = 1
			elif stage == 1:
				artist = input("Enter Artist Name: ")
				stage = 2
		elif guess == "y":
			if stage == 0:
				artist = guess_artist
			if stage == 1:
				artist = previous_artist #redundant but here for clarity
			stage = 2
		else:
			guess = input("Is this the artist you expect? `" + str(guess_artist) + "` (y/n)")
			print("y or n expected")
	return artist

def check_album(album):
	guess = ""
	if album == None:
		album = input("Enter Album Name: ")
	else: 
		while (guess != "y" and guess != "n"):
			guess = input("Use Previous Album? `" + str(album) + "` (y/n)")
			if guess == "n":
				album = input("Enter Album Name: ")
			elif guess == "y":
				album = album #redundant but for clarity of logic flow
			else:
				print("y or n expected")
	if album == "a": #shortcut, a "textexpands" into All Songs
		album = "All Songs"
	return album

def title_helper(guess_title):
	spaces = []
	temp = guess_title.find(" ")
	#copy = guess_title
	count = 0
	while(temp > -1):
		spaces.append(temp)
		count = temp + 1
		#guess_title = copy[temp + 1:]
		temp = guess_title.find(" ", count)
	space_dict = {}
	space_dict[""] = -1
	x = list(" "*(len(guess_title)))
	y = list(" "*(len(guess_title)))
	#print(spaces)
	for idx, val in enumerate(spaces):
		space_dict[ALPHABET[idx]] = val
		x[val] = "^"
		y[val] = ALPHABET[idx]
	guess = ""
	while(guess != "y"):
		print("ORIGINAL: `" + str(guess_title) + "`")
		print("index:	 " + "".join(x))
		print("key:	   " + "".join(y))
		print("------------------")
		split_key = input("Enter Split Key (or newline to exit helper): ")
		while(split_key not in space_dict):
			print("Invalid Key Entered, options are: [" + " ".join(list(space_dict.keys())) + "]")
			split_key = input("Enter Split Key (or newline to exit helper): ")
		index_to_cut = space_dict[split_key]
		if(index_to_cut < 0): #exited helper
			t = input("Enter Title: ")
		else:
			t = guess_title[:index_to_cut]
		print("TITLE: `" + str(t) + "`")
		guess = input("Is this the correct title?(y/n) ")
	return t

def check_title(guess_title):
	guess = ""
	while(guess != "y" and guess != "n"):
		guess = input("Is This The Song Title You Expect? `" + str(guess_title) + "` (y/n)")
		if guess == "n" and SONG_TITLE_HELPER:
			guess_title = title_helper(guess_title)
		elif guess == "n" and not SONG_TITLE_HELPER:
			guess_title = input("Enter Song Title: ")
		#elif guess == "y":
			#do nothing
	return guess_title

def format_albums(album_folder, output_folder):
	#for each album in the input directory
	root, albums, songs = next(os.walk(album_folder))
	for album_iter in albums:
		folder = album_folder / album_iter
		if os.path.isdir(folder):
			guess = ""
			output = album_iter
			while(guess != "y"):
				print(output)
				guess = input("Does this album follow the correct standards?\nStandard album organization is `{Artist name} - {Album Name}`, no dashes in artist or album name\n(y/n): ")
				success, artist, album = parse_album(output)
				if(guess == "y" and success):
					print("ALBUM: `" + str(album) + "`")
					album_guess = input("Is this the album you expect?(y/n): ")
					print("ARTIST: `" + str(artist) + "`")
					artist_guess = input("Is this the artist you expect?(y/n): ")
					if (album_guess == "y" and artist_guess == "y"):
						guess = "y" #redundant but kept for clarity
					else:
						guess = "n"
						output = input("Please rename the folder with the correct standards:")
				else:
					output = input("Please rename the folder with the correct standards:")
		folder = album_folder / album_iter
		format_songs(folder, output_folder, True, album, artist)
	#goes into each album with previous knowledge and begins building songs

	#once we're all done, delete all old album directories
	for album_iter in albums:
		x = (album_folder / album_iter)
		os.rmdir(x)
			
def format_songs(song_folder, output_folder, specific_album, album, artist):
	previous_album = None
	previous_artist = None
	songs = os.listdir(song_folder)
	if len(songs) == 0:
		print("There are no songs in this folder to edit")
		return
	for song in os.listdir(song_folder):
		file_to_open = song_folder / song
		#Check that it is a .mp3
		if not song.endswith('.mp3'):
			print("invalid file found")
			continue #try next song, skip iteration

		song = ff.remove_unwanted_tags(song)

		#skip song item if it has bad unicode that would cause script to fail later.
		if ff.detect_weird_unicode_chars(song):
			continue #skip this for loop iteration
		
		# print here needed for output.
		print(song)
		guess_title, guess_artist = parse_song_text(song)
		guess_number = -1
		if specific_album:
			if not(guess_artist == artist):
				print("Artist of album doesn't match guessed artist of track")
				print("Beginning individual artist check")
				#TODO this doesn't actually do anything
			else:
				# skipping artist check
				print("")
			# specific album means skipping album check as well.
		else:
			previous_artist = artist
			artist = check_artist(guess_artist, previous_artist)
			
			album = check_album(previous_album)
			previous_album = album

		title = check_title(guess_title)
		
		if not fm.valid_audio_file(file_to_open):
			continue
		audio = MP3File(str(file_to_open))
		print(str(file_to_open))
		# audio = assign_audio_tags(audio, file_to_open, album, title, artist, guess_number)
		fm.assign_audio_tags(audio, album, title, artist)

		save_to_folder = fm.create_album_folder(artist, album, output_folder)
		fm.create_new_file(artist, title, file_to_open, save_to_folder, guess_number)
