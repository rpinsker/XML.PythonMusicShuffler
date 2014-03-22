#!/bin/bash
# -ss (score weighted shuffle) weighted shuffle by a "score"
#     that takes into account play date, play count, time of last play, and skip count
# -ws (weighted shuffle) weighted shuffle by play count
# [song name] plays the requested song (no .mp3 or .m4a required)
# -t (time) weighted shuffle by play count for songs last played within an hour
#    (1 hour ahead and 1 hour behind) of a given time

time=-2
done=1
while [ $done -eq 1 ]
do
for arg in "$@"
do
    if [[ $arg == "-ss" ]] 
    then
	var=$(python xmlScoreWeightedShuffle.py)
    elif [[ $arg == "-t" ]] 
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
	var=$(python xmlMusic.py "$arg")
    fi
    var=${var//%20/ }
    var=${var#*"file://localhost"}
    echo $var
    afplay "${var}"
done
done
exit(0)





