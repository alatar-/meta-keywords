import logging

from flask import Flask

from api import utils

# flask setup
app = Flask(__name__)

utils.configure_loggers()

logger = logging.getLogger()
logger.info("Test")

@app.route("/url", methods=['GET'])
def endpoint():
    return "ok"
