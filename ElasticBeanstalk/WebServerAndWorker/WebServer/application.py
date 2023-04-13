from datetime import date, timedelta
from flask import Flask, render_template, request
from flask import json
import boto3
import logging
import os
import random

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PORT = int(os.environ.get("PORT", 5000))
DEBUG = bool(os.environ.get("DEBUG", False))
WORKERQUEUE = os.environ.get("WORKERQUEUE", None)


application = Flask(__name__)


@application.route('/')
def handle_index():
    # Simulate an expansive request
    process_time = random.uniform(0, 5)
    return render_template("index.html", process_time=process_time)


@application.route('/download')
def handle_download():
    # Put a message in the Queue telling the worker that it should download
    # the given ZTF Daily alert tarball...
    tarball_date = request.args.get('date', None)
    if not tarball_date:
        yesterday = date.today() - timedelta(1)
        tarball_date = yesterday.strftime("%Y%m%d")
    logger.info(f"Downloading ZTF Daily Alerts tarball {tarball_date} ... ")
    if not WORKERQUEUE:
        raise ValueError("WORKERQUEUE Environment Variable has not been set!")
    logger.info(f"Sending message to SQS Queue {WORKERQUEUE}")
    sqs = boto3.client('sqs')
    response = sqs.send_message(
        QueueUrl=WORKERQUEUE,
        MessageBody=json.dumps({ "tarball_date": tarball_date})
    )
    return render_template("download.html", tarball_date=tarball_date, response=response)


@application.route('/health')
def handle_health():
    return "OK"


def main():
    application.run(debug=DEBUG, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
