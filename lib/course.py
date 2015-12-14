#-*-coding:utf-8-*-

def get_course_by_userid(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select courseattend.courseid,course.name,course.teacher from course,courseattend where courseattend.userid=%s and course.id=courseattend.courseid'%userid)
    res = []
    for item in cur:
        res.append({'courseid':item[0],'name':item[1],'teacher':item[2]})
    sql.close()
    return res

def check_attend_course(userid, courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from courseattend where userid=%s and courseid=%s'%(userid, courseid))
    if cur.rowcount != 0:
        return True
    return False

def add_course(teacher, name, description, time, classroom):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into course values(NULL,"%s","%s","%s","%s","%s")')
    sql.conn.commit()
    cur.execute('select * from course')
    courseid = cur.rowcount
    import os
    path = os.path.realpath(__file__)
    path = '/'.join(path[:-2]) + '/course/%d'%courseid
    os.system("mkdir %s/homework"%path)
    os.system("mkdir %s/resource"%path)

def get_info_by_courseid(courseid):
    from model.mysql import MySQL
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

# def get_news_by_courseid(courseid):
#     from model.mysql import MySQL
#     sql = MySQL()
#     cur = sql.cur
#     cur.execute('select id,description,publisher from news where courseid=%s'%courseid)
#     res = []
#     for item in cur:
#         temp = item
#         res.append({
#             'id':temp[0],
#             'description':temp[1],
#             'publisher':temp[2]
#             })
#     sql.close()
#     return res

def get_homework_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select id,description,deadline from homework where courseid=%s'%courseid)
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

def get_studentlist_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select userid from courseattend where courseid=%s'%courseid)
    res = []
    for item in cur:
        res.append(item[0])
    sql.close()
    return res

def get_homeworksubmit_by_homeworkid(homeworkid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select userid from homeworksubmit where homeworkid=%s'%homeworkid)
    res = []
    for item in cur:
        res.append(item[0])
    sql.close()
    return res

def check_is_course_teacher(userid, courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from course,user where user.id="%s" and course.teacher=user.name'%userid)
    if cur.rowcount == 0:
        sql.close()
        return False
    sql.close()
    return True

def check_homework_exist(homeworkid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select * from homework where id=%s'%homeworkid)
    if cur.rowcount == 0:
        sql.close()
        return False
    sql.close()
    return True

def add_homework_by_courseid(courseid, description, deadline):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into homework values(NULL,%s,"%s","%s")'%(courseid, description, deadline))
    sql.conn.commit()
    sql.close()

def homework_submit(userid, homeworkid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into homeworksubmit values(%s, %s)'%(userid, homeworkid))
    sql.conn.commit()
    sql.close()

def get_homework_submit_by_userid(userid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select homeworkid from homeworksubmit where usrid=%s'%userid)
    res = []
    for item in cur:
        res.append(item[0])
    sql.close()
    return res

def add_resource_by_courseid(courseid, filename):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into resource values(%s,"%s")'%(courseid, filename))
    sql.conn.commit()
    sql.close()

def get_resource_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select filename from resource where courseid=%s'%courseid)
    res = []
    for item in cur:
        res.append(item[0])
    sql.close()
    return res

def add_news_by_courseid(courseid, description, publisher, newstype):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('insert into news values(%s,"%s","%s","%s")')
    sql.conn.commit()
    sql.close()

def get_news_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select description,publisher,newstype from news where courseid=%s'%courseid)
    res = []
    for item in cur:
        res.append({
            'description':item[0],
            'publisher':item[1],
            'newstype':item[2]
            })
    sql.close()
    return res
