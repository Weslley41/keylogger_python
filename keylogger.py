from keys import Keyboard

class Keylogger:

	def __init__(self):
		self._keyboard = Keyboard()


	def __repr__(self):
		return "Instance of Keylogger"


	def runner(self):
		# run the program
		pass


	def get_log(self, day=None):
		# returns log of day in JSON format
		pass


	def get_interval_log(self, start, end):
		# returns log of interval in JSON format
		pass
