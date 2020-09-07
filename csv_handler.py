import csv

def get_contents_of_file(f):
    with open(f, 'r', encoding='utf-8') as csv_file:
        words = csv.reader(csv_file)
        return next(words)