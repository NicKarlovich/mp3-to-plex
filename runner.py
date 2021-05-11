from pathlib import Path
import testing_helper as th
import flippy as flip
import add_track_numbers as atn

TESTING = False

if TESTING:
    data_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/raw-songs/")
    output_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/output/")
else:
    data_folder = Path("H:/Plex/TestSongs/")
    output_folder = Path("H:/Plex/Media/Music - Copy/")
# run some code

print("lets do it")
if TESTING:
    th.setup()
print('run?')
flip.format_albums(data_folder, output_folder)
flip.format_songs(data_folder, output_folder, False, None, None)

#apply numbers to tracks?
#add track numbers to All Songs Albums
# program will not be adding numbers to albums with custom names
g = input("Would you like backreference to ensure that track numbers are added to all songs, this will take some time (y/n): ")
while (g != "y" or g !="n"):
    print("please enter y or n")
    g = input("Would you like backreference to ensure that track numbers are added to all songs, this will take some time (y/n): ")
if g == "y":
    atn.add_track_numbers_to_all_songs(output_folder, True)
else: 
    atn.add_track_numbers_to_all_songs(output_folder, False)
    print("track numbers only added to obvious new entries")
    #do nothing

if TESTING:
    th.teardown()
    