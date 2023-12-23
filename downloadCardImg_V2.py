import datetime
import requests
import urllib
import json
import time
import os

# type(result_dict):
# 	{
# 		"resultType": (bool)(NOT NULL),		结果状态 字段不可缺失 True=成功 False=失败
# 		"code": (str)(NOT NULL),			结果代码 字段不可缺失
# 		"exception": (str),					异常内容 字段可缺失: 当不存在exception时
# 		"dataDict": (dict)/(card_dict),		数据字典 字段可缺失: 当无数据时
# 	}

# type(card_dict):
# 	{
# 		"cardType": (str)(NOT NULL),			卡片类型 字段不可缺失 str=(enum)["Multicard", "Singlecard", "Token"]
# 		"cardId": (array[UUID])(NOT NULL),		卡片id数组 字段不可缺失
# 		"cardLang": (str),						卡片语言 字段可缺失: 当cardType==Token时
# 		"cardName": (str),						卡片名称 字段可缺失: 当cardType==Token时
# 		"face_uriList": (array[str]),			卡图uri数组 字段可缺失: 当cardType==Token时
# 		"has_token": (bool),					卡片是否有衍生物 字段可缺失: 当cardType==Token时 False=无衍生物 True=有衍生物
# 		"token_idList": (array[UUID]),			卡片衍生物id 字段可缺失: 当cardType==Token/has_token==False时
# 		"tokenParent": (str)					衍生物父名 字段可缺失: 当cardType!=Token时
# 	}

# https://scryfall.com/docs/api
cardLang = ["en", "zhs"] # 搜索指定语言的卡图
scyfallApi = "https://api.scryfall.com/cards/" # scyfall的api地址
savePath = "./downloadImg/" # 卡图保存路径
cardList = "./cardList.txt" # 牌表txt路径
cardIndependentFolder = False # 是否为每个多面卡单独创建文件夹 True=是 False=否
tokenIndependentFolder = False # 是否为每组衍生物单独创建文件夹 True=是 False=否
searchMethod = 2 # 搜索方式 0=单独搜索卡图 1=单独搜索衍生物 2=搜索卡图及其衍生物

# 为信息加上[Success/Error][%time]前缀并打印 result=True=Success result=False=Error addtion=附加前缀 info=要打印的信息
def printAddprefix(result, addtion, info):
	current_time = datetime.datetime.now().time()
	formatted_time = current_time.strftime("[%H:%M:%S]")
	if(result):
		result = "[Success]"
	else:
		result = "[Error]"
	print(result, formatted_time , addtion, info)

# 字节转字典 data_bytes=字节信息 return=字典
def bytes2dict(data_bytes):
	data_str = data_bytes.decode("utf-8")
	data_dict = json.loads(data_str)
	return data_dict

# 尝试GET uri=尝试发送GET请求的地址 return=type(result_dict)
def tryGET(uri):
	try:
		time.sleep(1)
		getData = requests.get(uri)
	except BaseException as e:
		resultType = False
		code = "requests.get error: "
		result = {
			"resultType": resultType,
			"code": code,
			"exception": str(e)
		}
		return result
	resultType = True
	code = "requests.get Success!"
	dataDict = bytes2dict(getData.content)
	result = {
		"resultType": resultType,
		"code": code,
		"dataDict": dataDict
	}
	return result

# 根据卡名及语言搜索卡片 cardName=卡名 lang=语言 return=type(result_dict)
def searchCard(cardName, lang):
	searchUri = scyfallApi + "search?q=lang%3A" + lang + "+" + cardName
	tryGETresult = tryGET(searchUri)
	if(tryGETresult["resultType"]):
		dataDict = tryGETresult["dataDict"]
	else:
		tryGETresult["code"] += cardName
		return tryGETresult
	if(dataDict["object"]=="error"):
		resultType = False
		code = dataDict["code"]
		result = {
			"resultType": resultType,
			"code": code
		}
		return result
	elif(dataDict["object"]=="list"):
		for cardObject in dataDict["data"]:
			pos = cardObject["name"].find(" // ")
			if(pos==-1):
				pos = len(cardObject["name"])
			if(cardObject["name"][0:pos]==cardName):
				resultType = True
				code = cardName + " Find!"
				cardId = [cardObject["id"]]
				cardLang = cardObject["lang"]
				has_token = False
				token_idList = []
				if("card_faces" in cardObject.keys()):
					cardType = "Multicard"
					face_uriList = []
					for cardFace in cardObject["card_faces"]:
						face_uriList.append(cardFace["image_uris"]["png"])
				else:
					cardType = "Singlecard"
					face_uriList = [cardObject["image_uris"]["png"]]
				if("all_parts" in cardObject.keys()):
					for partObject in cardObject["all_parts"]:
						if(partObject["component"]=="token"):
							has_token = True
							token_idList.append(partObject["id"])
				cardDict = {
					"cardType": cardType,
					"cardId": cardId,
					"cardLang": cardLang,
					"cardName": cardName,
					"face_uriList": face_uriList,
					"has_token": has_token,
					"token_idList": token_idList
				}
				result = {
					"resultType": resultType,
					"code": code,
					"dataDict": cardDict
				}
				return result
	resultType = False
	code = "other_error: " + cardName
	result = {
		"resultType": resultType,
		"code": code
	}
	return result

# 根据字典下载卡图 cardDict=卡片字典 return=type(result_dict)
def downloadImg(cardDict):
	if(cardDict["cardType"]=="Token"):
		tokenFolder = savePath + "tokens/"
		if not(os.path.exists(tokenFolder)):
			os.mkdir(tokenFolder)
		if(tokenIndependentFolder):
			tokenFolder += cardDict["tokenParent"] + "/"
		if not(os.path.exists(tokenFolder)):
			os.mkdir(tokenFolder)
		count = 0
		for face_uri in cardDict["face_uriList"]:
			cardSave = tokenFolder + cardDict["tokenParent"] + str(count) + ".png"
			try:
				urllib.request.urlretrieve(face_uri, cardSave)
			except BaseException as e:
				resultType = False
				code = "urllib.request.urlretrieve error: " + cardDict["tokenParent"]
				result = {
					"resultType": resultType,
					"code": code,
					"exception": str(e)
				}
				return result
			count += 1
		resultType = True
		code = cardDict["tokenParent"] + " Success!"
		result = {
			"resultType": resultType,
			"code": code
		}
		return result
	else:
		langFolder = savePath + cardDict["cardLang"] + "/"
		if not(os.path.exists(langFolder)):
			os.mkdir(langFolder)
		if(cardDict["cardType"]=="Multicard"):
			if not(os.path.exists(langFolder + "Multicard/")):
				os.mkdir(langFolder + "Multicard/")
			if(cardIndependentFolder):
				cardPath = langFolder + "Multicard/" + cardDict["cardName"] + "/"
			else:
				cardPath = langFolder + "Multicard/"
			if not(os.path.exists(cardPath)):
				os.mkdir(cardPath)
			count = 0
			for face_uri in cardDict["face_uriList"]:
				cardSave = cardPath + cardDict["cardName"] + str(count) + ".png"
				try:
					urllib.request.urlretrieve(face_uri, cardSave)
				except BaseException as e:
					resultType = False
					code = "urllib.request.urlretrieve error: " + cardDict["cardName"]
					result = {
						"resultType": resultType,
						"code": code,
						"exception": str(e)
					}
					return result
				count += 1
		else:
			cardPath = langFolder + "Singlecard/"
			if not(os.path.exists(cardPath)):
				os.mkdir(cardPath)
			for face_uri in cardDict["face_uriList"]:
				cardSave = cardPath + cardDict["cardName"] + ".png"
				try:
					urllib.request.urlretrieve(face_uri, cardSave)
				except BaseException as e:
					resultType = False
					code = "urllib.request.urlretrieve error: " + cardDict["cardName"]
					result = {
						"resultType": resultType,
						"code": code,
						"exception": str(e)
					}
					return result
		resultType = True
		code = cardDict["cardName"] + " Success!"
		result = {
			"resultType": resultType,
			"code": code
		}
		return result

# 解析衍生物 cardDict=主卡片字典 return=type(result_dict)
def analysisToken(cardDict):
	if(cardDict["has_token"]):
		cardType = "Token"
		cardId = cardDict["token_idList"]
		tokenParent = cardDict["cardName"]
		face_uriList = []
		for tokenId in cardDict["token_idList"]:
			cardUri = scyfallApi + tokenId
			tryGETresult = tryGET(cardUri)
			if(tryGETresult["resultType"]):
				dataDict = tryGETresult["dataDict"]
			else:
				tryGETresult["code"] += tokenId
				return tryGETresult
			if(dataDict["object"]=="error"):
				resultType = False
				code = dataDict["code"]
				result = {
					"resultType": resultType,
					"code": code
				}
				return result
			elif(dataDict["object"]=="card"):
				face_uriList.append(dataDict["image_uris"]["png"])
		dataDict = {
			"cardType": cardType,
			"cardId": cardId,
			"tokenParent": tokenParent,
			"face_uriList": face_uriList
		}
		resultType = True
		code = "Card " + cardDict["cardName"] + "_" + cardDict["cardLang"] + "token Find!"
		result = {
			"resultType": resultType,
			"code": code,
			"dataDict": dataDict
		}
		return result
	resultType = False
	code = "Card " + cardDict["cardName"] + "_" + cardDict["cardLang"] + " donot have token!"
	result = {
		"resultType": resultType,
		"code": code
	}
	return result

# 解析卡片 cardName=卡片名称
def analysisCard(cardName):
	for lang in cardLang:
		result = searchCard(cardName, lang)
		if(result["resultType"]):
			if(searchMethod==0):
				result = downloadImg(result["dataDict"])
				printAddprefix(result["resultType"], "[Card]", result["code"])
			elif(searchMethod==1):
				result = analysisToken(result["dataDict"])
				if(result["resultType"]):
					result = downloadImg(result["dataDict"])
					printAddprefix(result["resultType"], "[Token]", result["code"])
				else:
					printAddprefix(result["resultType"], "[Token]", result["code"])
			elif(searchMethod==2):
				downloadresult = downloadImg(result["dataDict"])
				printAddprefix(downloadresult["resultType"], "[Card]", downloadresult["code"])
				result = analysisToken(result["dataDict"])
				if(result["resultType"]):
					result = downloadImg(result["dataDict"])
					printAddprefix(result["resultType"], "[Token]", result["code"])
				else:
					printAddprefix(result["resultType"], "[Token]", result["code"])
		elif(result["code"]!="not_found"):
			printAddprefix(result["resultType"], "[Search]", result["code"])
			break
	if(result["code"]=="not_found"):
		printAddprefix(result["resultType"], "[Search]", result["code"]+": "+cardName)

# 读取txt牌表 filePath=牌表txt路径
def readList(filePath):
	with open(filePath, 'r') as file:
		lines = file.readlines()
	for line in lines:
		analysisCard(line[2:-1])

def main():
	if not(os.path.exists(savePath)):
		os.makedirs(savePath)
	readList(cardList)
main()
