#!/usr/bin/python
# coding=utf-8
from uliweb.orm import *

class Ftpusers(Model):
    '''
    后台登陆用户管理
    '''
    __table_args__ = {'mysql_engine':'MyISAM'}

    User = Field(str, verbose_name="用户名", max_length=16, required=True,index=True,unique=True,nullable=False)
    Password = Field(str, verbose_name="密码", max_length=32,required=True,server_default='')
    Uid = Field(int, verbose_name='用户id',server_default=1000,nullable=False)
    Gid = Field(int, verbose_name='用户组id',server_default=1000,nullable=False)
    Dir = Field(str, verbose_name='用户家目录',max_length=128,server_default='',nullable=False)
    QuotaFiles = Field(int, verbose_name='文件数限制',server_default=0,nullable=False)
    QuotaSize = Field(int, verbose_name='空间大小限制',server_default=0,nullable=False)
    ULBandwidth = Field(int, verbose_name='上传限速',server_default=0,nullable=False)
    DLBandwidth = Field(int, verbose_name='下载限速',server_default=0,nullable=False)
    Ipaddress = Field(str, verbose_name='允许连接的ip',max_length=15,server_default='*',nullable=False)
    Status = Field(bool,server_default=1,nullable=False)
    RLRatio = Field(SMALLINT, verbose_name='上传比',server_default=1,nullable=False)
    DLRatio = Field(SMALLINT, verbose_name='下载比',server_default=1,nullable=False)
    Comment = Field(TEXT,verbose_name='备注')

class FtpHosts(Model):
    '''
    ftp主机管理
    '''
    __table_args__ = {'mysql_engine':'MyISAM'}

    HostName = Field(str, verbose_name="名称", max_length=32,required=True,index=True,unique=True,nullable=False)
    HostIp = Field(str, verbose_name="主机ip", max_length=32,required=True,nullable=False)
    Users = ManyToMany('ftpusers', verbose_name='Ftpusers', collection_name='HostUsers')
    FtpPort = Field(int, verbose_name="ftp端口",nullable=False,server_default=22)
    Comment = Field(TEXT,verbose_name='备注')

class FtpuserGroup(Model):
    '''
    ftp用户组
    '''
    __table_args__ = {'mysql_engine':'MyISAM'}
    GroupName = Field(str, verbose_name="名称", max_length=32,required=True,index=True,unique=True,nullable=False)
    Users = ManyToMany('ftpusers', verbose_name='Ftpusers', collection_name='GroupsUsers')
    Comment = Field(TEXT,verbose_name='备注')
