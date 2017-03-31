/**
 *
 * Created by xixi.zhu on 2016/6/6,0006.
 */
/*
	扩展easyui中的控件方法或修改其默认属性
	@eric
 */

//翻页工具栏文字
if ($.fn.pagination){
	$.fn.pagination.defaults.showPageList=false;
	$.fn.pagination.defaults.beforePageText="第 <span id='currentPage'>1</span> 页  转到",
	$.fn.pagination.defaults.afterPageText = "页&nbsp; <a style='border:0;text-decoration:none; font-size:15px;font-weight:bold;color:#8DB2E3' href='javascript:void(0);' onclick='jumpPage()'>GO</a>&nbsp; 共 {pages} 页";
	$.fn.pagination.defaults.displayMsg ="当前{from}-{to} 条  共{total}条记录";
}
if ($.fn.datagrid){
	$.fn.datagrid.defaults.loadMsg = '正在加载...';
}

//window窗体默认属性
$.fn.window.defaults.resizable=false;
$.fn.window.defaults.collapsible=false;
$.fn.window.defaults.minimizable=false;
$.fn.window.defaults.maximizable=false;
$.fn.window.defaults.shadow=false;
$.fn.window.defaults.modal=true;
$.fn.window.defaults.loadingMessage = '正在加载...';

//信息框按钮文字
if ($.messager){
	$.messager.defaults.ok = '确定';
	$.messager.defaults.cancel = '取消';
}

$.extend($.fn.validatebox.defaults.rules, {
    /*必须和某个字段相等*/
    equalTo: {
        validator:function(value,param){
            return $(param[0]).val() == value;
        },
        message:'字段不匹配'
    },
	ip : {// 验证IP地址
				validator : function(value) {
                    if (value != '*'){
                        return /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/i.test(value);
                    } else {
						return true;
					}
				},
				message : 'IP地址格式不正确'
			},
	 //数字
    number: {
        validator: function (value) {
            var reg =/^[0-9]*$/;
            return reg.test(value);
        },
        message: '必须为数字'
    },
	account: {//param的值为[]中值
        validator: function (value, param) {
            if (value.length < param[0] || value.length > param[1]) {
                $.fn.validatebox.defaults.rules.account.message = '用户名长度必须在' + param[0] + '至' + param[1] + '范围';
                return false;
            } else {
                if (!/^[\w]+$/.test(value)) {
                    $.fn.validatebox.defaults.rules.account.message = '用户名只能数字、字母、下划线组成.';
                    return false;
                } else {
                    return true;
                }
            }
        }, message: ''
    },

});
