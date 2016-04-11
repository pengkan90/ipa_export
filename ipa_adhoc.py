#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import datetime
import time
import getpass
import sys
import ipa_export

#xcodebuild clean
#xcodebuild archive -project $PWD/*.xcodeproj -scheme Parking_Where -archivePath /Users/apple/Desktop/Release/Ad_hoc/Parking_Where/Parking_Where.xcarchive
#xcodebuild -exportArchive -archivePath /Users/apple/Desktop/Release/Ad_hoc/Parking_Where/Parking_Where.xcarchive -exportPath /Users/apple/Desktop/Release/Ad_hoc/Parking_Where -exportFormat ipa -exportProvisioningProfile xinFlyWhere

reload(sys)
sys.setdefaultencoding('utf-8')

#项目中文名
PROJECT_C_NAME = "代泊司机端"

#请修改为需要使用的证书全称
CODE_SIGN = "iPhone Distribution: Wuhan Mobilefly Technology Co. Ltd. (HTPX8WMR4A)"

#PROFILE文件的值， 点击左上角“Xcode” -> "Preferences" -> "Accounts" -> "要使用的appleID" -> "View Details" -> 
# "右键点击需要使用的PROFILE" -> "show in Finder" -> 文件名就是这个值
PROFILE = "9382aa73-a9db-4996-a1d5-a066266526b7"   #ad_hoc
PROFILE_NAME = "ParkerDriver_adHoc"
#PROFILE = "10c10fab-6893-45c8-9aec-9d9a5dcaee11"    #appStore
#PROFILE_NAME = "ParkerDriver_appStore"

PROJECT_NAME = "parker"
SCHEME_NAME = "parker"
#导出路径
EXPORT_PATH_PREFIX = "/Users/%s/Desktop/Release/Ad_hoc/%s"%(getpass.getuser(),PROJECT_NAME)
#二维码导出路径
QRCODE_NAME = "/Users/%s/Desktop/Release/Ad_hoc/%s/download_url.png"%(getpass.getuser(),PROJECT_NAME)

#蒲公英上传时需要的参数配置
PGYER_UKEY = "04fa2184bed5c4a0e1fea6e205e20aab"
PGYER_API_KEY = "815ab126c9e527e7fb56b061c50394e7"

#发送邮件相关配置
TO_LIST = ["fsxin@tnar.cn"]
FROM_MAIL = "kpeng@tnar.cn" #你的邮箱
FROM_PASS = "pwd"   #你的密码
MAIL_HOST = "smtp.tnar.cn"

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


