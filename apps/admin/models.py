#!/usr/bin/python
# coding=utf-8

from uliweb.orm import *

class Admin(Model):
    '''
    后台登陆用户管理
    '''
    __table_args__ = {'mysql_engine':'MyISAM'}
    Username = Field(str, verbose_name="用户名", max_length=35, required=True,index=True,unique=True,nullable=False)
    Password = Field(CHAR, verbose_name="密码", max_length=100,required=True,nullable=False,server_default='')
    Email = Field(str, verbose_name="联系邮箱", max_length=32,server_default='')
    Add_time = Field(datetime.datetime, verbose_name='提交时间', auto_now_add=True, format='%Y-%m-%d %H:%M:%S')