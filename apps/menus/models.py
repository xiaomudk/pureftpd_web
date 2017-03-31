#!/usr/bin/python
# coding=utf-8

from uliweb.orm import *

class Category(Model):
    '''
    后台菜单
    '''
    # __without_id__ = True

    # id = Field(int,verbose_name="菜单id",primary_key=True,autoincrement=True)
    catname = Field(str, verbose_name='菜单名称',required=True,unique=True)
    parentid = Field(int,verbose_name="父菜单id", server_default=0,index=True,)
    url = Field(str,verbose_name='菜单地址')
    isshow = Field(bool,verbose_name='是否显示',server_default=1,nullable=False)