from datetime import date, timedelta, datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from keys import Keyboard

app = FastAPI()
keyboard = Keyboard()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET"],
  allow_headers=["*"],
)

def format_json(data, date_start=None, date_end=None, column_name='name', date_format='%Y-%m-%d'):
  if column_name == 'name':
    new_data = {}
    for row in data:
      new_data[row['name']] = row['count']

    return new_data

  new_data, index_list = {}, 0
  date_start = datetime.strptime(date_start, '%Y-%m-%d').date()
  date_end = datetime.strptime(date_end, '%Y-%m-%d').date()

  while date_start <= date_end:
    date_list = data[index_list][column_name]
    if date_start == date_list:
      new_data[date_list.strftime(date_format)] = data[index_list]['count']
      index_list += 1
    else:
      new_data[date_start.strftime(date_format)] = 0

    date_start += timedelta(days=1)

  return new_data


@app.get("/")
def home(request: Request):
  return { "msg": f"Welcome to Keylogger API, see {request.base_url}docs" }


@app.get("/weekly_log/")
def weekly_log():
  end = date.today()
  start = end - timedelta(days=6)
  data = keyboard.get_interval_use_count(start, end)
  data = format_json(data, str(start), str(end), column_name='date', date_format='%a')

  return data


@app.get("/get_most_used_keys/")
def get_most_used_keys(day:str = date.today(), amount:int = 5):
  data = keyboard.get_most_used_keys(day, amount)

  return format_json(data)


@app.get("/get_interval_most_used_keys/{start}/to/{end}/")
def get_interval_most_used_keys(start:str, end:str, amount:int = 5):
  data = keyboard.get_interval_most_used_keys(start, end, amount)

  return format_json(data)


@app.get("/get_all_time_most_used_keys/")
def get_all_time_most_used_keys(amount:int = 5):
  data = keyboard.get_all_time_most_used_keys(amount)

  return format_json(data)


@app.get("/get_used_keys/")
def get_used_keys(day:str = date.today()):
  data = keyboard.get_used_keys(day)

  return format_json(data)


@app.get("/get_interval_used_keys/{start}/to/{end}/")
def get_interval_used_keys(start:str, end:str):
  data = keyboard.get_interval_used_keys(start, end)
  return format_json(data)


@app.get("/get_all_time_used_keys/")
def get_all_time_used_keys():
  data = keyboard.get_all_time_used_keys()

  return format_json(data)


@app.get("/get_use_count/")
def get_use_count(day:str = date.today()):
  data = keyboard.get_use_count(day)

  return data


@app.get("/get_interval_use_count/{start}/to/{end}/")
def get_interval_use_count(start:str, end:str):
  data = keyboard.get_interval_use_count(start, end)

  return format_json(data, start, end, column_name='date')


@app.get("/get_all_time_use_count/")
def get_all_time_use_count():
  start = oldest_date()
  end = date.today()
  data = keyboard.get_all_time_use_count()

  return format_json(data, str(start), str(end), column_name='date')


@app.get("/oldest_date/")
def oldest_date():
  return keyboard.get_oldest_date()
