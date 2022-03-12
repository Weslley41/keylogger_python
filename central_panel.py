import json
import os
from datetime import date
from time import sleep
from operator import itemgetter
from platform import system


def main():
	"""
	Main function - Panel
	...
	Show menu and call functions.
	"""
	today = date.today().isoformat()
	filename = f"daily_log_{today}.json"
	try:
		log_file_r = open('system_logs/' + filename, "r")
		log = json.load(log_file_r)
	except FileNotFoundError:
		print(f"# Log file not found. Exiting...")
		exit()

	clear()

	while True:
		choice = menu(today, log["counted_keys"])
		if (choice == '1'):
			show_top_keys(log["keys_pressed"])
		elif (choice == '2'):
			while (get_log() == '2'):
				get_log()
		elif (choice == '3'):
			get_graphic()
		elif (choice == '0'):
			exit()
		else:
			print('Invalid choice.')
			sleep(1)
			clear()


def clear():
	""" Clear the screen """
	if (system() == 'Windows'):
		os.system('cls')
	else:
		os.system('clear')


def menu(today, counts):
	"""
	Show menu
	...
	Return user choice.
	"""
	print(' Menu '.center(50, '-'))
	print(f'Today: {today} - counted keys: {counts}')
	print("""
	1. Show top keys
	2. Get log file
	3. Get weekly graphic
	0. Exit
	""")

	choice = input('--| Please enter your choice: ')

	return choice


def show_top_keys(keys):
	""" Show top5 keys most pressed """
	clear()
	print('# Top5 keys most-used:')
	keys_pressed = sorted(keys.items(), key=itemgetter(1), reverse=True)
	for index, item in enumerate(keys_pressed[:10]):
		index = str(index + 1)
		print(f'{index.rjust(2)}º: {item[1]} - {item[0]}')


def get_log():
	""" Get a log of day, saved as file """
	clear()
	print('Enter 0 for back to menu.')
	day = input('Enter a day (YYYY-MM-DD): ')
	if (day == '0'):
		return '0'

	path = os.path.dirname(__file__)
	filename = f"daily_log_{day}"
	try:
		log_file_r = open(path + '/system_logs/' + filename + '.json', "r")
		log = json.load(log_file_r)
		log_file_w = open(path + '/user_logs/' + filename + '.txt', "w")
	except FileNotFoundError:
		print('Not are logs for this day or format is wrong.')
		sleep(1.5)
		return '2'

	log_file_w.write(f'Day: {day}\nKeys pressed: {log["counted_keys"]}\n\n')
	log_file_w.write('Key'.center(11) + '|' + 'Count'.center(10) + '\n')
	keys_pressed = sorted(log['keys_pressed'].items(), key=itemgetter(1), reverse=True)
	for key, value in keys_pressed:
		log_file_w.write(f'{key.ljust(10)} | {str(value).rjust(5)}\n')

	print(f"created a log file in '{path}/user_logs/daily_log_{day}.txt'")
	sleep(1)

	return True


def get_graphic():
	""" See the weekly graphic """
	try:
		from datetime import timedelta
		from matplotlib import pyplot as plt
	except ImportError:
		print("[!] Error: Modules not found. Please run 'pip install -r requirements.txt'")
		exit()

	today = date.today()
	counts = {}
	today -= timedelta(days=6)
	for i in range(7):
		filename = f"daily_log_{today.isoformat()}.json"
		try:
			log_file_r = open('system_logs/' + filename, "r")
			log = json.load(log_file_r)
			counts[today.isoformat()] = log["counted_keys"]
		except FileNotFoundError:
			pass
		today += timedelta(days=1)

	clear()
	print('# Weekly graphic:')
	print(len(counts), 'days of logs.')
	plt.plot(counts.keys(), counts.values())
	plt.title(f'Weekly graphic - {date.today().isoformat()}')
	plt.grid(True)
	plt.show()


if (__name__ == '__main__'):
	os.chdir(os.path.dirname(__file__))
	main()
