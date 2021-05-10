import glob, os
import os.path
import eyed3
from pathlib import Path
from mp3_tagger import *
#from mutagen.easyid3 import ID3

def add_track_numbers_to_all_songs(data_folder):
    #data_folder = Path("H:/Plex/Media/Music1/")
    print(data_folder)
    need_to_update = []

    for artist in os.listdir(data_folder):
        if not os.path.isdir(artist):
            continue
        else:
            for album in os.listdir(data_folder / artist):
                albums_searched = "All Songs"
                if album.find(albums_searched) > -1:
                    try: 
                        # Add 0 to beginning of every track.
                        x = 0
                        for song in os.listdir(data_folder / artist / album):
                            if song.endswith('.mp3'):
                                x += 1
                                print(song)
                                #If the first character is not a number ie it doesn't have something assigned to it.
                                if not song[:1].isdigit():
                                    song_text = str(x) + ". " + song
                                    file_to_open = data_folder / artist / album / song
                                    new_file = data_folder /     artist / album / song_text
                                    print("File to open: " + str(file_to_open))
                                    print("New File to open: " + str(new_file))
                                    audio = MP3File(str(file_to_open))
                                    audio.set_version(VERSION_1)
                                    audio.track = str(x)
                                    audio.save()
                                    os.rename(file_to_open,new_file)
                    #except is likely to trigger when album.index() fails    
                    except:
                        if album.endswith('.mp3'):
                            for song in os.listdir(data_folder / artist / album):
                                if song.endswith('.mp3') and not song[:1].isdigit():
                                    # If its an actual album
                                    need_to_update.append((album + " / " + song))
                        else:
                            print("found non-album probably the cover.png")
                else:
                    if not(album == "cover.png" or album == "cover.jpg"): #ignore the case where it finds a cover.png item, we dont' care that we 'skipped' it
                        print(str(album) + " is not an `" + albums_searched + "` album, so it was skipped")

    print("Albums that Need Updating:\n")
    for x in need_to_update:
        print(x)

