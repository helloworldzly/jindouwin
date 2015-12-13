#-*-coding:utf-8-*-

def get_course_by_userid(userid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select courseattend.courseid,course.name from course,courseattend where courseattend.userid="%s" and course.id=courseattend.courseid'%userid)
    res = []
    for item in cur:
        res.append({'course':item[0],'name':item[1]})
    sql.close()
    return res

def check_attend_course(userid, courseid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from courseattend where userid="%s" and courseid="%s"'%(userid, courseid))
    if cur.rowcount != 0:
        return True
    return False

def get_info_by_courseid(courseid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from course where id="%s"'%courseid)
    res = []
    for item in cur:
        res.append(item)
    sql.close()
    course_data = res[0]
    course = {}
    course["id"] = course_data[0]
    course["teacher"] = course_data[1]
    course["name"] = course_data[2]
    course["description"] = course_data[3]
    course["time"] = course_data[4]
    course["classroom"] = course_data[5]
    return course

def get_news_by_courseid(courseid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select news from coursenews where courseid="%s"'%courseid)
    res = []
    for item in cur:
        res.append(item)
    sql.close()
    return res

def get_homework_by_courseid(courseid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from homework where courseid="%s"'%courseid)
    res = []
    for item in cur:
        temp = item
        res.append({
            'id':temp[0],
            'description':temp[1],
            'deadline':temp[2]
            })
    sql.close()
    return res

def check_id_course_teacher(userid, courseid):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from course,user where user.id="%s" and course.teacher=user.name'%userid)
    if cur.rowcount == 0:
        sql.close()
        return False
    sql.close()
    return True

def add_homework_by_courseid(courseid, description, deadline):
    from mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into homework values(NULL,"%s","%s")'%(description, deadline))
    sql.close()