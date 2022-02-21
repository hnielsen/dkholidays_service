# app.py
import os
import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from logzero import logger

from calendar_dk import DanishHolidays

def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    app.config['JSON_AS_ASCII'] = False

    @app.get("/holidays")
    def get_holidays():    
        year = request.args.get('year', datetime.date.today().year, type=int)
        print(year, flush=True)
        dh = DanishHolidays(year)
        holidays = dh.get_danish_holidays_formatted()
        return jsonify(holidays)

    @app.route("/")
    def get_default():
        return get_holidays()
    
    @app.route("/<year>")
    def get_holidays_by_year():
        return get_holidays()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app = create_app()
    app.run(host="0.0.0.0", port=port)