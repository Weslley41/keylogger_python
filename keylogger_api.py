from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from keys import Keyboard

app = FastAPI()
keyboard = Keyboard()

origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
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


@app.get("/interval_log/{start}/to/{end}")
def interval_log(start:str, end:str):
  """
    Args format: YYYY-MM-DD
  """
  data = keyboard.get_interval_log(start, end)
  return format_json(data, 'date')
