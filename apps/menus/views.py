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
@expose('/menus')
class menus():
    def __init__(self):

        self.model = functions.get_model('category')

    def list(self):
        return {}

    def getlist(self):
        # page = int(request.GET.get('page',1))
        # rows = int(request.GET.get('rows',10))
        #分页: 结果集 = 结果集.offset((页号-1)*每页条数).limit(每页条数)
        # menus = self.model.all().offset((page-1)*rows).limit(rows)
        result = {}
        # total = self.model.all().count()
        # result = {'total':total}

        menus = self.model.all()
        #把结果中的每条信息都转成dict
        #all_menus = [ menu.to_dict() for menu in menus ]
        #result['rows'] = all_menus
        #return json(result)

        parentcat_list = []
        children_dict = {}
        #把一级菜单和二级菜单区分开来
        #二级菜单放在以父菜单id为key 的dict中
        for menu in menus:
            if menu.parentid == 0:
                parentcat_list.append(menu.to_dict())
            else:
                if children_dict.has_key(menu.parentid):
                    children_dict[menu.parentid].append(menu.to_dict())
                else:
                    children_dict[menu.parentid] = [menu.to_dict(),]

        newmenus_list = []
        #把二级菜单填进一级菜单
        for parent in parentcat_list:
            newmenus_list.append(parent)
            if children_dict.has_key(parent['id']):
                newmenus_list += children_dict[parent['id']]

        result['rows'] = newmenus_list
        return json(result)

    def get_parent(self):
        '''
        获取父菜单
        :return: join([{},{}])
        '''

        all_parent = self.model.filter(self.model.c.parentid=='0')
        if not all_parent:
            all_parent = []
        all_parent = [parent.to_dict() for parent in all_parent]
        all_parent = [{"catname":"无","id":0}] + all_parent

        return json(all_parent)

    def _get_cat(self,id):
        '''
        获取菜单信息
        '''

        menu = self.model.get(int(id))
        return menu

    def getcat_json(self,id):
        '''
        获取json格式的菜单信息
        '''
        cat = self._get_cat(id)
        if not cat:
            error("条目不存在")
        cat = cat.to_dict()

        return json(cat)



    def save(self,):
        #获取post数据
        id = request.POST.get('id',None)
        catname = request.POST.get('catname')
        parentid = request.POST.get('parentid','0')
        url = request.POST.get('url','')
        isshow = request.POST.get('isshow',True)

        print id

        if not catname:
            message = '菜单名称不能为空!'
            returncode = 500
        elif id == parentid:
            message = '父菜单不能为自己!'
            returncode = 500
        else:
            try:
                if id:
                     #修改信息
                    cat = self._get_cat(id)
                    cat.catname = catname
                    cat.parentid = parentid
                    cat.url = url
                    cat.isshow = isshow

                    cat.save()

                    message = '导航菜单修改成功！'
                    returncode = 200
                else:
                    #新增信息
                    menu = self.model(catname=catname,parentid=parentid,url=url,isshow=isshow)
                    menu.save()

                    message = '导航菜单新增成功！'
                    returncode = 200
            #字段重复
            except exc.IntegrityError as e:
                returncode = 501
                #获取返回的错误信息
                error_info = e.orig.args[1]
                if 'catname' in error_info:
                    message = '菜单名字已存在'
                else:
                    message = '未知错误'
            except:
                message = '导航菜单新增失败，请联系开发人员'
                returncode = 500

            return json({'returncode':returncode,'message':message,})


    def delete(self,):
        '''删除
        '''

        menu_id = request.POST.getlist('id[]',None)
        print menu_id

        if not menu_id:
            message = '请选择你要删除的菜单!'
            returncode = 500
        else:
            # self.model.filter(self.model.c.id.in_(menu_id)).remove()
            menus={}
            for id in menu_id:
                cat = self._get_cat(int(id))
                if cat:
                    menus[id] = cat
                else:
                    message = '你选择了不存在的菜单'
                    returncode = 500
                    return json({'returncode':returncode,'message':message,})
            try:
                for id in menu_id:
                    menus[id].delete()

                message = '菜单删除成功！'
                returncode = 200
            except:
                message = '菜单删除失败，请联系开发人员'
                returncode = 500

            return json({'returncode':returncode,'message':message,})

    def ztreedata(self):
        menus = self.model.filter(self.model.c.isshow=='1')
        parentcat_list = []
        children_dict = {}
        #把一级菜单和二级菜单区分开来
        #二级菜单放在以父菜单id为key 的dict中
        for menu in menus:
            if menu.parentid == 0:
                parentcat_list.append(menu.to_dict())
            else:
                if children_dict.has_key(menu.parentid):
                    children_dict[menu.parentid].append(menu.to_dict())
                else:
                    children_dict[menu.parentid] = [menu.to_dict(),]

        #把二级菜单填进一级菜单
        for parent in parentcat_list:
            if children_dict.has_key(parent['id']):
                parent['children'] = children_dict[parent['id']]
            else:
                parent['isParent'] = True

        return json(parentcat_list)
