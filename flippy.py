import glob, os
import os.path
import traceback
from pathlib import Path
import add_track_numbers as atn
import csv_handler as csv
from mutagen.easyid3 import EasyID3
from tinytag import TinyTag
from mp3_tagger import *

data_folder = Path("H:/Plex/TestSongs/")
output_folder = Path("H:/Plex/Media/Music/")

import eyed3

#artist = "None"
#title = "None"
#album = "None"

SONG_TITLE_HELPER = True
ALPHABET = csv.get_contents_of_file("H:/Desktop/SongFixes/alphabet.csv")
LIST_OF_REMOVE_KEYWORDS = csv.get_contents_of_file('H:/Desktop/SongFixes/tags.csv')
BAD_FILE_ELEMENTS = csv.get_contents_of_file('H:/Desktop/SongFixes/error_keys.csv')

root, albums, songs = next(os.walk(data_folder)) #os.walk returns 3 lists, root, dirs and files

def remove_mp3_file_extension(filename):
    if filename[-4:] == ".mp3":
        filename = str(filename[:-4])
    return filename

def detect_weird_unicode_chars(filename):
    for entry in BAD_FILE_ELEMENTS:
        try:
            if(filename.find(entry) > -1):
                print("file: " + str(filename) + "  has invalid unicode chars.  script will not work, needs manual handling")
                return True
        except:
            #traceback.print_exc()
            print("file: " + str(filename) + "  has invalid unicode chars.  script will not work, needs manual handling")
            return True
    return False

#Expects file naming scheme of Artist - Title, if song number is included it will be wrong.
# If value does have song number use parse_album_song_text instead
def parse_song_text(filename):
    filename = remove_mp3_file_extension(filename)
    if(filename.count("-") > 0):
        dash_idx = filename.index("-")
        guess_artist = (str(filename))[:dash_idx - 1]
        guess_title = (str(filename))[dash_idx + 2:]
    else:
        guess_artist = "Couldn't Guess Artist"
        guess_title = filename
    return guess_title, guess_artist

def parse_album_song_text(filename):
    filename = remove_mp3_file_extension(filename)
    # Assuming we have enough dashes to identify song number, artist and title
    if filename.count("-") > 1:
        dash_idx = filename.index("-")
        try:
            guess_number = int((str(filename))[:dash_idx - 1])
        except:
            guess_number = -1
        filename = filename[dash_idx + 2:] #removing already parsed value
        dash_idx = filename.index("-") #find next dash
        guess_artist = (str(filename))[:dash_idx - 1]
        guess_title = (str(filename))[dash_idx + 2:]

    elif filename.count("-") == 1: # Assuming missing song number
        dash_idx = filename.index("-")
        guess_number = -1
        guess_artist = (str(filename))[:dash_idx - 1]
        guess_title = (str(filename))[dash_idx + 2:]

    elif filename.count("-") < 1: # no dashes found
        guess_number = -1
        guess_artist = "Couldn't Guess Artist"
        guess_title = filename

    return guess_number, guess_title, guess_artist

def check_artist(guess_artist, previous_artist, artist):
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
    if album == "None":
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
        print("index:     " + "".join(x))
        print("key:       " + "".join(y))
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

def check_title(guess_title, title):
    guess = ""
    while(guess != "y" and guess != "n"):
        guess = input("Is This The Song Title You Expect? `" + str(guess_title) + "` (y/n)")
        if guess == "n" and SONG_TITLE_HELPER:
            title = title_helper(guess_title)
        elif guess == "n" and not SONG_TITLE_HELPER:
            title = input("Enter Song Title: ")
        elif guess == "y":
            title = guess_title
    return title

def valid_audio_file(file_to_open):
    audio = MP3File(str(file_to_open))
    audio.set_version(VERSION_1)
    if(audio == None):
        print("File is corrupt or not openable.")
        print("file_to_open: " + str(file_to_open))
        return False
    return True

'''
def valid_audio_file(file_to_open):
    audio = eyed3.load(file_to_open)
    if(audio == None):
        print("File is corrupt or not openable.")
        print("file_to_open: " + str(file_to_open))
        return False
    return True
'''

def assign_audio_tags(audio, file_to_open, album, title, artist, number=-1):
    audio.set_version(VERSION_1)
    audio.album = album
    audio.song = title
    audio.artist = artist
    audio.year = "" #clear year entry, leftover data from MediaHuman we don't want.
    audio.set_version(VERSION_2)
    audio.song = title #apply title to both versions to ensure it actually "sets"
    audio.band = artist
    if(number != -1):
        audio.track = str(number)
    audio.save()

'''
def assign_audio_tags(audio, file_to_open, album, title, artist, number=-1):
    audio.tag.album_artist = artist
    audio.tag.album = album
    audio.tag.title = title
    audio.tag.artist = artist
    if(number != -1):
        audio.tag.track_num = number
    audio.tag.save()
    return audio
'''
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
                print("skipping loop, changes not saved")
            else:
                print("y or n expected")
    else: 
        os.rename(file_to_open,new_file)

def format_albums(album_folder, album, artist, title):
    for album_iter in albums:
        folder = album_folder / album_iter
        print(folder)
        guess = ""
        output = album_iter
        while(guess != "y"):
            guess = input("Does this album follow the correct standards?(y/n, ? for standard)")
            if(guess == "?"):
                print("Standard album organization is `{Artist name} - {Album Name}")
            elif(guess == "n"):
                output = input("Please rename the folder with the correct standards:")
            elif(guess != "y"):
                print('y or n expected')
            if(guess == "n" or guess == "y"):
                dash_idx = output.find("-")
                if dash_idx < 0:
                    print("couldn't find album, doesn't follow standards, try again")
                else:
                    album = (str(output))[dash_idx + 2:]
                    print("ALBUM: " + str(album))
                    guess = input("Is this the album you expect?(y/n) ")
            
    for album_iter in albums:
        folder = album_folder / album_iter
        format_songs(folder, True, album, artist, title)

    for album_iter in albums:
        x = (album_folder / album_iter)
        os.rmdir(x)
            

def format_songs(song_folder, specific_album, album, artist, title):
    if not specific_album:
        album = "None"
    #print(songs)
    for song in os.listdir(song_folder):
        file_to_open = song_folder / song
        #Check that it is a .mp3
        if not song.endswith('.mp3'):
            print("invalid file found")
            continue #try next value, skip iteration
        for keyword in LIST_OF_REMOVE_KEYWORDS:
            song = song.replace(keyword, "")
        song = song.strip()

        #skip song item if it has bad unicode that would cause script to fail later.
        if detect_weird_unicode_chars(song):
            continue
        
        # print here needed for output.
        print(song)
        if specific_album:
            guess_number, guess_title, guess_artist = parse_album_song_text(song)
        else:
            guess_title, guess_artist = parse_song_text(song)
            guess_number = -1

        previous_artist = artist
        artist = check_artist(guess_artist, previous_artist, artist)

        album = check_album(album)

        title = check_title(guess_title, title)
        
        if not valid_audio_file(file_to_open):
            continue
        audio = MP3File(str(file_to_open))
        # audio = assign_audio_tags(audio, file_to_open, album, title, artist, guess_number)
        assign_audio_tags(audio, file_to_open, album, title, artist, guess_number)

        save_to_folder = create_album_folder(artist, album, output_folder)
        create_new_file(artist, title, file_to_open, save_to_folder, guess_number)
        

format_albums(data_folder, "None", "None", "None")
format_songs(data_folder, False, "None", "None", "None")

guess = ""
while(guess != "y" and guess != "n"):
    guess = input("Add track numbers to All Songs Albums? (y/n)")
if guess == "y":
    atn.add_track_numbers_to_all_songs(output_folder)
