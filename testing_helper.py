from pathlib import Path
import os
import shutil

home_dir = Path("C:/Users/nick4/Desktop/SongFixes/")
raw_songs = "test-dir/raw-songs/"
backup_songs = "test-dir/copy-raw/"
output_songs = "test-dir/output/"

#copies files from backup copy location to raw-songs
def setup():
    src = home_dir / backup_songs
    dest = home_dir / raw_songs
    output = home_dir / output_songs
    if os.path.exists(output):
        shutil.rmtree(output)
    if os.path.exists(dest):
        teardown()
    os.mkdir(output)
    shutil.copytree(src, dest)
    

# removes raw-songs folder and all subfolders & items
def teardown():
    raw_data = home_dir / raw_songs
    if os.path.exists(raw_data):
        shutil.rmtree(raw_data)
    