#-*-coding:utf-8-*-

def check_username_exist(username):
	from mysql import MySQL
	sql = MySQL()
	cur = sql.cur
	cur.execute('select * from user where username="%s"'%username)
	if cur.rowcount == 0:
		sql.close()
		return False
	sql.close()
	return True

def user_register(username, password, email, phone, name, studentid, usertype):
	from mysql import MySQL
	cur = MySQL().cur
	cur.execute('insert into user values(NULL,"%s","%s","%s","%s","%s","%s",%s)'%(username, password, email, phone, name, studentid, usertype))
	cur.close()

def user_login(username, password, session):
	from mysql import MySQL
	sql = MySQL()
	cur = sql.cur
	cur.execute('select id from user where username="%s" and password="%s"'%(username, password))
	if cur.rowcount == 0:
		sql.close()
		return False
	sql.close()

	from redisdb import RedisDB
	con = RedisDB().con
	con.set('session2username:%s'%session, id)

	return True

def get_userid_by_session(session):
	from redisdb import RedisDB
	con = RedisDB().con
	userid = con.get('session2username:%s'%session)
	return userid

def get_info_by_id(userid):
	from mysql import MySQL
	sql = MySQL()
	cur = sql.cur
	cur.execute('select * from user where id=%s'%userid)
	res = []
	for item in cur:
		res.append(item)
	info_data = res[0]
	info = {}
	info['email'] = info_data[3]
	info['phone'] = info_data[4]
	info['name'] = info_data[5]
	info['studentid'] = info_data[6]
	return info
