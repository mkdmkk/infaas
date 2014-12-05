import httplib
from INFaaS import settings

__author__ = 'mkk'


def post_user1():
    # Prepare connection to INFaaS
    conn = httplib.HTTPConnection(settings.SERVER_HOST, settings.SERVER_PORT)

    # Prepare user
    user = {
        "email": "mkdmkk@gmail.com",
        "name": "Moon Kwon Kim",
        "pw": "1234",
        "biography": "Ph.D. Student in Soongsil University"
    }

    # Register user
    conn.request("POST", "/api/infer", json.dumps(user), headers={"Content-Type": "application/json"})
