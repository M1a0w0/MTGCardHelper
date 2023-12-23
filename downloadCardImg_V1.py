import requests
import urllib

def downloadImg(cardName):
    savePath = "./downloadImg/"
    scryfall = "https://scryfall.com/search?q="
    scryfall += cardName
    html = requests.get(scryfall).text
    startindex = html.find("Images and Data")
    if startindex == -1:
        file = open(savePath+cardName+".error", 'w')
        file.close()
        return False
    startindex = html.find("href", startindex)
    endindex = html.find("\">", startindex)
    imgURL = html[startindex+6:endindex]
    urllib.request.urlretrieve(imgURL, savePath+cardName+".png")
    print(cardName+" Success!")

def readList(filePath):
    file = open(filePath, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        result = downloadImg(line[2:-1])
        if result==False:
            print(line[2:-1]+" Error!")

readList("./cardList.txt")
