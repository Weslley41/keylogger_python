import os
import re
from datetime import date, timedelta
from pathlib import Path
from time import sleep
from matplotlib import pyplot as plt
import requests


def show_menu():
    keyboard_count = requests.get(HOSTNAME + 'get_use_count/', timeout=10).text
    os.system('clear')
    print(' Keylogger '.center(50, '-'))
    print(f'Today: {date.today()}'.ljust(24),
		f'Counted keys: {keyboard_count}'.rjust(25))
    print('-'*50)

    print(
        "1. Show the most used keys\n"
        "2. Get log file\n"
        "3. Show weekly graphic\n"
        "4. Exit\n"
    )

    option = input('Choice one: ')
    if option.isdigit() and int(option) in range(1, 5):
        return int(option)

    print('Invalid option.')
    sleep(1.5)
    return show_menu()


def press_to_back():
    input('Press Enter to back.')


def input_date():
    os.system('clear')
    print('tricks:\n\
  0: back\n\
  today: show today\'s data')

    day = input('Choice a date(YYYY-MM-DD): ')

    match day:
        case 'today':
            os.system('clear')
            return date.today()
        case '0':
            return False
        case _:
            re_matches = re.search(DATE_REGEX, day)
            if re_matches:
                os.system('clear')
                return re_matches.group(0)

            print('Invalid date format.')
            sleep(1.5)
            input_date()


def format_json_to_text(title, day, json_data):
    string = ' Keylogger '.center(50, '-') + '\n'
    string += f'{title}'.ljust(25)
    string += f'Day: {day}'.rjust(25) + '\n'
    string += '-' * 50 + '\n'

    for key in json_data:
        string += key.ljust(40) + str(json_data[key]).rjust(10) + '\n'

    if not json_data:
        string += 'Data not found\n'.center(50)

    return string


def show_most_used_keys():
    day = input_date()
    if day:
        data = requests.get(
            HOSTNAME + f'get_most_used_keys/?day={day}', timeout=10).json()
        print(format_json_to_text('Most used keys', day, data))
        press_to_back()


def get_log_file():
    day = input_date()
    if day:
        data = requests.get(
            HOSTNAME + f'get_used_keys/?day={day}', timeout=10).json()
        if data:
            filename = f'{Path.home()}/keyboard_logs/keyboard_log_{day}.txt'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='UTF-8') as log_file:
                log_file.write(format_json_to_text('Log file', day, data))

            print(f'Log as saved in {filename}\n')
        else:
            print('Data not found\n')

        press_to_back()


def show_weekly_graphic():
    start, end = date.today() - timedelta(days=6), date.today()
    data = requests.get(
        HOSTNAME + f'get_interval_use_count/{start}/to/{end}/', timeout=10).json()

    plt.figure("Keylogger graphic", figsize=(8, 4.5))
    plt.plot(data.keys(), data.values())
    plt.title(f'Weekly graphic: {start} to {end}')
    plt.grid(True)
    plt.show()


def main():
    run_cli = True

    while run_cli:
        option = show_menu()

        match option:
            case 1:
                show_most_used_keys()
            case 2:
                get_log_file()
            case 3:
                show_weekly_graphic()
            case 4:
                run_cli = False


if __name__ == '__main__':
    DATE_REGEX = r'(\d{4})-(\d{2}|\d)-(\d{2}|\d)'
    HOSTNAME = 'http://localhost:1234/'
    main()
