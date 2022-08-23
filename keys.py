from datetime import date
from connection import Connection

class Key():
	_key_name = None
	_count = 0
	_connection = Connection()

	def __init__(self, key_name):
		self._key_name = key_name
		self._count = self.count(date.today())

		if not self._count:
			cursor = self._connection.connect()
			sql_insert = "INSERT INTO keyboard_key(name, count, date)\
										VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=name;"
			cursor.execute(sql_insert, (self._key_name, 1, date.today()))
			self._connection.disconnect(cursor)
		else:
			self.increment()


	def __repr__(self):
		return f'Instance of Key: (name: {self._key_name}, count: {self._count})'


	def increment(self):
		self._count += 1
		cursor = self._connection.connect()
		sql_update = "UPDATE keyboard_key SET count = %s\
									WHERE (name = %s AND date = %s);"
		cursor.execute(sql_update, (self._count, self._key_name, date.today()))

		self._connection.disconnect(cursor)


	def count(self, day=None):
		if not day:
			return self._count

		cursor = self._connection.connect()
		sql_query = "SELECT count FROM keyboard_key WHERE (name = %s AND date = %s);"
		cursor.execute(sql_query, (self._key_name, day))
		result = cursor.fetchone()
		self._connection.disconnect()

		if not result:
			print('No data from this date or invalid format.')
			return None
		else:
			return result['count']


class Keyboard():
	_keys = {}
	_connection = Connection()
	_count = 0

	def __repr__(self):
		return 'Instance of Keyboard'


	def add(self, keyboard_key):
		if keyboard_key not in self._keys:
			self._keys[keyboard_key] = Key(keyboard_key)
		else:
			self._keys[keyboard_key].increment()


	def count(self, day=date.today()):
		cursor = self._connection.connect()
		sql_query = "SELECT SUM(count) as total_count FROM keyboard_key WHERE date = %s;"
		cursor.execute(sql_query, (day,))
		result = cursor.fetchone()
		self._connection.disconnect(cursor)

		return result['total_count']


	def get_top_keys(self, day=date.today(), amount=5):
		cursor = self._connection.connect()
		sql_query = "SELECT name, count FROM keyboard_key\
								WHERE date = %s ORDER BY count DESC LIMIT %s;"
		cursor.execute(sql_query, (day, amount))
		result = cursor.fetchall()
		self._connection.disconnect()

		return result


	def get_keys_log(self, day=date.today()):
		cursor = self._connection.connect()
		sql_query = "SELECT name, count FROM keyboard_key\
								WHERE date = %s ORDER BY count DESC;"
		cursor.execute(sql_query, (day,))
		result = cursor.fetchall()
		self._connection.disconnect()

		return result


	def get_interval_log(self, start, end):
		cursor = self._connection.connect()
		sql_query = "SELECT date, SUM(count) AS count\
								FROM keyboard_key\
								WHERE date BETWEEN %s AND %s\
								GROUP BY date ORDER BY date;"
		cursor.execute(sql_query, (start, end))
		result = cursor.fetchall()
		self._connection.disconnect()

		return result
