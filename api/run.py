import logging

import flask

from api import utils, fetcher, parser

# flask setup
app = flask.Flask(__name__)

# setup logging
utils.configure_loggers()
logger = logging.getLogger('main')


@app.route("/count_keywords", methods=['GET'])
def endpoint():
    url = flask.request.args.get('url')
    if not url:
        return flask.jsonify({
                'message': "Missing URL parameter"
            }), 400

    soup, status = fetcher.get_soup_from_url(url)
    if not soup:
        return flask.jsonify({
                'message': "Couldn't make it :("
            }), 500

    keywords = parser.find_meta_keywords(soup)
    result = parser.count_keywords_in_text(soup, keywords)

    return flask.jsonify({
            'message': "Success!",
            'result': result
        }), 200


if __name__ == '__main__':
    # Development routine, executed only when file explicitly run
    # from console. For production, use appropriate server e.g. gunicorn.
    app.run(debug=True)
