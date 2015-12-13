#-*-coding:utf-8-*-

from server import app
from flask import render_template, make_response, request, redirect

@app.route('/login', methods=['GET'])
def login():
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_username_by_session
        username = get_username_by_session(session)
        if username != None:
            return redirect('/')
    else:
        from lib import generate_session
        session = generate_session()
    resp = make_response(render_template('login.html'))
    resp.set_cookie('session', session, max_age=120)
    return resp

@app.route('/login2', methods=['GET'])
def login2():
    return render_template('login.html')

@app.route('/', methods=['GET'])
def index():
    cookies = request.cookies
    if 'session' in cookies:
        session = cookies['session']
        from lib import get_username_by_session
        username = get_username_by_session(session)
        if username == None:
            return redirect('/login')
        else:
            resp = make_response(render_template('index.html', username=username))
            return resp
    else:
        return redirect('/login')

@app.route('/2', methods=['GET'])
def index2():
    return render_template('index.html')

@app.route('/course', methods=['GET'])
def course():
    return render_template('course.html')

@app.route('/downloads', methods=['GET'])
def downloads():
    pass

@app.route('/news', methods=['GET'])
def news():
    pass