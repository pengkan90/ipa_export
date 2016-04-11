#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import datetime
import time
import getpass
import json
import sys
import ipa_export

#请修改为需要使用的证书全称
CODE_SIGN = "iPhone Distribution: Wuhan Mobilefly Technology Co. Ltd. (HTPX8WMR4A)"

#PROFILE文件的值， 点击左上角“Xcode” -> "Preferences" -> "Accounts" -> "要使用的appleID" -> "View Details" -> 
# "右键点击需要使用的PROFILE" -> "show in Finder" -> 文件名就是这个值
PROFILE = "10c10fab-6893-45c8-9aec-9d9a5dcaee11"    #appStore
PROFILE_NAME = "ParkerDriver_appStore"

PROJECT_NAME = "parker"
SCHEME_NAME = "parker"
#导出路径
EXPORT_PATH_PREFIX = "/Users/%s/Desktop/Release/app_store/%s"%(getpass.getuser(),PROJECT_NAME)

def export(buildcmd) :
	ipa_export.export_appstore(PROJECT_NAME, CODE_SIGN, PROFILE, buildcmd, EXPORT_PATH_PREFIX)
	return

#项目类型
try:
	projectType = sys.argv[1]
	now = datetime.datetime.now()
	ipaName = "%s_%d-%d-%d-%d-%d-%d"%(PROJECT_NAME, now.year, now.month, now.day, now.hour, now.minute, now.second)

	if projectType == 'p' : #project
		buildcmd = '''xcodebuild clean;xcodebuild archive -project $PWD/*.xcodeproj -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
		export(buildcmd)
	elif projectType == 'w' : #workspace
		buildcmd = '''xcodebuild clean;xcodebuild archive -workspace $PWD/*.xcworkspace -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
		export(buildcmd)
	else :
		print "请输入项目类型， project请运行'xxxx.py p', workspace请运行'xxxx.py w'"
except Exception, e :
	print "请输入项目类型， project请运行'xxxx.py p', workspace请运行'xxxx.py w'"






