#-*-coding:utf-8-*-

def get_course_by_userid(userid, isteacher):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    if isteacher == False:
        cur.execute('select courseattend.courseid,course.name,course.teacher from course,courseattend,user where user.id=%s and courseattend.studentid=user.studentid and course.id=courseattend.courseid'%userid)
        res = []
        for item in cur:
            res.append({'courseid':item[0],'name':item[1].decode('utf-8'),'teacher':item[2].decode('utf-8')})
        sql.close()
        return res
    else:
        cur.execute('select course.id,course.name from course,user where course.teacher=user.name and user.id=%s'%userid)
        res = []
        for item in cur:
            res.append({'courseid':item[0],'name':item[1].decode('utf-8')})
        sql.close()
        return res
def check_attend_course(userid, courseid, isteacher):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    if isteacher == False:
        cur.execute('select * from courseattend,user where user.id=%s and courseattend.studentid=user.studentid and courseid=%s'%(userid, courseid))
        if cur.rowcount != 0:
            return True
        return False
    else:
        cur.execute('select * from course,user where course.teacher=user.name and user.id=%s'%userid)
        if cur.rowcount != 0:
            return True
        return False

def add_course(teacher, name, description, time, classroom, filename):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    command = 'insert into course values(NULL,"%s","%s","%s","%s","%s")'%(teacher, name, description, time, classroom)
    command = command.encode('utf-8') 
    cur.execute(command)
    sql.conn.commit()
    cur.execute('select * from course')
    courseid = cur.rowcount
    import os
    path = os.path.realpath(__file__)
    filepath = '/'.join(path.split('/')[:-2]) + '/tmp/' + filename
    path = '/'.join(path.split('/')[:-2]) + '/course/%d'%courseid
    os.system("mkdir -p %s/homework"%path)
    os.system("mkdir -p %s/resource"%path)

    f = open(filepath)
    data = f.read()
    f.close()
    data = data.split()
    command = ''
    for item in data:
        import re
        temp = re.split(',|;', item)
        print temp
        studentid = temp[0]
        name = temp[1]
        command += 'insert into courseattend values(%s,"%s");'%(courseid, studentid)
       # line = f.readline();
    print command
    cur.execute(command)
    sql.conn.commit()
    sql.close()

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

def get_homework_by_courseid(courseid, userid):
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
    cur.execute('select homeworkid from homeworksubmit where userid=%s'%userid)
    homeworklist = []
    for item in cur:
        homeworklist.append(item[0])
    for i in range(len(res)):
        homeworkid = res[i]['id']
        if homeworkid in homeworklist:
            res[i]['issubmit'] = '1'
        else:
            res[i]['issubmit'] = '0'
    sql.close()
    return res

def get_studentlist_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select user.id,user.name,user.studentid from user,courseattend where courseattend.courseid=%s and courseattend.studentid=user.studentid'%courseid)
    res = []
    for item in cur:
        res.append((item[0],item[2],item[1]))
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
    command = 'insert into homework values(NULL,%s,"%s","%s")'%(courseid, description, deadline)
    command = command.encode('utf-8')
    cur.execute(command)
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
    command = 'insert into resource values(%s,"%s")'%(courseid, filename)
    command = command.encode('utf-8')
    cur.execute(command)
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
    command = 'insert into news values(NULL,%s,"%s","%s",%d)'%(courseid, description, publisher, newstype)
    command = command.encode('utf-8')
    print command
    cur.execute(command)
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
            'newstype':str(item[2])
            })
    sql.close()
    return res

def get_course_teacher_info_by_courseid(courseid):
    from model.mysql import MySQL
    sql = MySQL()
    cur = sql.cur
    cur.execute('select user.name,user.email,user.avatar from user,course where courseid=%s and user.nane=course.teacher'%courseid)
    res = []
    for item in cur:
        res.append({'teachername':item[0],'teacheremail':item[1],'teacheravatar':item[2]})
    sql.close()
    return res[0]
