import json
import os
import sys
import re

from connection import Connection

if len(sys.argv) != 2:
	print('expected 1 arguments, but got', len(sys.argv) - 1)
	print('run: pipenv run python3 bin/export_old_data.py full/path/to/old_data/')
	sys.exit()

connection = Connection()
cursor = connection.connect()
directory = sys.argv[1] if sys.argv[1].endswith('/') else sys.argv[1] + '/'
EXP_REGEX = re.compile(r'daily_log_(?P<date>\d{4}-\d{2}-\d{2}).json')
files = list(filter(EXP_REGEX.match, os.listdir(directory)))
files.sort()

count_files = len(files)
print(count_files, 'files were found.')

for index, filename in enumerate(files):
	os.system('clear')
	print(f'insert files data: {index + 1}/{count_files}')
	with open(directory + filename, 'r', encoding='UTF-8') as file:
		data = json.load(file)
		date = re.search(EXP_REGEX, filename).group('date')

		for name in data['keys_pressed']:
			count = data['keys_pressed'][name]
			SQL_INSERT = "INSERT INTO keyboard_key(name, count, date)\
										VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=name;"
			cursor.execute(SQL_INSERT, (name, count, date))

connection.disconnect(cursor)
