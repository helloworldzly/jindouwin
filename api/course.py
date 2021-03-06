#-*-coding:utf-8-*-

from api import api
from flask import request, jsonify, make_response
from config.rescode import *

@api.route('/course/getcourse', methods=['GET'])
def getcourse_list():
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_user_is_teacher
    res = check_user_is_teacher(userid)
    from lib import get_course_by_userid
    course_list = get_course_by_userid(userid, res)

    return jsonify(res=SUCCESS, course=course_list)

@api.route('/course/info/<courseid>', methods=['GET'])
def getcourse_info(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_is_course_teacher
    isteacher = check_is_course_teacher(userid, courseid)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid, isteacher)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_info_by_courseid
    course_info = get_info_by_courseid(courseid)
    return jsonify(res=SUCCESS, info=course_info)

@api.route('/course/add', methods=['POST'])
def course_add():
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(USER_NOT_LOGIN_IN)
    from lib import check_user_is_teacher
    res = check_user_is_teacher(userid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)
    form = request.form
    require = ['name', 'description', 'time', 'classroom']
    for item in require:
        if not item in form:
            return jsonify(res=PARAMETER_WRONG)

    name = form['name']
    description = form['description']
    time = form['time']
    classroom = form['classroom']

    from lib import get_name_by_userid
    teacher = get_name_by_userid(userid)
    teacher = teacher.decode('utf-8')

    files = request.files
    f = files['file']
    filename = f.filename
    f.save('tmp/' + filename)

    from lib import add_course
    add_course(teacher, name, description, time, classroom, filename)
    return jsonify(res=SUCCESS)

@api.route('/course/upload/namelist/<courseid>', methods=['POST'])
def upload_namelist(courseid):
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

    files = request.files
    f = files['file']
    import os
    path = os.path.realpath(__file__)
    path = '/'.join(path[:-2]) + '/tmp/%s.csv'%courseid
    f.save(path)

    from lib import add_userlist_from_csv
    add_userlist_from_csv(path)

    return jsonify(res=SUCCESS)

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

    from lib import check_user_is_teacher
    isteacher = check_user_is_teacher(userid)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid, isteacher)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_news_by_courseid
    course_news = get_news_by_courseid(courseid)
    return jsonify(res=SUCCESS, news=course_news)

@api.route('/course/homework/<courseid>', methods=['GET'])
def getcourse_homework(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_user_is_teacher
    isteacher = check_user_is_teacher(userid)

    from lib import check_attend_course
    res = check_attend_course(userid, courseid, isteacher)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_homework_by_courseid
    course_homework = get_homework_by_courseid(courseid, userid)
    return jsonify(res=SUCCESS, homework=course_homework)

@api.route('/course/add/homework/<courseid>', methods=['POST'])
def add_homework(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import get_name_by_userid
    name = get_name_by_userid(userid)
    name = name.decode('utf-8')

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

    from lib import add_news_by_courseid
    add_news_by_courseid(courseid, description, name, 2)

    return jsonify(res=SUCCESS)

@api.route('/course/homework/submit/<courseid>/<homeworkid>', methods=['GET','POST'])
def homework_submit(courseid, homeworkid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    if request.method == 'POST':

        from lib import check_attend_course
        res = check_attend_course(userid, courseid, False)
        if res == False:
            return jsonify(res=PERMISSION_DENIED)

        from lib import check_homework_exist
        res = check_homework_exist(homeworkid)
        if res == False:
            return jsonify(res=PERMISSION_DENIED)

        files = request.files
        f = files['file']
        filename = f.filename
        filetype = filename.split('.')[-1]
        filename = userid + '.' + filetype

        import os
        path = os.path.realpath(__file__).split('/')[:-2]
        dirpath = '/'.join(path) + '/course/%s/homework/%s'%(courseid, homeworkid)
        os.system("mkdir -p %s"%dirpath)
        path = '/'.join(path) + '/course/%s/homework/%s/%s'%(courseid, homeworkid, filename)
        f.save(path)

        from lib import homework_submit
        homework_submit(userid, homeworkid)

        return jsonify(res=SUCCESS)
    else:
        from lib import check_is_course_teacher
        res = check_is_course_teacher(userid, courseid)
        if res == False:
            return jsonify(res=PERMISSION_DENIED)

        from lib import check_homework_exist
        res = check_homework_exist(homeworkid)
        if res == False:
            return jsonify(res=PERMISSION_DENIED)

        from lib import get_studentlist_by_courseid
        studentlist = get_studentlist_by_courseid(courseid)

        from lib import get_homeworksubmit_by_homeworkid
        homeworksubmit = get_homeworksubmit_by_homeworkid(homeworkid)

        res = []
        for item in studentlist:
            if item[0] in homeworksubmit:
                res.append({'userid':item[0],'name':item[1],'studentid':item[2],'issubmit':'1'})
            else:
                res.append({'userid':item[0],'name':item[1],'studentid':item[2],'issubmit':'0'})
        return jsonify(res=SUCCESS, homework=res)


@api.route('/course/resource/upload/<courseid>', methods=['POST'])
def resource_upload(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import get_name_by_userid
    name = get_name_by_userid(userid)
    name = name.decode('utf-8')

    from lib import check_is_course_teacher
    res = check_is_course_teacher(userid, courseid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    files = request.files
    f = files['file']
    filename = f.filename
    import os
    path = os.path.realpath(__file__).split('/')[:-2]
    path = '/'.join(path) + '/course/%s/resource/%s'%(courseid, filename)
    f.save(path)

    from lib import add_resource_by_courseid
    add_resource_by_courseid(courseid, filename)
    from lib import add_news_by_courseid
    add_news_by_courseid(courseid, filename, name, 1)

    return jsonify(res=SUCCESS)

@api.route('/course/resource/<courseid>', methods=['GET'])
def getcourse_resource(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    # session = '111111'
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_user_is_teacher
    isteacher = check_user_is_teacher(userid)
    from lib import check_attend_course
    res = check_attend_course(userid, courseid, isteacher)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_resource_by_courseid
    course_resource = get_resource_by_courseid(courseid)
    return jsonify(res=SUCCESS, resource=course_resource)

@api.route('/course/teacher/info/<courseid>', methods=['GET'])
def course_teacher_info(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    from lib import check_user_is_teacher
    isteacher = check_user_is_teacher(userid)
    from lib import check_attend_course
    res = check_attend_course(userid, courseid, isteacher)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import get_course_teacher_info_by_courseid
    teacher = get_course_teacher_info_by_courseid(courseid)
    return jsonify(res=SUCCESS, teacher=teacher)

@api.route('/course/add/news/<courseid>', methods=['POST'])
def course_add_news(courseid):
    cookies = request.cookies
    if not 'session' in cookies:
        return jsonify(res=PARAMETER_WRONG)
    session = cookies['session']
    from lib import get_userid_by_session
    userid = get_userid_by_session(session)
    if userid == None:
        return jsonify(res=USER_NOT_LOGIN_IN)

    form = request.form
    if not 'notice' in form:
        return jsonify(res=PARAMETER_WRONG)
    notice = form['notice']

    from lib import get_name_by_userid
    name = get_name_by_userid(userid)
    name = name.decode('utf-8')

    from lib import check_is_course_teacher
    res = check_is_course_teacher(userid, courseid)

    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    from lib import add_news_by_courseid
    add_news_by_courseid(courseid, notice, name, 3)
    return jsonify(res=SUCCESS)
