
class Key():
	_key_code = None
	_key_name = None
	_count = 0

	def __init__(self, key_code):
		self._key_code = key_code


	def __repr__(self):
		return f'Instance of Key: (code: {self._key_code}, name: {self._key_name})'


	def increment(self):
		self._key_code += 1


	def get_count(self, day=None):
		if not day:
			return self._count


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
