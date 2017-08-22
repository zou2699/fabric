#!/usr/bin/env python
# encoding: utf-8
# Author: zouhl
# Created Time : 2017年08月22日 星期二 21时27分37秒
# File Name: yisa.py
# Description:


from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm

env.user = 'root'
#env.hosts = ['192.168.42.143','192.168.42.130']
env.port = 22
env.password = 'z'
#定义组
env.roledefs = {
        'web_server': ['192.168.42.143'],
        'db_server': ['192.168.42.130'],
        'gpu_server': ['192.168.42.130']
        }
lpath='/tmp/srv.tar.gz'
rpath='/tmp/test/'

#该装饰的组才能执行
@roles('db_server')
def task1():
    cmd = prompt('plz input cmd to run:', default="hostname")
    if confirm('really to run cmd,contine?'):
        run(cmd)

#上传压缩包
@roles('gpu_server')
def srv():
    run('mkdir -p /tmp/test/')
    with settings(warn_only=True):
        result = put(lpath,rpath)
    if result.failed and not confirm('put file failed,continue[Y/N]?'):
        abort("Aborting file put task!")
    print blue('put file success')

#解压压缩包
@roles('gpu_server')
def install_srv():
    with cd('/tmp/test/'):
        run('tar zxvf srv.tar.gz')
    print blue('success')
#执行上面修饰的方法
def go():
    #execute(task1)
    execute(srv)
    execute(install_srv)
