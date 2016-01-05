#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/user/register', methods=['POST'])
def register():
    form = request.form
    require = ['username', 'password', 'email', 'phone', 'name', 'studentid', 'usertype']
    for item in require:
        if not item in form:
            return jsonify(res=PARAMETER_WRONG)

    username = form['username']
    password = form['password']
    email = form['email']
    phone = form['phone']
    name = form['name']
    studentid = form['studentid']
    usertype = form['usertype']

    from lib import check_username_exist
    if check_username_exist(username) == True:
        return jsonify(res=USERNAME_EXIST)

    files = request.files
    f = files['file']
    filename = f.filename
    filetype = filename.split('.')[-1]
    from lib import generate_session
    code = generate_session()
    filename = code + '.' + filetype
    f.save("static/user/avatar/"+filename)

    from lib import user_register
    user_register(username, password, email, phone, name, studentid, usertype, filename)

    return jsonify(res=SUCCESS)

@api.route('/user/update', methods=['POST'])
def update():
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    form = request.form
    require = ['email', 'phone', 'name', 'studentid']
    for item in require:
        if not item in form:
            return jsonify(res=PARAMETER_WRONG)

    email = form['email']
    phone = form['phone']
    name = form['name']
    studentid = form['studentid']

    from lib import update_user_info
    update_user_info(email, phone, name, studentid, userid)
    return jsonify(res=SUCCESS)

@api.route('/user/login', methods=['POST'])
def login():
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'

    form = request.form
    if not 'username' in form or not 'password' in form:
        return jsonify(res=PARAMETER_WRONG)

    username = form['username']
    password = form['password']

    from lib import user_login
    res = user_login(username, password, session)
    if res == False:
        return jsonify(res=USERNAME_OR_PASSWORD_ERROR)

    return jsonify(res=SUCCESS)

@api.route('/user/info', methods=['GET'])
def info():
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'

    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN)

    from lib import get_info_by_id
    user_info = get_info_by_id(userid)

    return jsonify(res=SUCCESS, info=user_info)

@api.route('/user/logout', methods=['GET'])
def logout():
    resp = make_response(jsonify(res=SUCCESS))
    resp.delete_cookie('session')
    return resp
