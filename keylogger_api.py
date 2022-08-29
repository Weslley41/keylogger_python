from datetime import date

from fastapi import FastAPI
from keys import Keyboard

app = FastAPI()
keyboard = Keyboard()

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
  return keyboard.get_top_keys(day, amount)


@app.get("/daily_log/")
def daily_log(day:str = date.today()):
  """
    Args:
      day format: YYYY-MM-DD
  """
  return keyboard.get_keys_log(day)


@app.get("/interval_log/{start}/to/{end}")
def interval_log(start:str, end:str):
  """
    Args format: YYYY-MM-DD
  """
  return keyboard.get_interval_log(start, end)
