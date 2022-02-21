# app.py
import datetime
from flask import Flask, jsonify
from .calendar_dk import DanishHolidays

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def get_default():
    return holidays(datetime.date.today().year)

@app.route("/<year>")
def get_holidays_by_year(year):
    return holidays(int(year))

def holidays(year):
    dh = DanishHolidays(year)
    holidays = dh.get_danish_holidays_api()
    return jsonify(holidays)
