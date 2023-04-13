from datetime import date, timedelta
from flask import Flask, render_template, request
from flask import json
import datetime
import logging
import os

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PORT = int(os.environ.get("PORT", 80))
DEBUG = bool(os.environ.get("DEBUG", False))

application = Flask(__name__)

@application.route('/')
def handle_index():
    # Simulate an expansive request

    return render_template("index.html", page_generated=datetime.datetime.now())

@application.route('/health')
def handle_health():
    return "OK"

def main():
    application.run(debug=DEBUG, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
