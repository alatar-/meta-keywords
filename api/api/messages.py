from enum import Enum

class status(Enum):
    OK = 0
    MISSING_URL_PARAM = 1
    URL_VALIDATION_FAILED = 11
    FETCHING_OR_DECODING_ERROR = 21
    HTML_DOM_PARSING_ERROR = 22
    UNEXPECTED_SERVER_RESPONSE = 23
    URL_NOT_FOUND = 24


_MESSAGES = {
    "en": {
        "fallback": "Server error.",
        status.OK: "Success!",
        status.MISSING_URL_PARAM: "URL parameter not provided!",
        status.URL_VALIDATION_FAILED: "Invalid URL provided. Please use the correct format.",
        status.FETCHING_OR_DECODING_ERROR: "Server error [1].",
        status.HTML_DOM_PARSING_ERROR: "Server error [2].",
        status.UNEXPECTED_SERVER_RESPONSE: "Server error [3].",
        status.URL_NOT_FOUND: "Page under provided URL not found.",
    }
}


def get_message(req_status):
    local = 'en'

    fallback_message = _MESSAGES[local].get('fallback', "Server error.")
    message = _MESSAGES[local].get(req_status, fallback_message)

    return message
