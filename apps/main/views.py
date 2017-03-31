#coding=utf-8
from uliweb import expose, functions

def __begin__():
    """
    用户验证 权限验证
    """
    from uliweb import functions
    functions.require_login()
    return
@expose('/')
def index():
    return {}
@expose('/left')
def left():
    return {}

