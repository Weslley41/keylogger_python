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

	choice = menu(today, log["counted_keys"])
	while choice:
		if (choice == '1'):
			show_top_keys(log["keys_pressed"])
		elif (choice == '2'):
			get_log(log, today)
		elif (choice == '3'):
			get_graphic()
		elif (choice == '0'):
			exit()
		else:
			print('Invalid choice.')
			sleep(1)
			clear()

		choice = menu(today, log["counted_keys"])


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
	print(f'Today: {today} - counted keys: {counts}')
	print("""
	1. Show top keys
	2. Get today's log
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
	for key, value in keys_pressed[:5]:
		print(f'Key: {key}\nCount: {value}\n')


def get_log(log, today):
	""" Get today's log, saved as file """
	clear()
	path = os.path.dirname(__file__) + '/user_logs/'
	filename = f"daily_log_{today}.txt"
	log_file = open(path + filename, "w")

	log_file.write(f'Today: {today}\nKeys pressed: {log["counted_keys"]}\n\n')
	log_file.write('Key'.center(11) + '|' + 'Count'.center(10) + '\n')
	keys_pressed = sorted(log['keys_pressed'].items(), key=itemgetter(1), reverse=True)
	for key, value in keys_pressed:
		log_file.write(f'{key.ljust(10)} | {str(value).rjust(5)}\n')

	print(f"# Log: create a file in '{path}daily_log_{today}.txt'")
	sleep(1)


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
