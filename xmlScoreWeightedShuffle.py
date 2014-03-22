import xml.etree.ElementTree as ET
from sys import argv
from sys import stdin
import random
import time
import decimal
import re
from datetime import date

xmlDoc = "/Users/Rachel/Music/iTunes/iTunes Music Library.xml"
doc = ET.parse(xmlDoc)
rootDict = doc.find('dict')
tracksDict = rootDict.find('dict')
tracks = tracksDict.findall('dict')

songToScore = {}

class Song(object):
    def __init__(self,name,artist,playCount,path,playDate,skipCount,playTime):
        self.name = name
        self.artist = artist
        self.playCount = playCount
        self.path = path
        self.playDate = playDate
        self.skipCount = skipCount
        if playTime != "":
            splits = re.split('T',playTime)
            self.playTime = splits[1]
        if playTime == "":
            self.time = 100.00
        else:
            hourAndMin = re.split(':',self.playTime)
            timeString = hourAndMin[0] + "." + hourAndMin[1]
            self.time = float(timeString)
        if self.playCount == "":
            self.plays = 0
        else:
            self.plays = int(self.playCount)
        if self.playDate == "":
            self.date = 0
        else:
            self.date = (int(self.playDate) - 3029529600) / 864000 #(play date - (seconds from 1/1/1904 to 1/1/2000)) converted to days and then divided by 10
        if self.skipCount == "":
            self.skips = 0
        else:
            self.skips = int(self.skipCount)
    
    def returnScore(self): 
        timeSongs = {}
        currentTime = float(time.strftime("%H.%M"))
        songTime = self.time
        timeScore = 0 
        decimal.getcontext().prec = 6
        curTimes = re.split('\.',str(currentTime))
        songTimes = re.split('\.',str(songTime))
        curTimes[1] = '.' + curTimes[1]
        songTimes[1] = '.' + songTimes[1]
        curTimes = map(decimal.Decimal,curTimes)
        songTimes = map(decimal.Decimal,songTimes)
        songTimes[0] = decimal.Decimal(1.00) * songTimes[0]
        songTimes[1] = decimal.Decimal(1.00) * songTimes[1]
        
        if curTimes[1] < .1:
            if songTimes[0] == timeMinusOne(curTimes[0]) and curTimes[1] + decimal.Decimal(.5) < songTimes[1]:
                timeScore = 30
            elif songTimes[0] == curTimes[0] and abs(songTimes[1] - curTimes[1]) < .1:
                timeScore = 30
        elif curTimes[1] > .5:
            if songTimes[0] == timePlusOne(curTimes[0]) and songTimes[1] + decimal.Decimal(.5) < curTimes[1]:
                timeScore = 30
            elif songTimes[0] == curTimes[0] and abs(songTimes[1] - curTimes[1]) < .1:
                timeScore = 30
        elif curTimes[0] == songTimes[0] and abs(curTimes[1] - songTimes[1]) < .1:
            timeScore = 30
        return self.plays + self.date - self.skips + timeScore


def timePlusOne(time):
    if time >= 23:
        return 0
    else:
        return time + 1

def timeMinusOne(time):
    if time <= 1:
        return 23
    else:
        return time - 1


songs = {}
for track in tracks:
    skipCount = ""
    playCount = ""
    name = ""
    playDate = ""
    playTime = ""
    nameBool = 1
    artistBool = 1
    playCountBool = 1
    pathBool = 1
    playDateBool = 1
    skipCountBool = 1
    playTimeBool = 1
    for child in track:
        if nameBool == 0:
            name = child.text
            nameBool = 1
        elif artistBool == 0:
            artist = child.text
            artistBool = 1
        elif playCountBool == 0:
            playCount = child.text
            if playCount is None:
                playCount = ""
            playCountBool = 1
        elif pathBool == 0:
            path = child.text
            pathBool = 1
        elif playDateBool == 0:
            playDate = child.text
            if playDate is None:
                playDate = ""
            playDateBool = 1
        elif skipCountBool == 0:
            skipCount = child.text
            if skipCount is None:
                skipCount = ""
            skipCountBool = 1
        elif playTimeBool == 0:
            playTime = child.text
            if playTime is None:
                playTime = ""
            playTimeBool = 1
        elif child.text == "Name" and child.tag == "key":
            nameBool = 0
        elif child.text == "Artist" and child.tag == "key":
            artistBool = 0
        elif child.text == "Play Count" and child.tag == "key":
            playCountBool = 0
        elif child.text == "Location" and child.tag == "key":
            pathBool = 0
        elif child.text == "Play Date" and child.tag == "key":
            playDateBool = 0
        elif child.text == "Skip Count" and child.tag == "key":
            skipCountBool = 0
        elif child.text == "Play Date UTC" and child.tag == "key":
            playTimeBool = 0
    songs[name] = Song(name,artist,playCount,path,playDate,skipCount,playTime)


for name in songs:
    songToScore[name] = songs[name].returnScore()

i = 0
weightedSongs = {}
for song in songs:
    count = int(songs[song].returnScore())
    j = 0
    while j < count:
        weightedSongs[i] = songs[song]
        i = i + 1
        j = j + 1

j = 0
randomNumbers = {}
while j < 50:
    randomNumbers[random.randint(0,i)] = 0
    j = j + 1

for num in randomNumbers:
    print(weightedSongs[num].path + ";;;")
