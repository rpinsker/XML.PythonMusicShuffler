#!/bin/bash
# -ss (score weighted shuffle) weighted shuffle by a "score"
#     that takes into account play date, play count, last played time, and skip count
# -ws (weighted shuffle) weighted shuffle by play count
# [song name] plays the requested song (no .mp3 or .m4a required)
# -t (time) weighted shuffle by play count for songs last played within ten minutes
#    (10 minutes ahead and 10 minutes behind) of a given time

time=-2
if [[ $1 == "-ss" ]] 
then
    var=$(python xmlScoreWeightedShuffle.py)
    #echo $var
elif [[ $1 == "-t" ]] 
then
    if [[ $time == "-2" ]]
    then
	echo "Enter a time in the form hour.min (type -1 to use current time)"
	read time
    fi
    if [[ $time == "-1" ]]
    then
	var=$(python xmlTimeShuffle.py)
    else 
	var=$(python xmlTimeShuffle.py $time)
    fi
else
    var=$(python xmlMusic.py "$1")
fi

song=""
while [[ $var != "" ]]
do
    song=${var%%";;;"*";;;"}
    song=${song//%20/ }
    song=${song#*"file://localhost"}
    var=${var#*";;;"}
    if [[ $var != ""  ]]
    then
	echo "Playing: " $song
	afplay "${song}"
    fi
done
song=${song%";;;"}
echo "Playing: " $song
afplay "${song}"
#exit(0)