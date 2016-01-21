# 筋斗云学堂

## 环境配置

本项目使用gunicorn+flask作为后台，mysql+redis作为数据库，部署在ubuntu server操作系统上，可以用以下指令进行配置

```bash

# 安装python第三方库
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo pip install flask
sudo pip install pymysql
sudo pip install redis
sudo pip install gevent

# 安装git
sudo apt-get install git

# 下载源码
git clone https://github.com/zengzhaoyang/zlysb.git

# 安装mysql
sudo apt-get install mysql-server

# 安装redis 并启动
wget http://download.redis.io/releases/redis-3.0.6.tar.gz
tar xf redis-3.0.6.tar.gz
cd redis-3.0.6
make
cd src
./redis-server &

# 安装gunicorn
sudo apt-get install gunicorn

# 运行程序
cd $(SRCROOT)  # 进入源码路径
source work &  # 可以修改gun.conf配置以及config/__init__.py的配置
```