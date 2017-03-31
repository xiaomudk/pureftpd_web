#coding=utf-8
from uliweb import expose, functions
from uliweb.orm import get_model
from sqlalchemy import exc

def __begin__():
    """
    用户验证 权限验证
    """
    from uliweb import functions
    functions.require_login()
    return
@expose('/pureftpd')
class pureftpd():
    def __init__(self):

        self.model = functions.get_model('ftpusers')

    def list(self):
        return {}

    def getlist(self):
        page = int(request.GET.get('page',1))
        rows = int(request.GET.get('rows',10))

        #分页: 结果集 = 结果集.offset((页号-1)*每页条数).limit(每页条数)
        ftpusers = self.model.all().offset((page-1)*rows).limit(rows)
        result = {}
        total = self.model.all().count()
        result = {'total':total}

        #把结果中的每条信息都转成dict
        all_ftpusers = [ ftpuser.to_dict() for ftpuser in ftpusers ]
        result['rows'] = all_ftpusers
        return json(result)


        result['rows'] = ftpusers
        return json(result)


    def _get_ftpuser(self,id):
        '''
        获取菜单信息
        '''

        ftpuser = self.model.get(int(id))
        return ftpuser

    def getftpuser_json(self,id):
        '''
        获取json格式的菜单信息
        '''
        print id
        ftpuser = self._get_ftpuser(id)
        if not ftpuser:
            error("条目不存在")
        ftpuser = ftpuser.to_dict()

        return json(ftpuser)

    def _get_value(self,fileds,value):

        model_dict = self.model.properties
        if value == None or len(value) == 0:
            if model_dict[fileds].kwargs.has_key('server_default'):
                value =  model_dict[fileds].kwargs['server_default']

        #如果是bool型，刚先把value转为int型
        if model_dict[fileds].data_type==bool:
            if value == 'true':
                value = 1
            elif value == 'false':
                value = 0
            else:
                value = int(value)
        value = model_dict[fileds].data_type(value)
        #加密
        if fileds == 'Password':
            value = functions.get_hexdigest('md5',value)
        return value

    def get_all_defalut(self):
        form_data = {}
        for k in self.model.properties:
            form_data[k] = self._get_model_defalult(k)

        return json(form_data)



    def save(self,):
        #获取post数据
        #遍历数据库的字段，从form表单里来获取对应字段的值
        #表单提交的字段 必须 与数据库字段一一对应
        model_columns = self.model.properties.keys()

        form_data = request.form.to_dict()

        #set(s).issubset(t) 是否 s 中的每一个元素都在 t 中
        #判断post过来的数据是否完整
        if  not set(model_columns).issubset(form_data.keys()+['Password','id']):
            message = '恶意的提交'
            returncode = 500
            return json({'returncode':returncode,'message':message,})


        if not form_data['User'] :

            message = '用户名不能为空!'
            returncode = 500
            return json({'returncode':returncode,'message':message,})

        try:
            if form_data.has_key('id') and len(form_data['id']) !=0:
                print form_data
                print model_columns
                 #修改信息
                ftpuser_id = self._get_ftpuser(form_data['id'])
                 #删除密码字段
                model_columns.remove('Password')
                for k in model_columns:
                    value = self._get_value(k,form_data[k])
                    form_data[k] = value
                ftpuser = ftpuser_id.update(**form_data)


                message = '用户修改成功！'
                returncode = 200
            else:
                if len(form_data['Password'])==0 or  form_data['Password'] != form_data['Password2']:
                    message = '密码不能为空且两次输入的密码必须一致'
                    returncode = 500
                    return json({'returncode':returncode,'message':message,})
                #新增信息
                model_columns.remove('id')
                for k in model_columns:
                    value = self._get_value(k,form_data[k])
                    form_data[k] = value
                ftpuser = self.model(**form_data)

                message = '用户新增成功！'
                returncode = 200
            ftpuser.save()
        #字段重复
        except exc.IntegrityError as e:
            returncode = 501
            #获取返回的错误信息
            error_info = e.orig.args[1]
            if 'User' in error_info:
                message = '用户名已存在'
            else:
                message = '未知错误'
        except Exception,e:
            print e
            message = '用户新增失败，请联系开发人员'
            returncode = 500

        return json({'returncode':returncode,'message':message,})

    def savepassword(self):
        form_data = request.form.to_dict()
        print form_data
        if len(form_data['Password'])==0 or  form_data['Password'] != form_data['Password2']:
            message = '密码不能为空且两次输入的密码必须一致'
            returncode = 500
            return json({'returncode':returncode,'message':message,})
        try:
            #修改信息
            ftpuser_id = self._get_ftpuser(form_data['id'])
            #删除密码字段
            form_data['Password'] = self._get_value('Password',form_data['Password'])
            ftpuser = ftpuser_id.update(**form_data)
            ftpuser.save()

            message = '密码修改成功！'
            returncode = 200
        except Exception,e:
            print e
            message = '用户新增失败，请联系开发人员'
            returncode = 500


        return json({'returncode':returncode,'message':message,})

    def delete(self,):
        '''删除
        '''

        ftp_ids = request.POST.getlist('id[]',None)

        if not ftp_ids:
            message = '请选择你要删除的用户!'
            returncode = 500
        else:
            # self.model.filter(self.model.c.id.in_(menu_id)).remove()
            ftpusers={}
            for id in ftp_ids:
                ftpuser = self._get_ftpuser(int(id))
                if ftpuser:
                    ftpusers[id] = ftpuser
                else:
                    message = '你选择了不存在的用户'
                    returncode = 500
                    return json({'returncode':returncode,'message':message,})
            try:
                for id in ftp_ids:
                    ftpusers[id].delete()

                message = '用户删除成功！'
                returncode = 200
            except Exception,e:
                print e
                message = '用户删除失败，请联系开发人员'
                returncode = 500

            return json({'returncode':returncode,'message':message,})
