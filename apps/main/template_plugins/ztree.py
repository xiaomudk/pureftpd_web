#!/usr/bin/python
# coding=utf-8

def call(version='3.5.23'):

	a = []

	name = 'zTree_v' + version

	a.append(name + '/css/zTreeStyle/zTreeStyle.css')
	a.append(name + '/js/jquery.ztree.core.js')
	a.append(name + '/js/jquery.ztree.excheck.js')

	return {'toplinks':a}
