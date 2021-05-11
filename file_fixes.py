import csv_handler as csv
BAD_FILE_ELEMENTS = csv.get_contents_of_file('C:/Users/nick4/Desktop/SongFixes/error_keys.csv')
LIST_OF_REMOVE_KEYWORDS = csv.get_contents_of_file('C:/Users/nick4/Desktop/SongFixes/tags.csv')

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

def remove_unwanted_tags(song):
	for keyword in LIST_OF_REMOVE_KEYWORDS:
		song = song.replace(keyword, "")
	song = song.strip()
	return song

