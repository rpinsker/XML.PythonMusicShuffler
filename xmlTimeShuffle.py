import xml.etree.ElementTree as ET
from sys import argv
from sys import stdin
import random
import re
from datetime import date
import time
import decimal

# no arguments: play songs last played within 10 min (10 min ahead and 10 min behind) of current time
# hour.min (floating point number of a given time--eg 10:35am is 10.35 and 4:20pm is 16.2): play songs last played
#          within 10 min(10 min ahead and 10 min behind) of given time 

#NOTE: some of the commented out code is for the program to work to play songs last played
# within an hour (ahead and behind) of the current/provided time

xmlDoc = "/Users/Rachel/Music/iTunes/iTunes Music Library.xml"
doc = ET.parse(xmlDoc)
rootDict = doc.find('dict')
tracksDict = rootDict.find('dict')
tracks = tracksDict.findall('dict')

songToScore = {}

class Song(object):
    def __init__(self,name,artist,playCount,path,playTime):
        self.name = name
        self.artist = artist
        self.playCount = playCount
        self.path = path
        splits = re.split('T',playTime)
        self.playTime = splits[1]
        if self.playCount == "":
            self.plays = 0
        else:
            self.plays = int(self.playCount)
        if self.playTime == "":
            self.time = -1
        else:
            hourAndMin = re.split(':',self.playTime)
            timeString = hourAndMin[0] + "." + hourAndMin[1]
            self.time = float(timeString)

songs = {}
for track in tracks:
    skipCount = ""
    playCount = ""
    name = ""
    playDate = ""
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
        elif child.text == "Play Date UTC" and child.tag == "key":
            playTimeBool = 0
    songs[name] = Song(name,artist,playCount,path,playTime)

timeSongs = {}

currentTime = float(time.strftime("%H.%M"))
if len(argv) > 1:
    currentTime = float(argv[1])

def timePlusOne(time):
    if time >= 23:
    # CODE FOR SONGS WITHIN 1 HOUR
    #    t = str(time)
    #    times = re.split('\.',t)
    #    return float('0.' + times[1])
        return 0
    else:
        return time + 1

def timeMinusOne(time):
    if time <= 1:
    # CODE FOR SONGS WITHIN 1 HOUR
    #    t = str(time)
    #    times = re.split('\.',t)
    #    return float('23.' + times[1])
        return 23
    else:
        return time - 1

#print(currentTime)
for song in songs:
    #CODE TO PLAY SONGS WITHIN 1 HOUR OF LAST PLAYED TIME
    #if currentTime >= 23:
    #    if abs(songs[song].time - currentTime) < 1 or timePlusOne(currentTime) > songs[song].time:
    #        timeSongs[song] = songs[song]
            #print(str(timeSongs[song].time) + " " + str(currentTime))
    #elif currentTime <= 1:
    #    if abs(songs[song].time - currentTime) < 1 or timeMinusOne(currentTime) < songs[song].time:
    #        timeSongs[song] = songs[song]
            #print(str(timeSongs[song].time) + " " + str(currentTime))
    #elif abs(songs[song].time - currentTime) < 1:
        #timeSongs[song] = songs[song]
        #print(str(timeSongs[song].time) + " " + str(currentTime))
    
    # CODE TO PLAY SONGS WITHIN 10 MINUTES OF LAST PLAYED TIME
    decimal.getcontext().prec = 6
    curTimes = re.split('\.',str(currentTime))
    songTimes = re.split('\.',str(songs[song].time))
    curTimes[1] = '.' + curTimes[1]
    songTimes[1] = '.' + songTimes[1]
    curTimes = map(decimal.Decimal,curTimes)
    songTimes = map(decimal.Decimal,songTimes)
    songTimes[0] = decimal.Decimal(1.00) * songTimes[0]
    songTimes[1] = decimal.Decimal(1.00) * songTimes[1]
    
    if curTimes[1] < .1:
        if songTimes[0] == timeMinusOne(curTimes[0]) and curTimes[1] + decimal.Decimal(.5) < songTimes[1]:
            timeSongs[song] = songs[song]
        elif songTimes[0] == curTimes[0] and abs(songTimes[1] - curTimes[1]) < .1:
            timeSongs[song] = songs[song]
    elif curTimes[1] > .5:
        if songTimes[0] == timePlusOne(curTimes[0]) and songTimes[1] + decimal.Decimal(.5) < curTimes[1]:
            timeSongs[song] = songs[song]
        elif songTimes[0] == curTimes[0] and abs(songTimes[1] - curTimes[1]) < .1:
            timeSongs[song] = songs[song]
    elif curTimes[0] == songTimes[0] and abs(curTimes[1] - songTimes[1]) < .1:
        timeSongs[song] = songs[song]
            
        
        
i = 0
weightedSongs = {}
for song in timeSongs:
    print(timeSongs[song].time)
    count = int(timeSongs[song].plays)
    j = 0
    while j < count:
        weightedSongs[i] = timeSongs[song]
        i = i + 1
        j = j + 1

if i > 1:
    k = 0
    randomNumbers = {}
    while k < 50:
        randomNumbers[random.randint(0,i-1)] = 0
        k = k + 1
    if len(timeSongs) != 0:
        for num in randomNumbers:
            print(weightedSongs[num].path + ";;;")
else:
    print("NOTHING PLAYED WITHIN 10 MINUTES OF THAT TIME. TRY AGAIN;;;")

                        
