#-*-coding:utf-8-*-

def check_username_exist(username):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from user where username="%s"'%username)
    if cur.rowcount == 0:
        sql.close()
        return False
    sql.close()
    return True

def user_register(username, password, email, phone, name, studentid, usertype):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    command = 'insert into user values(NULL,"%s","%s","%s","%s","%s","%s",%s)'%(username, password, email, phone, name, studentid, usertype)
    command = command.encode('utf-8')
    cur.execute(command)
    sql.conn.commit()
    sql.close()

def update_user_info(email, phone, name, studentid, userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    command = 'update user set email="%s",phone="%s",name="%s",studentid="%s" where id=%s'%(email, phone, name, studentid, userid)
    command = command.encode('utf-8')
    cur.execute(command)
    sql.conn.commit()
    sql.close()

def user_login(username, password, session):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select id from user where username="%s" and password="%s"'%(username, password))
    res = []
    if cur.rowcount == 0:
        sql.close()
        return False
    for item in cur:
        res.append(item[0])
    sql.close()

    from model.redisdb import RedisDB
    con = RedisDB().con
    con.set('session2username:%s'%session, res[0])

    return True

def get_userid_by_session(session):
    from model.redisdb import RedisDB
    con = RedisDB().con
    userid = con.get('session2username:%s'%session)
    print userid
    return userid

def get_info_by_id(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from user where id=%s'%userid)
    res = []
    for item in cur:
        res.append(item)
    info_data = res[0]
    info = {}
    info['username'] = info_data[1]
    info['email'] = info_data[3]
    info['phone'] = info_data[4]
    info['name'] = info_data[5]
    info['studentid'] = info_data[6]
    return info

def is_teacher(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select usertype from user where id=%s'%userid)
    res = []
    for item in cur:
        res.append(item)
    info_data = res[0]
    if str(info_data[0]) == '2':
        return True
    return False

def get_name_by_userid(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select name from user where id=%s'%userid)
    res = []
    for item in cur:
        res.append(item)
    return res[0][0]

def check_user_is_teacher(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from user where id=%s and usertype=2'%userid)
    if cur.rowcount == 0:
        return False
    return True
