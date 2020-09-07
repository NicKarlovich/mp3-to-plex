import glob, os
import os.path
from pathlib import Path
#from mutagen.easyid3 import ID3

data_folder = Path("H:/Plex/TestSongs/")
output_folder = Path("H:/Plex/Media/Music/")

import eyed3

artist = "None"
title = "None"
album = "None"
list_of_remove_keywords = {"(Official Video)", "[Official Video]",
            "(Audio)", "(Official Audio)", "(lyrics)", "[Official Music Video]", "(Official Music Video)",
            "(Mashup)", "(Lyric Video)", "(OFFICIAL MUSIC VIDEO)", "[OFFICIAL MUSIC VIDEO]", "(HQ)", "(HD)", "(VIP)",
            "(Radio Edit)", "(EXPLICIT)", "(Uncensored and Lyrics)", "(Lyrics)", ".mp3", "(Offical Album)",
            "[Offical Album]", "[Full Album]", "(Full Album)"}

for filename in os.listdir(data_folder):
    if filename.endswith('.mp3'):
        print("\n")
        try:
            dash_idx = filename.index("-") #Assuming that inputted file follows: Artist - Title setup.
            guess_artist = (str(filename))[:dash_idx - 1]
            guess_title = (str(filename))[dash_idx + 1:]
        except ValueError:
            #dash_idx = 1
            guess_artist = "Couldn't Guess Artist"
            guess_title = filename
            if guess_title[-4:] == ".mp3":
                guess_title = str(filename[:-4])
            else:
                guess_title = "Couldn't Guess Title"
        
        for keyword in list_of_remove_keywords:
            guess_artist = guess_artist.replace(keyword,"")
            guess_title = guess_title.replace(keyword,"")
        guess_artist = guess_artist.strip()
        guess_title = guess_title.strip()
            
        file_to_open = data_folder / filename
        print("filename: " + str(file_to_open))
        guess = ""
        while (guess != "n" and guess != "y"):
            if artist == "None":
                guess = input("Is This The Artist You Expect? `" + str(guess_artist) + "` (y/n)")
                if guess == "n":
                    artist = input("Enter Artist Name: ")
                elif guess == "y":
                    artist = guess_artist
                else:
                    print("y or n expected")
            else:
                same_artist_bool = ""
                guess = input("Is This The Artist You Expect? `" + str(guess_artist) + "` (y/n)")
                if guess == "n":
                    while (same_artist_bool != "n" and same_artist_bool != "y"):
                        same_artist_bool = input("Use Previous Artist? `" + str(artist) + " `(y/n)")
                        if same_artist_bool == "n":
                            artist = input("Enter Artist Name: ")
                        elif same_artist_bool != "y":
                            print("y or n expected")
                elif guess == "y":
                    artist = guess_artist
                else:
                    print("y or n expected")
    
        # intial case, or if we know if we changed artists we probably want a different album as well.
        if album == "None" or same_artist_bool == "n":
            album = input("Enter Album Name: ")
        else: 
            same_album_bool = ""
            while (same_album_bool != "y" and same_album_bool != "n"):
                same_album_bool = input("Use Previous Album? `" + str(album) + "` (y/n)")
                if same_album_bool == "n":
                    album = input("Enter Album Name: ")
                if same_album_bool != "y":
                    print("y or n expected")

        # Shortcut                
        if album == "a":
            album = "All Songs"
        guess = ""
        while(guess != "y" and guess != "n"):
            guess = input("Is This The Song Title You Expect? `" + str(guess_title) + "` (y/n)")
            if guess == "n":
                title = input("Enter Song Title: ")
            if guess == "y":
                title = guess_title
            

        audio = eyed3.load(file_to_open)
        if(audio == None):
            print("File is corrupt or not openable.")
            print("file_to_open: " + str(file_to_open))
        else:
            audio.tag.album_artist = artist
            audio.tag.album = album
            audio.tag.title = title
            audio.tag.artist = artist
            audio.tag.save()
            # file_name = artist + " - " + title + ".mp3"
            
            temp = artist + " - " + album
            save_to_folder = output_folder / artist / temp
            #save_to_album_folder = save_to_artist_folder / temp
            if not os.path.isdir(save_to_folder):
                os.makedirs(save_to_folder)

            file_name = artist + " - " + title + ".mp3"
            new_file = save_to_folder / file_name
            if os.path.exists(new_file):
                temp = ""
                while(temp != "n" and temp != "y"):
                    temp = input("The file: " + str(new_file)+ " already exists, do you want to continue and override? (y/n)")
                    if temp == "y":
                        os.remove(new_file)
                        os.rename(file_to_open,new_file)
                    elif temp != "n":
                        print("y or n expected")
            else: 
                os.rename(file_to_open,new_file)