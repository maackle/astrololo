import logging

from flask import Flask, render_template, request, redirect, session, flash, url_for, g, jsonify
import requests

from astro import get_natal_chart
from dateutil import parser


def create_app():

    from cache import cache

    requests.packages.urllib3.add_stderr_logger()

    app = Flask(__name__)

    app.config.from_object('config.settings')
    try:
        app.config.from_envvar('ASTROLOLO_SETTINGS')
        print("Loaded config from envvar ASTROLOLO_SETTINGS")
    except:
        app.config.from_object('config.development')
        print("Loaded DEVELOPMENT config")

    cache.init_app(app, config={
        'CACHE_TYPE': 'simple',
        # 'CACHE_DIR': '.flask-cache',
        'CACHE_THRESHOLD': 1000000,
        'CACHE_DEFAULT_TIMEOUT': 60*60*60*24,  # one day
        })

    return app


app = create_app()


@app.route('/natal/')
def natal():
    """
    Request:
        date=1984-11-11

    Response:
    {
        Sun: {
            sign: "Scorpio",
            angle: 0.3315804123368795,
            angle_dms: "18° 59"",
            total_angle: 3.9967718415249713
        },
        Moon: {
            angle: 0.2554040978936747,
            angle_dms: "14° 38"",
            sign: "Gemini",
            total_angle: 1.3026016490902723
        },
    }
    """

    date_str = request.args.get('date')
    if date_str:
        date = parser.parse(date_str)
        chart = get_natal_chart(date)
        return jsonify(chart)
    else:
        return jsonify({"error": "invalid date"})
