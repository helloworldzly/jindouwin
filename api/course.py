#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/course/getcourse', methods=['GET'])
def getcourse_list():
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(res=PARAMETER_WRONG)
    # session = cookies['session']
    session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import get_course_by_userid
    course_list = get_course_by_userid(userid)
    return jsonify(res=SUCCESS, course=course_list)

@api.route('/course/info/<courseid>', methods=['GET'])
def getcourse_info(courseid):
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(res=PARAMETER_WRONG)
    # session = cookies['session']
    session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_info_by_courseid
    course_info = get_info_by_courseid(courseid)
    return jsonify(res=SUCCESS, info=course_info)

@api.route('/course/news/<courseid>', methods=['GET'])
def getcourse_news(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_news_by_courseid
    course_news = get_news_by_courseid(courseid)
    return jsonify(res=SUCCESS, news=course_news)

@api.route('/course/homework/<courseid>', methods=['GET'])
def getcourse_homework(courseid):
    # cookies = request.cookies
    # if not 'session' in cookies:
    #     return jsonify(res=PARAMETER_WRONG)
    # session = cookies['session']
    session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_homework_by_courseid
    course_homework = get_homework_by_courseid(courseid)
    return jsonify(res=SUCCESS, homework=course_homework)

@api.route('/course/add/homework/<courseid>', methods=['GET'])
def add_homework(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_is_course_teacher
    res = check_is_course_teacher(userid, courseid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    form = request.form
    if not 'description' in form or not 'deadline' in form:
        return jsonify(res=PARAMETER_WRONG)
    description = form['description']
    deadline = form['deadline']

    from lib import add_homework_by_courseid
    add_homework_by_courseid(courseid, description, deadline)
    return jsonify(res=SUCCESS)