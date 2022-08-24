import json
import os
try:
	import mysql.connector
except ImportError as err:
  raise Exception("[!] Error: Modules not found. Please run 'pipenv sync'") from err

class Connection():
	_connection = None

	def connect(self):
		try:
			mysql_configs = json.loads(os.getenv('MYSQL_CONFIG'))
			connection = mysql.connector.connect(**mysql_configs)
		except TypeError:
			raise Exception("[!] Can't load .env configs")
		except mysql.connector.Error as error:
			match error.errno:
				case 1045:
					raise Exception(f"[!] Access denied to user: {mysql_configs['user']}") from error
				case 1049:
					raise Exception(f"[!] Can't connect to database: {mysql_configs['database']}") from error
				case _:
					raise Exception(error) from error

		self._connection = connection
		return self._connection.cursor(dictionary=True)


	def disconnect(self, cursor_to_close=None):
		if cursor_to_close:
			cursor_to_close.close()
		self._connection.commit()
		self._connection.close()
