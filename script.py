import glob, os
import os.path
from pathlib import Path
#from mutagen.easyid3 import ID3


data_folder = Path("H:/Plex/TestSongs/")

import eyed3

#DIR_HOME = 'H:\\Plex\\All Songs4\\'
'''
print(DIR_HOME)

for filename in os.listdir(data_folder):
    
    if filename.endswith('.mp3'):
        file_to_open = data_folder / filename
        print(file_to_open)
        audio = eyed3.load(file_to_open)
        if(audio == None):
            print("Weird stuff here! -------------------")
        else:
            print(audio.tag.artist)

'''
allSame = input("Same Artist and Album? (y/n): ")
allSameAlbum = input("Same Album? (y/n): ")
allSameArtist = input("Same Artist? (y/n): ")
Artist = input("Enter Artist Name: ")
Title = input("Enter Song Title: ")
Album = input("Enter Album: ")
for filename in os.listdir(data_folder):
    if filename.endswith('.mp3'):
        file_to_open = data_folder / filename
        print(file_to_open)
        Title = input("Enter Song Title: ")
        if(allSame == 'n'):
            if(allSameArtist == 'n'):
                Artist = input("Enter Artist Name: ")
            if(allSameAlbum == 'n'):
                Album = input("Enter Album: ")
        audio = eyed3.load(file_to_open)
        if(audio == None):
            print("FUNKY SHIT YAAA")
        else:
            audio.tag.album_artist = Artist
            audio.tag.album = Album
            audio.tag.title = Title
            audio.tag.artist = Artist
            audio.tag.save()
            thing = Artist + " - " + Title + ".mp3"
            file_to_rename = data_folder / thing
            new_name = data_folder / thing
            os.rename(file_to_open,file_to_rename)


