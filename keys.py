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


	def get_count(self, day=None):
		if not day:
			return self._count

		return 0


class Keyboard():
	_keys = []
	_count = 0

	def __init__(self):
		# Instance all keys on list
		pass


	def __repr__(self):
		return 'Instance of Keyboard'


	def get_count(self, day=None):
		if not day:
			return self._count

		return 0

# For tests
key = Key('enter')
key.connect()
key.disconnect()
