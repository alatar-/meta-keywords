import logging
from enum import Enum

import flask

from . import config
from . import messages

def configure_loggers():
    default_format = '%(asctime)s %(levelname)s\t%(name)s:\t%(message)s'
    default_date_format = '%H:%M:%S'
    default_formatter = logging.Formatter(default_format, default_date_format)

    logging.basicConfig(
        level=logging.INFO,
        format=default_format,
        datefmt=default_date_format
    )

    mainLoggerFileHandler = logging.FileHandler(config.APP_LOG_FILE)
    mainLoggerFileHandler.setFormatter(default_formatter)
    mainLoggerFileHandler.setLevel(logging.DEBUG)
    mainLogger = logging.getLogger('main')
    mainLogger.setLevel(logging.DEBUG)

    logging.getLogger().addHandler(mainLoggerFileHandler)
    mainLogger.addHandler(mainLoggerFileHandler)


def gen_response(http_code, req_status, result=None):
    '''
    Helper function generating Flask response based on
    passed data.

    Returns `http_code` status with JSON response containing
    "message" and "result" (if provided).
    '''
    response = {
        "message": messages.get_message(req_status)
    }
    if result:
        response['result'] = result

    return flask.jsonify(response), http_code