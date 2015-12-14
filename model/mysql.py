#-*-coding:utf-8-*-

import pymysql
from config import *

class MySQL:
    def __init__(self):
        self.conn = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
        self.cur = self.conn.cursor()
    def close(self):
        self.cur.close()
        self.conn.close()
