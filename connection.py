import json
import os
import sys
import mysql.connector

class Connection():
	_connection = None

	def connect(self):
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


	def disconnect(self, cursor_to_close=None):
		if cursor_to_close:
			cursor_to_close.close()
		self._connection.commit()
		self._connection.close()
