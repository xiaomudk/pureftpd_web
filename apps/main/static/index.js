/**
 * Created by xixi.zhu on 2016/4/6,0006.
 */

var setting = {
    async: {
        enable: true,
        url:"/menus/ztreedata",
	},
	view: {
		showLine: false,
		selectedMulti: false,
		dblClickExpand: false,
		showIcon: false,
		//addDiyDom: addDiyDom
	},
	data: {
		key:{
			name:"catname",
			//当后台数据只能生成 url 属性，又不想实现点击节点跳转的功能时，可以直接修改此属性为其他不存在的属性名称
			//这里如果不修改，会新打开一个页面
			url:"xurl",
		}
	},
	callback: {
		onAsyncSuccess: function (event, treeId, treeNode, msg){
			var zTreeObj = $.fn.zTree.getZTreeObj("menuTree");
			var curMenu = zTreeObj.getNodes()[0];
			zTreeObj.expandNode(curMenu);
			var a = $("#" + curMenu.tId + "_a");
			a.addClass("cur");
		},
		beforeClick: this.beforeClick,
		onClick:function(e, id, node){
			//var zTreeObj = $.fn.zTree.getZTreeObj("menuTree");
			////如果是父菜单刚展开，如果是子菜单，再执行addTabs函数
			//if(node.isParent) {
			//	if(node.children) {
			//		zTreeObj.expandNode(node);
			//	}
			//} else {
				addTabs(node.catname, node.url);
			//}
		}
	}
};
function beforeClick(treeId, node) {
	var zTreeObj = $.fn.zTree.getZTreeObj("menuTree");
	if (node.isParent) {
			var allNodes = zTreeObj.getNodes();
			for (var i=0,l=allNodes.length;i<l;i++){
				if (allNodes[i].open){
					var pNode = allNodes[i];
					break;
				}
			}
			if (pNode !== node) {
				var a = $("#" + pNode.tId + "_a");
				a.removeClass("cur");
				zTreeObj.expandNode(pNode, false);
			}
			a = $("#" + node.tId + "_a");
			a.addClass("cur");

			zTreeObj.expandNode(node, true);
		}
	return !node.isParent;
}

function addDiyDom(treeId, treeNode) {
			var spaceWidth = 5;
			var switchObj = $("#" + treeNode.tId + "_switch"),
			icoObj = $("#" + treeNode.tId + "_ico");
			switchObj.remove();
			icoObj.before(switchObj);

			if (treeNode.level > 1) {
				var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level)+ "px'></span>";
				switchObj.before(spaceStr);
			}
		}

$(function() {
	$.fn.zTree.init($("#menuTree"), setting);
	var zTreeObj = $.fn.zTree.getZTreeObj("menuTree");
	var firstMenu = zTreeObj.getNodes()[0];
	zTreeObj.expandNode(firstMenu);

	//中间部分tab
	$('#tabs').tabs({
		border:false,
		fit:true,
		onSelect: function(title, index){
			var treeNode = zTreeObj.getNodeByParam("name", title, null);
			zTreeObj.selectNode(treeNode);
		}
	});

	$('.index_panel').panel({
	  width:300,
	  height:200,
	  closable:true,
	  minimizable:true,
	  title: 'My Panel'
	});

});

//添加一个选项卡面板
function addTabs(title, url, icon){
	if(!$('#tabs').tabs('exists', title)){
		$('#tabs').tabs('add',{
			title:title,
			content:'<iframe src="'+url+'" frameBorder="0" border="0" scrolling="no" style="width: 100%; height: 100%;"/>',
			closable:true
		});
	} else {
		$('#tabs').tabs('select', title);
	}
}

