#coding=utf-8
from uliweb import expose, functions
from uliweb import response
from uliweb.orm import get_model
from sqlalchemy import exc
from sqlalchemy.sql import select,or_

# def __begin__():
#     """
#     用户验证 权限验证
#     """
#     from uliweb import functions
#     functions.require_login()
#     return
@expose('/pureftpd')
class ftpgroups():
    def __init__(self):

        self.groupsmodel = functions.get_model('ftpgroups')
        self.usersmodel= functions.get_model('ftpusers')

    def groups(self):
        #定义模板目录
        response.template = 'pureftpd/groups.html'
        return {}

    def getgroupslist(self):
        page = int(request.GET.get('page',1))
        rows = int(request.GET.get('rows',10))

        #分页: 结果集 = 结果集.offset((页号-1)*每页条数).limit(每页条数)
        groups = self.groupsmodel.all().offset((page-1)*rows).limit(rows)
        result = {}
        total = self.groupsmodel.all().count()
        result = {'total':total}

        #把结果中的每条信息都转成dict
        all_ftpusers = [ group.to_dict() for group in groups ]
        result['rows'] = all_ftpusers
        return json(result)


        result['rows'] = ftpusers
        return json(result)


    def _get_ftpgroup(self,id):
        '''
        获取菜单信息
        '''

        ftpgroup = self.groupsmodel.get(int(id))
        return ftpgroup

    def getgroup_json(self,id):
        '''
        获取json格式的菜单信息
        '''
        print id
        ftpgroup = self._get_ftpgroup(id)
        if not ftpgroup:
            error("条目不存在")
        ftpgroup = ftpgroup.to_dict()

        return json(ftpgroup)

    def _get_value(self,fileds,value):

        model_dict = self.groupsmodel.properties
        if value == None or len(value) == 0:
            if model_dict[fileds].kwargs.has_key('server_default'):
                value =  model_dict[fileds].kwargs['server_default']

        #如果是bool型，刚先把value转为int型
        if model_dict[fileds].data_type==bool:
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

    def getgroup_users(self,id):
        group = self._get_ftpgroup(id)

        group_users = group.Users.ids() or [0,]

        ftpgroups_userid = self.groupsmodel.Users.table.c[self.groupsmodel.Users.fieldb]
        ftpgroups_groupid= self.groupsmodel.Users.table.c[self.groupsmodel.Users.fielda]
        #查找出来所有
        #a = select([ftpgroups_userid]).where(ftpgroups_groupid != id).group_by(ftpgroups_userid)
        a = select([ftpgroups_userid]).group_by(ftpgroups_userid)
        all_users = self.usersmodel.filter(or_(self.usersmodel.c.id.notin_(a),self.usersmodel.c.id.in_(group_users))).all()

        alluser_json = []

        for user in all_users:
            user_dict = user.to_dict()
            if user.id in group_users:
                user_dict.update({'selected':True})
            else:
                user_dict.update({'selected':False})

            alluser_json.append(user_dict)

        return json(alluser_json)


    def groups_save(self,):
        #获取post数据
        #遍历数据库的字段，从form表单里来获取对应字段的值
        #表单提交的字段 必须 与数据库字段一一对应
        model_columns = self.groupsmodel.properties.keys()
        print model_columns

        form_data = request.form.to_dict()
        print form_data

        #set(s).issubset(t) 是否 s 中的每一个元素都在 t 中
        #判断post过来的数据是否完整
        if  not set(model_columns).issubset(form_data.keys()+['Users','id']):
            message = '恶意的提交'
            returncode = 500
            return json({'returncode':returncode,'message':message,})


        if not form_data['GroupName'] :

            message = '用户组名不能为空!'
            returncode = 500
            return json({'returncode':returncode,'message':message,})

        try:
            if form_data.has_key('id') and len(form_data['id']) !=0:
                print form_data
                print model_columns
                 #修改信息
                ftpgroup_id = self._get_ftpgroup(form_data['id'])
                model_columns.remove('Users')
                for k in model_columns:
                    value = self._get_value(k,form_data[k])
                    form_data[k] = value
                ftpgroup = ftpgroup_id.update(**form_data)


                message = '用户组修改成功！'
                returncode = 200
            else:
                #新增信息
                model_columns.remove('id')
                model_columns.remove('Users')
                for k in model_columns:
                    value = self._get_value(k,form_data[k])
                    form_data[k] = value
                ftpgroup = self.groupsmodel(**form_data)

                message = '用户组新增成功！'
                returncode = 200
            ftpgroup.save()
        #字段重复
        except exc.IntegrityError as e:
            returncode = 501
            #获取返回的错误信息
            error_info = e.orig.args[1]
            if 'GroupName' in error_info:
                message = '用户名已存在'
            else:
                message = '未知错误'
        except Exception,e:
            print e
            message = '用户组新增失败，请联系开发人员'
            returncode = 500

        return json({'returncode':returncode,'message':message,})

    def save_groupuser(self):
        print request.form.to_dict()
        groupid = request.POST.get('id')
        users_list = request.POST.getlist('groupusers[]')
        print users_list

        group = self._get_ftpgroup(groupid)
        print self.usersmodel.filter(self.usersmodel.c.id.in_([1,2]))
        print self.usersmodel.filter(self.usersmodel.c.id.in_(users_list)).fields('id')
        ormdata_user = list(self.usersmodel.filter(self.usersmodel.c.id.in_(users_list)).fields('id'))
        group.Users.update(ormdata_user)
        returncode = 200
        message = '组成员设置成功！'
        return json({'returncode':returncode,'message':message,})




    def deletegroups(self,):
        '''删除
        '''

        groups_ids = request.POST.getlist('id[]',None)

        if not groups_ids:
            message = '请选择你要删除的用户组!'
            returncode = 500
        else:
            # self.model.filter(self.model.c.id.in_(menu_id)).remove()
            for id in groups_ids:
                group = self._get_ftpgroup(int(id))
                if not group:
                    message = '你选择了不存在的用户组'
                    returncode = 500
                    return json({'returncode':returncode,'message':message,})
            try:
                for id in groups_ids:
                    group = self.groupsmodel.get(int(id))
                    #从组中移除用户
                    group.Users.remove(group.Users.ids())
                    group.delete()

                message = '用户删除成功！'
                returncode = 200
            except Exception,e:
                print e
                message = '用户删除失败，请联系开发人员'
                returncode = 500

            return json({'returncode':returncode,'message':message,})
