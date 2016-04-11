#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import datetime
import time
import urllib
import commands
import getpass
import smtplib
from email.mime.text import MIMEText
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def setProjectConfig(filePath, codesign, profile) :
	fileObj = open(filePath, "r")

	firstCodeSign = 0
	firstProfile = 0
	iphoneosCount = 0

	try:
		all_text = fileObj.readlines()
		i=-1
		for text in all_text:
			i+=1
			if 'CODE_SIGN_IDENTITY' in text :
				if '[sdk=iphoneos*]' in text :
					if iphoneosCount<3 :
						iphoneosCount += 1
					else :
						all_text.remove(text)
						all_text.insert(i, '''				"CODE_SIGN_IDENTITY[sdk=iphoneos*]" = "%s";\n'''%codesign)
				else :
					if firstCodeSign==0 :
						firstCodeSign=1
					else:
						all_text.remove(text)
						all_text.insert(i, '''				CODE_SIGN_IDENTITY = "%s";\n'''%codesign)
    
    		if 'PROVISIONING_PROFILE' in text :
				if firstProfile==0 :
					firstProfile = 1
				else :
					all_text.remove(text)
					all_text.insert(i, '''				PROVISIONING_PROFILE = "%s";\n'''%profile)
	finally:
		fileObj.close()

	fileObj = open(filePath, "w")
	try:
		for text in all_text :
			fileObj.write(text)
	finally:
		fileObj.close()
	return

#fromMail : FROM_MAIL  发件邮箱
#fromPass : FROM_PASS  发件邮箱密码
#toList : TO_LIST      收件邮箱数组
#projectCName : PROJECT_C_NAME   项目中文名称
#mailHost : MAIL_HOST  邮箱域名
def sendMail(fromMail, fromPass, toList, projectCName, appQRCodeURL, mailHost):
	me = "%s<%s>"%(fromMail, fromMail)
	to = ";".join(toList)
	content = """"%s"已上传，请扫描二维码下载，并进行测试。请及时反馈测试中遇到的问题，以便我们能及时更改。
	<br/>
	<img src="%s"></img>
	"""%(projectCName, appQRCodeURL)
	msg = MIMEText(content, _subtype='html', _charset='utf-8')
	msg['Subject'] = '''"%s"已上传，请扫描二维码下载'''%projectCName
	msg['From'] = me
	msg['To'] = to

	try:
		smtpObj = smtplib.SMTP()
		smtpObj.connect(mailHost)
		smtpObj.login(fromMail, fromPass)
		smtpObj.sendmail(fromMail, toList, msg.as_string())  
		smtpObj.close()       
		print "Successfully sent email"
	except Exception, e:
		print str(e)
		print "Error: unable to send email"

#projectName : PROJECT_NAME  项目名称，英文名
#projectCName : PROJECT_C_NAME 项目名称， 中文名
#codeSign : CODE_SIGN   签名证书名称
#profile : PROFILE   描述文件的值
#buildcmd : 导出命令
#exportPathPrefix ： EXPORT_PATH_PREFIX   导出目录
#ipaName : 导出的ipa包的名称
#pgyUKey : PGYER_UKEY   蒲公英UKey
#pgyAPIKey : PGYER_API_KEY  蒲公英apiKey
#qrCodeName : QRCODE_NAME  二维码文件名(全路径)
#fromMail : FROM_MAIL  发件邮箱
#fromPass : FROM_PASS  发件邮箱密码
#toList :   TO_LIST    收件邮箱数组
#mailHost : MAIL_HOST  邮箱域名
def export_adhoc(projectName, projectCName, codeSign, profile, buildcmd, exportPathPrefix, ipaName, qrCodeName, pgyUKey, pgyAPIKey, fromMail, fromPass, toList, mailHost) :
	#配置编译环境
	configFilePath = "%s.xcodeproj/project.pbxproj"%projectName
	setProjectConfig(configFilePath, codeSign, profile)
    
    #开始编译、导出
    # buildcmd = '''xcodebuild clean;xcodebuild archive -workspace $PWD/*.xcworkspace -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
	print buildcmd
	os.system(buildcmd)

    #上传蒲公英
	ipaPath = "%s/%s.ipa"%(exportPathPrefix, ipaName)

	print ipaPath

	cmd = '''curl -F "file=@%s" -F "uKey=%s" -F "_api_key=%s" http://www.pgyer.com/apiv1/app/upload'''%(ipaPath, pgyUKey, pgyAPIKey)
	print cmd
	output = commands.getoutput(cmd);
    # output = os.popen(cmd)

	start = output.find('{')
	if start >= 0 :
		result_str = output[start:]
		result = json.loads(result_str)
		data_str = result["data"]
		data_str = json.dumps(data_str)
		data = json.loads(data_str)
		appQRCodeURL =  data["appQRCodeURL"]
		urllib.urlretrieve(appQRCodeURL, qrCodeName)

        #发送通知邮件
        #fromMail, fromPass, toList, projectCName, appQRCodeURL, mailHost
		sendMail(fromMail, fromPass, toList, projectCName, appQRCodeURL, mailHost)
	return


def export_appstore(projectName, codeSign, profile, buildcmd, exportPathPrefix) :
	#配置编译环境
	configFilePath = "%s.xcodeproj/project.pbxproj"%projectName
	setProjectConfig(configFilePath, codeSign, profile)
    
    #开始编译、导出
    # buildcmd = '''xcodebuild clean;xcodebuild archive -workspace $PWD/*.xcworkspace -scheme %s -archivePath %s/%s.xcarchive;xcodebuild -exportArchive -archivePath %s/%s.xcarchive -exportPath %s/%s -exportFormat ipa -exportProvisioningProfile %s'''%(SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,SCHEME_NAME,EXPORT_PATH_PREFIX,ipaName,PROFILE_NAME)
	print buildcmd
	os.system(buildcmd)
	return



