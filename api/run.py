import logging

from flask import Flask

from api import utils, fetcher, parser

# flask setup
app = Flask(__name__)

# setup logging
utils.configure_loggers()
logger = logging.getLogger()


@app.route("/url", methods=['GET'])
def endpoint():
    soup = fetcher.get_url_soup('https://www.twilio.com')
    keywords = parser.count_keywords(soup)

    return keywords


if __name__ == '__main__':
    # Development routine, executed only when file explicitly run
    # from console. For production, use appropriate server e.g. gunicorn.
    app.run(debug=True)
