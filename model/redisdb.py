#-*-coding:utf-8-*-

from redis import Redis
from config import *

class RedisDB:
	def __init__(self):
		self.con = Redis(REDIS_HOST, REDIS_PORT)