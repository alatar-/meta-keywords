import logging

import flask
from flask import send_from_directory

from api import utils, fetcher, parser
from api.messages import status

# flask setup
app = flask.Flask(__name__)

# setup logging
utils.configure_loggers()
logger = logging.getLogger('main')


@app.route("/count_keywords", methods=['GET'])
def endpoint():
    url = flask.request.args.get('url')
    if not url:
        return utils.gen_response(400, status.MISSING_URL_PARAM)

    soup, req_status = fetcher.get_soup_from_url(url)
    if req_status == status.URL_VALIDATION_FAILED:
        return utils.gen_response(400, req_status)
    if req_status != status.OK:
        return utils.gen_response(500, req_status)

    keywords = parser.find_meta_keywords(soup)
    result = parser.count_keywords_in_text(soup, keywords)
    return utils.gen_response(200, status.OK, result)


if __name__ == '__main__':
    # Development routine, executed only when file explicitly run from
    # the console. For production, use appropriate server e.g. gunicorn.
    # See README.md for more details.
    @app.route('/')
    def serve_index():
        return send_from_directory('../frontend/', 'index.html')
    @app.route('/static/<path>/<resource>')
    def serve_static(path, resource):
        print(path, resource)
        return send_from_directory('../frontend/static/{}/'.format(path), resource)

    app.run(debug=True, port=8000)
