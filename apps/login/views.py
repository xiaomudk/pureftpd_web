#coding=utf-8
from uliweb import expose, functions
import urllib


def login():

    if request.method == 'GET':
        return {}
    if request.method == 'POST':

        username= request.POST.get('username')
        password= request.POST.get('password')

        f, d = functions.authenticate(username=username, password=password)

        if f:
            functions.login(username)
            next = urllib.unquote(request.POST.get('next','/'))

            message = next
            returncode = 200
        else:

            message = '账户或密码错误'
            returncode = 500
        return json({'returncode':returncode,'message':message,})

def logout():
    from uliweb.contrib.auth import logout as out
    out()
    next = urllib.unquote(request.GET.get('next', '/login'))
    return redirect(next)

@expose('/login/get_name')
def get_name():
    user = functions.get_user()
    if user:
        return json({'username':user.Username})
