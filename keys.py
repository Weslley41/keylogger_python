from datetime import date
import json
import os
import sys
import mysql.connector

class Key():
	_key_name = None
	_count = 0
	_connection = None

	def __init__(self, key_name):
		self._key_name = key_name
		cursor = self._connect()
		sql_query = "SELECT count FROM keyboard_key\
								WHERE(name=%s AND date=%s);"
		cursor.execute(sql_query, (self._key_name, date.today()))
		result = cursor.fetchone()

		if not result:
			sql_insert = "INSERT INTO keyboard_key(name, count, date)\
										VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=name;"
			cursor.execute(sql_insert, (self._key_name, 0, date.today()))
		else:
			self._count = result['count']

		self._disconnect(cursor)


	def __repr__(self):
		return f'Instance of Key: (name: {self._key_name}, count: {self._count})'


	def _connect(self):
		try:
			mysql_configs = json.loads(os.getenv('MYSQL_CONFIG'))
			connection = mysql.connector.connect(**mysql_configs)
		except TypeError:
			print("Can't load .env configs")
			sys.exit()
		except mysql.connector.Error as error:
			match error.errno:
				case 1045:
					print(f"Access denied to user: {mysql_configs['user']}")
					sys.exit()
				case 1049:
					print(f"Can't connect to database: {mysql_configs['database']}")
					sys.exit()
				case _:
					print(error)
					sys.exit()

		self._connection = connection
		return self._connection.cursor(dictionary=True)


	def _disconnect(self, cursor_to_close=None):
		if cursor_to_close:
			cursor_to_close.close()
		self._connection.commit()
		self._connection.close()


	def increment(self):
		self._count += 1
		cursor = self._connect()
		sql_update = "UPDATE keyboard_key SET count = %s\
									WHERE (name = %s AND date = %s);"
		cursor.execute(sql_update, (self._count, self._key_name, date.today()))

		self._disconnect(cursor)


	def count(self, day=None):
		if not day:
			return self._count

		cursor = self._connect()
		sql_query = "select count FROM keyboard_key WHERE (name = %s AND date = %s);"
		cursor.execute(sql_query, (self._key_name, day))
		result = cursor.fetchone()

		if not result:
			print('No data from this date or invalid format.')
			return 0
		else:
			return result['count']


class Keyboard():
	_keys = {}

	def __repr__(self):
		return 'Instance of Keyboard'


	def add(self, keyboard_key):
		if keyboard_key not in self._keys:
			self._keys[keyboard_key] = Key(keyboard_key)
		else:
			self._keys[keyboard_key].increment()


	def get_count(self, day=None):
		return 0

# For tests
# key = Key('enter')
# print(key)
# key.increment()
# print(key)
# print(key.count('2022-08-22'))
# print(key.count('2022-08-21'))
