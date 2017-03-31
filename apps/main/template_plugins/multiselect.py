#!/usr/bin/python
# coding=utf-8

def call():

	a = []

	name = 'multiselect'

	a.append(name + '/css/bootstrap.min.css')
	a.append(name + '/js/multiselect.min.js')

	return {'toplinks':a}
