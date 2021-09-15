import base64
import json


def create(response, username):
    session = base64.b64encode(json.dumps({"username": username}).encode())
    response.set_cookie("Athena_session", session)
    return response


def load(request):

    session = {}
    cookie = request.cookies.get("Athena_session")

    try:
        if cookie:
            decoded = base64.b64decode(cookie.encode())
            if decoded:
                session = json.loads(base64.b64decode(cookie))
    except Exception:
        pass

    return session


def destroy(response):
    response.set_cookie("Athena_session", "", expires=0)
    return response
