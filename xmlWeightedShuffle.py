import xml.etree.ElementTree as ET
from sys import argv
from sys import stdin
import random


doc = ET.parse(argv[1])
rootDict = doc.find('dict')
tracksDict = rootDict.find('dict')
tracks = tracksDict.findall('dict')

class Song(object):
    def __init__(self,name,artist,playCount,path):
        self.name = name
        self.artist = artist
        if playCount == "":
            self.playCount = 0
        else:
            self.playCount = playCount
        self.path = path

songs = {}
for track in tracks:
    name = ""
    playCount = ""
    nameBool = 1
    artistBool = 1
    playCountBool = 1
    pathBool = 1
    for child in track:
        if nameBool == 0:
            name = child.text
            nameBool = 1
        elif artistBool == 0:
            artist = child.text
            artistBool = 1
        elif playCountBool == 0:
            playCount = child.text
            playCountBool = 1
        elif pathBool == 0:
            path = child.text
            pathBool = 1
        elif child.text == "Name" and child.tag == "key":
            nameBool = 0
        elif child.text == "Artist" and child.tag == "key":
            artistBool = 0
        elif child.text == "Play Count" and child.tag == "key":
            playCountBool = 0
        elif child.text == "Location" and child.tag == "key":
            pathBool = 0
    songs[name] = Song(name,artist,playCount,path)

i = 0
weightedSongs = {}
for song in songs:
    count = int(songs[song].playCount)
    if count != 0:
        j = 0
        while j < count:
            weightedSongs[i] = songs[song]
            i = i + 1
            j = j + 1

rand = random.randint(0,i-1)
print(weightedSongs[rand].path)
