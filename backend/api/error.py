from flask import jsonify


def throw_error(
    type: str,
    message: str,
    status_code: int = 401,
):
    """
    Throws an error status and message if something goes wrong during authentication
    """
    response = {
        "success": False,
        "result": {
            "type": type,
            "message": message,
        },
    }
    return jsonify(response), status_code
