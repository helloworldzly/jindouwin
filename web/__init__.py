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
    from lib import is_teacher
    if is_teacher(userid):
        return render_template('course_admin.html', courseid=courseid)
    else:
        return render_template('course.html', courseid=courseid)

@app.route('/course_admin/<courseid>', methods=['GET'])
def course_admin(courseid):
    return render_template('course_admin.html', courseid=courseid)

@app.route('/downloads', methods=['GET'])
def downloads():
    pass

@app.route('/news', methods=['GET'])
def news():
    pass

@app.route('/resource/<courseid>/<filename>', methods=['GET'])
def resource(courseid, filename):
    import os
    path = os.path.realpath(__file__).split('/')[:-2]
    path = '/'.join(path) + '/course/%s/resource/'%courseid
    return send_from_directory(path, filename,as_attachment=True)
