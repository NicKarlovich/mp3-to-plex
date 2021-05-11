from pathlib import Path
import testing_helper as th
import flippy as flip

TESTING = True

if TESTING:
    data_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/raw-songs/")
    output_folder = Path("C:/Users/nick4/Desktop/SongFixes/test-dir/output/")
else:
    data_folder = Path("H:/Plex/TestSongs/")
    output_folder = Path("H:/Plex/Media/Music/")
# run some code
print("lets do it")
if TESTING:
    th.setup()
print('run?')
flip.format_albums(data_folder, output_folder)
flip.format_songs(data_folder, output_folder, False, None, None)

#apply numbers to tracks?

if TESTING:
    th.teardown()
    