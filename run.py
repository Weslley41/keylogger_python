def main():
	"""
	Main function - Key logger
	...
	Reads pressed keys and save them to a log file.
	"""
	try:
		import keyboard, json
		from datetime import date
	except ImportError:
		print("[!] Error: Modules not found. Please run 'pip install -r requirements.txt'")
		exit()

	try:
		today = date.today().isoformat()
		filename = f"daily_log_{today}.json"
		log_file_r = open('system_logs/' + filename, "r")
	except FileNotFoundError:
		log_file_w = open('system_logs/' + filename, "w")
		log_file_w.write('{"counted_keys": 0, "keys_pressed": {}}\n')
		log_file_w.close()
		log_file_r = open('system_logs/' + filename, "r")

	log = json.load(log_file_r)
	while True:
		key_pressed = keyboard.read_key()
		if (not keyboard.is_pressed(key_pressed)):
			log["counted_keys"] += 1
			try:
				log['keys_pressed'][key_pressed] += 1
			except KeyError:
				log['keys_pressed'][key_pressed] = 1

			log_file_w = open('system_logs/' + filename, "w")
			json.dump(log, log_file_w)


if (__name__ == '__main__'):
	import os
	if (os.getuid() != 0):
		print("Please run as root.")
	else:
		os.chdir(os.path.dirname(__file__))
		main()
