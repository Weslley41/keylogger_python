from datetime import date, timedelta, datetime

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from keys import Keyboard

app = FastAPI()
keyboard = Keyboard()

origins = ["http://localhost:5173"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["GET"],
  allow_headers=["*"],
)

def format_json(data, column_name='name'):
  new_data = {}

  for row in data:
    new_data[row[column_name]] = row['count']

  return new_data


@app.get("/")
def home():
	return {"msg": "Welcome to Keylogger API, see localhost:8000/docs"}


@app.get("/count/")
def count(day:str = date.today()):
  """
    Args:
      day format: YYYY-MM-DD
  """
  return keyboard.count(day)


@app.get("/top_keys/")
def top_keys(day:str = date.today(), amount:int = 5):
  """
    Args:
      day format: YYYY-MM-DD
  """
  data = keyboard.get_top_keys(day, amount)
  return format_json(data)


@app.get("/daily_log/")
def daily_log(day:str = date.today()):
  """
    Args:
      day format: YYYY-MM-DD
  """
  data = keyboard.get_keys_log(day)
  return format_json(data)


@app.get("/interval_log/{start}/to/{end}", status_code=status.HTTP_200_OK)
def interval_log(start:str, end:str, response:Response):
  """
    Args format: YYYY-MM-DD
  """
  data = keyboard.get_interval_log(start, end)
  if data:
    return format_json(data, 'date')

  response.status_code = status.HTTP_404_NOT_FOUND


@app.get("/weekly_log/")
def weekly_log():
  end = date.today()
  start = end - timedelta(days=6)
  data = keyboard.get_interval_log(start, end)

  new_data = {}
  for day in data:
    str_day = str(day['date'])
    label = datetime.strptime(str_day, '%Y-%m-%d').strftime('%a')
    new_data[label] = day['count']

  return new_data
