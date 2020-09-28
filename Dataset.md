# Dataset

Confused by the dataset , soo many folders, so many files, Don't Worry I would be too, I will walk you through the dataset here
</br></br>
Lets start with all the folders and all their uses in the project

## zip

It contains the csv files represented by the player name and corresponding country.</br>Each csv file contains two columns having the match ids and the corresponding date at which the match was played
		 Now you might be confused as to what the match ids indicate and how do we get to know what match is being spoken about here </br></br>Lets take a example
		 </br><br>
		 ```
		 Matches/MatchScorecard_ODI.asp?MatchCode=4114 
		 ```
		</br></br>
		 Place the above match id in the following link http://www.howstat.com/cricket/Statistics/ like this
		</br></br>
		http://www.howstat.com/cricket/Statistics/Matches/MatchScorecard_ODI.asp?MatchCode=4114
		</br>	</br>
		Clicking on this link should take you to the respective scorecard of the match
		Similary its the same for all the matches, you can also find the list of each match name with their ids in the [allmatches.csv](https://github.com/lucasace/Best11-Fantasycricket/blob/master/allmatches.csv)
</br></br>

## zip2 
Contains records of the batsman in different matches.There are 5 columns namely match_id,score,how dismissed, strike rate,4s,6s,batting_position
The score does not contain the runs scored by the batsmen in that match but it contains the dream 11 score achieved by batting.
The dream 11 score table is presented further down, so dont worry 

</br></br>

## bowl 
As the name suggests, it contains the records of the bowlers. There are 6 columns namely match_id, score,overs,maidens,wickets,economy. Again here the score is the dream 11 score which will be covered later

</br></br>
## wk 
Again as the name suggests contains wicket keeper records, There are 2 columns, match id and score , here again its the dream 11 score which will be covered later
</br></br>

##6 Matches (Final) - 
This contains data required for testing our model, There are 6 csv files in this and each csv file is named as follows 
</br></br>
**<Name of the match>%Matches@MatchScorecard_ODI.asp?MatchCode=< match code>%< date of match played in yyyy-mm-dd format >.csv**
A example would be </br></br>
**Australia vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4316%2019-06-09.csv**

There are multiple columns in it but for now only two columns are important the 1st column and the last column
First column contains the player name followed by country 
Last column contains the role at which he plays 
Example : bat, bowl ,all, wk
Each self explanatoryhttps://doi.org/10.1007/978-1-0716-0826-5_3

</br></br></br>
I think this covers all the folders

Lets go on to the csv files

## test.csv

This csv file is used for testing of our model</br></br>The columns in these are as follows match_id of the 6 matches, the date , and player 1-22 of the players who have played in this match

## Winning_Points.csv
Contains the winning score for respective matches

That pretty much is our dataset , Hope you like it , if you have any suggestions to improve it do put up a issue or contact the maintainers. It will be much appreciated. As for the scoring table click on this link to understand
