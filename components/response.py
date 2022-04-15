from flask import jsonify
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)


def response_internal_server_error(error: Exception) -> (str, int):
    logger.exception(error)
    return jsonify({"body": str(error), "status": "fail"}), 500


def response_success(body):
    return jsonify({"body": body, "status": "ok"}), 200


def response_fail_auth():
    return jsonify({"body": "Unauthorized", "status": "fail"}), 401


def response_not_found(body=None):
    return jsonify({"body": body, "status": "fail"}) if body is not None else jsonify({"body": "File not found", "status": "fail"}), 404


def response_bad_request(exception):
    return jsonify({"body": f"Bad request: {exception}", "status": "fail"}), 400


def response_method_not_allowed():
    return jsonify({"body": "Method not allowed", "status": "fail"}), 405


def response_custom(body, code, status):
    return jsonify({"body": body, "status": status}), code
