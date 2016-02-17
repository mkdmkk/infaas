import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import smtplib
from email.mime.text import MIMEText

from pymysql import MySQLError, constants

#
# Constants
#
CODE_SUCCESS = {"code": "SUCCESS"}
CODE_FAILURE = {"code": "FAILURE"}
MSG_DB_FAILED = "Failed to handle DB requests."
MSG_NO_USER_LOGGEDIN = "No user logged in."
MSG_ALREADY_LOGGEDIN = "Already logged in."
MSG_INVALID_IDPW = "Invalid ID and/or PW."
MSG_INVALID_PARAMS = "Invalid parameters."
MSG_NODATA = "No data."
MSG_NO_EMAIL = "No email entered."
MSG_NO_USER_FOUND = "No user found."
MSG_EMAIL_SENT = "An email has been sent."

#
# Logging
#
logging.basicConfig(
    format="[%(name)s][%(asctime)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@csrf_exempt
def handle_contexts_mgt(request):
    """
    Handle login and logout requests.
    :param request:
    :return:
    """
    global db
    try:
        if request.method == 'POST':
            return JsonResponse(constants.CODE_SUCCESS)
        elif request.method == 'DELETE':
            return JsonResponse(constants.CODE_SUCCESS)
    except Exception as e:
        return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': str(e)}))
    else:
        msg = "/api/contexts<br>" \
              "[GET] and [PUT] are not provided.<br>" \
              "Use [POST] for Login.<br>Use [DELETE] for Logout."
    return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': msg}))


@csrf_exempt
def handle_users_mgt(request, first_try=True):
    """
    Retrieve or update a user.
    :param request: The body of PUT request is a JSON object of a user.
    :return:
    """
    global db
    try:
        if request.method == 'GET':
            if len(set(['userId', 'email']) & set(request.GET.keys())):
                #
                # Find user ID and password.
                #
                if 'email' not in request.GET:
                    raise Exception(MSG_NO_EMAIL)
                users = db.find_user_info(
                    user_id = request.GET.get('userId'),
                    email = request.GET.get('email')
                )
                if users and type(users) is list and len(users) > 1:
                    email_content = "Here are a list of ID and password registered with your email.\n"
                    for user in users:
                        email_content += "ID: %s, Password: %s" % (user['userId'], user['password'])
                elif users and (type(users) is dict or type(users) is list):
                    if type(users) is list:
                        users = users[0]
                    email_content = "Here are your ID and password.\n"
                    email_content += "ID: %s, Password: %s" % (users['userId'], users['password'])
                else:
                    raise Exception(MSG_NO_USER_FOUND)
                email_msg = MIMEText(email_content)
                email_msg['Subject'] = "[Rainbow] Account information"
                email_msg['From'] = 'admin@smartylab.co.kr'
                email_msg['To'] = request.GET['email']
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login("admin@smartylab.co.kr", "labsmarty7&")
                server.sendmail(email_msg['From'], [email_msg['To']], email_msg.as_string())
                server.quit()
                return JsonResponse(dict(constants.CODE_SUCCESS, **{'msg': MSG_EMAIL_SENT}))
            else:
                #
                # Get information of the user logged in.
                #
                user = request.session.get('user')
                if not user:
                    raise Exception(MSG_NO_USER_LOGGEDIN)
                return JsonResponse(dict(constants.CODE_SUCCESS, **{'user': user}))
        elif request.method == 'PUT':
            #
            # Update the user's information.
            #
            user = request.session.get('user')
            if not user:
                raise Exception(MSG_NO_USER_LOGGEDIN)
            if len(request.body) == 0:
                raise Exception(MSG_NODATA)
            user = json.loads(request.body.decode('utf-8'))
            res = db.update_user(
                user.get('password'),
                user.get('name'),
                user.get('nationality'),
                user.get('birthday'),
                user.get('mobile'),
                user.get('email'),
                user.get('gender'),
                user.get('fpId'),
                user.get('userId')
            )
            if not res:
                # When there is no change, this exception will also raised.
                raise Exception(MSG_DB_FAILED)
            # Get updated user
            user_id = user.get('userId')
            password = user.get('password')
            user = db.get_user(user_id, password)
            if not user:
                raise Exception(MSG_INVALID_IDPW)
            # Reassign the user to the session
            request.session['user'] = user
            return JsonResponse(dict(constants.CODE_SUCCESS, **{'user': user}))
    except MySQLError as e:
        db = AWSDataManager()
        if first_try:
            handle_sessions_mgt(request, first_try=False)
    except Exception as e:
        msg = str(e)
    else:
        msg = "/api/users<br>" \
              "[POST] and [DELETE] are not provided.<br>" \
              "Use [GET] for retrieving user information.<br>" \
              "Use [PUT] for updating user information."
    return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': msg}))


@csrf_exempt
def handle_measurements_mgt(request, first_try=True):
    """
    Retrieve measurements.
    :param request:
    :return:
    """
    global db
    try:
        if request.method == 'GET':
            user = request.session.get('user')
            if not user:
                raise Exception(MSG_NO_USER_LOGGEDIN)
            measurements = db.get_measurements(
                user.get('userId'),
                meas_type=request.GET.get('type'),
                time_from=request.GET.get('timeFrom'),
                time_to=request.GET.get('timeTo'),
                limit=request.GET.get('limit'),
                offset=request.GET.get('offset')
            )
            return JsonResponse(dict(constants.CODE_SUCCESS, **{'measurements': measurements}))
    except MySQLError as e:
        db = AWSDataManager()
        if first_try:
            handle_sessions_mgt(request, first_try=False)
    except Exception as e:
        msg = str(e)
    else:
        msg = "/api/measurements<br>" \
              "[POST], [PUT], and [DELETE] are not provided.<br>" \
              "Use [GET] for retrieving measurements."
    return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': msg}))


@csrf_exempt
def handle_contexts_mgt(request, first_try=True):
    """
    Retrieve contexts.
    :param request:
    :return:
    """
    global db
    try:
        if request.method == 'GET':
            user = request.session.get('user')
            logger.info(user)
            if not user:
                raise Exception(MSG_NO_USER_LOGGEDIN)
            ctxtype = request.GET.get('type')
            if not ctxtype:
                raise Exception(MSG_INVALID_PARAMS)
            contexts = db.get_contexts(
                user.get('userId'),
                context_type=ctxtype,
                time_from=request.GET.get('timeFrom'),
                time_to=request.GET.get('timeTo'),
                limit=request.GET.get('limit'),
                offset=request.GET.get('offset')
            )
            return JsonResponse(dict(constants.CODE_SUCCESS, **{
                'contexts': contexts,
                'categories': constants.Context.CATEGORIES[ctxtype]
            }))
    except MySQLError as e:
        db = AWSDataManager()
        if first_try:
            handle_sessions_mgt(request, first_try=False)
    except Exception as e:
        msg = str(e)
    else:
        msg = "/api/contexts<br>" \
              "[POST], [PUT], and [DELETE] are not provided.<br>" \
              "Use [GET] for retrieving contexts."
    return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': msg}))


@csrf_exempt
def handle_healthindexes_mgt(request, first_try=True):
    """
    Retrieve health indexes.
    :param request:
    :return:
    """
    global db
    try:
        if request.method == 'GET':
            user = request.session.get('user')
            if not user:
                raise Exception(MSG_NO_USER_LOGGEDIN)
            healthindexes = db.get_health_indexes(
                user.get('userId'),
                index_type=request.GET.get('type'),
                time_from=request.GET.get('timeFrom'),
                time_to=request.GET.get('timeTo'),
                limit=request.GET.get('limit'),
                offset=request.GET.get('offset')
            )
            return JsonResponse(dict(constants.CODE_SUCCESS, **{'healthIndexes': healthindexes}))
    except MySQLError as e:
        db = AWSDataManager()
        if first_try:
            handle_sessions_mgt(request, first_try=False)
    except Exception as e:
        msg = str(e)
    else:
        msg = "/api/healthindexes<br>" \
              "[POST], [PUT], and [DELETE] are not provided.<br>" \
              "Use [GET] for retrieving health indexes."
    return JsonResponse(dict(constants.CODE_FAILURE, **{'msg': msg}))
