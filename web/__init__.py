#-*-coding:utf-8-*-

from server import app
from flask import render_template, make_response, request, redirect, send_from_directory

@app.route('/login', methods=['GET'])
def login():
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid != None:
            return redirect('/')
    else:
        from lib import generate_session
        session = generate_session()
    resp = make_response(render_template('login.html'))
    resp.set_cookie('session', session, max_age=1200)
    return resp

@app.route('/login2', methods=['GET'])
def login2():
    return render_template('login.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/', methods=['GET'])
def index():
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid == None:
            return redirect('/login')
        else:
            from lib import is_teacher
            if is_teacher(userid):
                resp = make_response(render_template('index_admin.html'))
            else:
                resp = make_response(render_template('index.html'))
            return resp
    else:
        return redirect('/login')

@app.route('/2', methods=['GET'])
def index2():
    return render_template('index.html')

@app.route('/course/<courseid>', methods=['GET'])
def course(courseid):
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid == None:
            return redirect('/login')
        else:
            from lib import is_teacher
            if is_teacher(userid):
                resp = make_response(render_template('course_admin.html', courseid=courseid))
            else:
                resp = make_response(render_template('course.html', courseid=courseid))
            return resp
    else:
        return redirect('/login')

@app.route('/homework/<courseid>', methods=['GET'])
def homework(courseid):
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid == None:
            return redirect('/login')
        else:
            from lib import check_user_is_teacher
            isteacher = check_user_is_teacher(userid)

            from lib import check_attend_course
            res = check_attend_course(userid, courseid, isteacher)
            if res == False:
                return jsonify(res=PERMISSION_DENIED)

            return render_template('homework.html', courseid=courseid)
    else:
        return redirect('/login')

@app.route('/homework/<courseid>/<homeworkid>', methods=['GET'])
def homework_list(courseid, homeworkid):
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid == None:
            return redirect('/login')
        else:
            from lib import is_teacher
            if is_teacher(userid):
                resp = make_response(render_template('homework_admin.html', courseid=courseid, homeworkid=homeworkid))
            else:
                resp = make_response(render_template('course.html', courseid=courseid))
            return resp
    else:
        return redirect('/login')

@app.route('/course_admin/<courseid>', methods=['GET'])
def course_admin(courseid):
    return render_template('course_admin.html', courseid=courseid)

@app.route('/downloads/<courseid>', methods=['GET'])
def downloads(courseid):
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_userid_by_session
        userid = get_userid_by_session(session)
        if userid == None:
            return redirect('/login')
        else:
            from lib import check_user_is_teacher
            isteacher = check_user_is_teacher(userid)

            from lib import check_attend_course
            res = check_attend_course(userid, courseid, isteacher)
            if res == False:
                return jsonify(res=PERMISSION_DENIED)

            return render_template('downloads.html', courseid=courseid)
    else:
        return redirect('/login')

@app.route('/news', methods=['GET'])
def news():
    pass

@app.route('/resource/<courseid>/<filename>', methods=['GET'])
def resource(courseid, filename):
    import os
    path = os.path.realpath(__file__).split('/')[:-2]
    path = '/'.join(path) + '/course/%s/resource/'%courseid
    filename = filename.encode('utf-8')
    return send_from_directory(path.encode('utf-8'), filename, as_attachment=True)

@app.route('/homework/download/<courseid>/<homeworkid>/<studentuserid>', methods=['GET'])
def homework_download(courseid, homeworkid, studentuserid):
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
    from lib import check_homework_exist
    res = check_homework_exist(homeworkid)
    if res == False:
        return jsonify(res=PERMISSION_DENIED)

    if '.' in studentuserid:
        import os
        path = os.path.realpath(__file__).split('/')[:-2]
        path = '/'.join(path) + '/course/%s/homework/%s'%(courseid, homeworkid)
        filename = studentuserid
        return send_from_directory(path.encode('utf-8'), filename, as_attachment=True)
    else:
        import os
        path = os.path.realpath(__file__).split('/')[:-2]
        path = '/'.join(path) + '/course/%s/homework/%s'%(courseid, homeworkid)
        all_file = os.walk(path)
        for (a,b,c) in all_file:
            for item in c:
                if item.split('.')[0] == studentuserid:
                    filename = item
        return redirect('/homework/download/%s/%s/%s'%(courseid,homeworkid,filename))

