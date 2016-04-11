#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import datetime
import time
import getpass
import sys
import ipa_export

reload(sys)
sys.setdefaultencoding('utf-8')

#项目中文名
PROJECT_C_NAME = "代泊司机端"

#请修改为需要使用的证书全称
CODE_SIGN = "iPhone Distribution: xxxxxx Technology Co. Ltd. (xxxxx)"

#PROFILE文件的值， 点击左上角“Xcode” -> "Preferences" -> "Accounts" -> "要使用的appleID" -> "View Details" -> 
# "右键点击需要使用的PROFILE" -> "show in Finder" -> 文件名就是这个值
PROFILE = "xxxxxxx"   #ad_hoc
PROFILE_NAME = "xxxxxx"

PROJECT_NAME = "parker"
SCHEME_NAME = "parker"
#导出路径
EXPORT_PATH_PREFIX = "/Users/%s/Desktop/Release/Ad_hoc/%s"%(getpass.getuser(),PROJECT_NAME)
#二维码导出路径
QRCODE_NAME = "/Users/%s/Desktop/Release/Ad_hoc/%s/download_url.png"%(getpass.getuser(),PROJECT_NAME)

#蒲公英上传时需要的参数配置
PGYER_UKEY = "xxxxxx"
PGYER_API_KEY = "xxxxxx"

#发送邮件相关配置
TO_LIST = ["xxxxx"]
FROM_MAIL = "xxxxx" #你的邮箱
FROM_PASS = "pwd"   #你的密码
MAIL_HOST = "xxxxx"

def export(buildcmd, ipaName) :
	ipa_export.export_adhoc(PROJECT_NAME, PROJECT_C_NAME, CODE_SIGN, PROFILE, buildcmd, EXPORT_PATH_PREFIX, ipaName, QRCODE_NAME, PGYER_UKEY, PGYER_API_KEY, FROM_MAIL, FROM_PASS, TO_LIST, MAIL_HOST)
	return

#项目类型
try:
	projectType = sys.argv[1]
	now = datetime.datetime.now()
	ipaName = "%s_%d-%d-%d-%d-%d-%d"%(PROJECT_NAME, now.year, now.month, now.day, now.hour, now.minute, now.second)
	if projectType == 'p' : #project
		buildcmd = '''xcodebuild clean;xcodebuild archive -project $PWD/*.xcodeproj -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
		export(buildcmd, ipaName)
	elif projectType == 'w' : #workspace
		buildcmd = '''xcodebuild clean;xcodebuild archive -workspace $PWD/*.xcworkspace -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
		export(buildcmd, ipaName)
	else :
		print "请输入项目类型， project请运行'xxxx.py p', workspace请运行'xxxx.py w'"
except Exception, e :
	print "请输入项目类型， project请运行'xxxx.py p', workspace请运行'xxxx.py w'"


