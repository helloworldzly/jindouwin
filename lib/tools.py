#-*-coding:utf-8-*-

def generate_session():
    import os
    from model.redisdb import RedisDB
    con = RedisDB().con
    code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    while True:
        if con.sismember('session',code) == False:
            con.sadd('session',code)
            break
        code = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    return code

