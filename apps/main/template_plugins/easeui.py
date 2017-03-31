#!/usr/bin/python
# coding=utf-8

def call(version='1.4.4'):
    a = []

    easyui_name = 'jquery-easyui-' + str(version)

    a.append(easyui_name+'/themes/gray/easyui.css')
    a.append(easyui_name+'/themes/icon.css')
    # a.append(easyui_name+'/demo.css')
    a.append(easyui_name+'/jquery.min.js')
    a.append(easyui_name+'/jquery.easyui.min.js')

    return {'toplinks':a}

    # return {'bottomlinks':a}