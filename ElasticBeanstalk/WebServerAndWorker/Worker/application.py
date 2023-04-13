from flask import Flask, request, Response
import boto3
import logging
import os

logging.basicConfig(format='%(levelname)s | %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

PORT = int(os.environ.get("PORT", 5000))
DEBUG = bool(os.environ.get("DEBUG", False))


application = Flask(__name__)


@application.route('/')
def handle_index():
    return "OK"


@application.route('/process-message', methods=['POST'])
def handle_process_message():
    if request.json is None:
        raise ValueError("Was expecting JSON request")
    message = request.json
    logger.info(f"Downloading tarball {message['tarball_date']} ... ")
    return "OK"


@application.route('/scheduled', methods=['POST'])
def handle_scheduled():
    logger.info("Received task %s scheduled at %s",
                os.environ.get('HTTP_X_AWS_SQSD_TASKNAME', None),
                os.environ.get('HTTP_X_AWS_SQSD_SCHEDULED_AT', 'None'))
    return "OK"


@application.route('/health')
def handle_health():
    return "OK"


def main():
    application.run(debug=DEBUG, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
