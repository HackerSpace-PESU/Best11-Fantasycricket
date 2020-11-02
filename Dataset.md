# Dataset

Confused by the dataset , CSV Files too long? Don't Worry I would be too, I will walk you through the dataset here
</br></br>
Lets start with all the folders and all their uses in the project

## ODI

It contains four csv files namely batting_ODI.csv , bowling_ODI.csv , match_ids_ODI.csv , wicketkeeping_ODI.csv </br>
Now lets go into each csv file
		 
### batting_ODI.csv
Contains records of the batsman in different matches.There are 6 columns namely match_id,score,how dismissed, strike rate,4s,6s,batting_position , player_name
The score does not contain the runs scored by the batsmen in that match but it contains the dream 11 score achieved by batting.
The dream 11 score table is presented further down, so dont worry 
</br></br>
## bowling_ODI.csv 
As the name suggests, it contains the records of the bowlers. There are 7 columns namely match_id, score,overs,maidens,wickets,economy,player_name. Again here the score is the dream 11 score which will be covered later
</br></br>
## wicket_keeping_ODI.csv
Again as the name suggests contains wicket keeper records, There are 3 columns, match id ,score , player_name , here again its the dream 11 score which will be covered later
</br></br>
## 6 Matches (Final) - 
This contains data required for testing our model, There are 6 csv files in this and each csv file is named as follows 
</br></br>
**< Name of the match >%< date of match played in yyyy-mm-dd format >.csv**
</br></br>A example would be </br></br>
**Australia vs India%2019-06-09.csv**

There are multiple columns in it but for now only two columns are important the 1st column and the last column
First column contains the player name followed by country 
Last column contains the role at which he plays 
Example : bat, bowl ,all, wk
Each self explanatory

</br></br>
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

## T20

It contains two csv files as of now , batting_T20.csv and match_ids_T20.csv

The description for the csv files is same as the ODI except the scoring table which will be updated soon
</br></br>
I think this covers all the folders

Lets go on to the csv files

## test.csv

This csv file is used for testing of our model</br></br>The columns in these are as follows match_id of the 6 matches, the date , and player 1-22 of the players who have played in this match

## Winning_Points.csv
Contains the winning score for respective matches

That pretty much is our dataset , Hope you like it , if you have any suggestions to improve it do put up a issue or contact the maintainers. It will be much appreciated. 


# Scoring Table - ODI

Now for the scoring table
Lets start with batting

## Batting

Batting is quite simple, The points distribution is as follows

| Type | Points Assigned |
| ---- | --------------- |
| Runs scored | 1 point    |
| 4s   | 1 point     |
| 6s   | 2 points    |
| Half century| 4 points |
| Century | 8 points |
</vr>
Thats it!!

Lets take a example</br></br>
In the match   	
2019 ICC World Cup - 14th ODI - Australia v India - London
</br>
Match -Id : Matches/MatchScorecard_ODI.asp?MatchCode=4316
Lets take Virat Kohli, if we see his score he scored 82 runs with 4 fours and 2 sixes
He also scores a half century which enables him for the half century bonus
Lets calculate his points

Points  =  82 x 1 + 4 x 1  + 6 x 2  + 4 

 Which makes 94, if you look at his csv file under zip2 in the row matching the id , we see the score as 94

## Bowling

| Type | Points Assigned |
| ---- | --------------- |
| Wicket | 25 points    |
| 4 wicket haul   | 4 point     |
| 5 wicket haul   | 8 points    |
| Maiden Over     | 4 Points    |

### Economy Points

| Economy | Points Assigned |
| ---- | --------------- |
| below 2.5 per over | 6 points    |
| Between 2.5 - 3.49 runs per over   | 4 point |
| Between 3.5 - 4.49 runs per over| 2 points   |
| Between 7 - 8 runs per over| -2 points |
| Between 8.1 - 9 runs per over | -4 points |
| Above 9 per over | -6 points |

Note for Economy Points to be considered, the bowler must bowl atleast 5 overs


</vr>
Thats it!!

Lets take an example
In the match   	
2019 ICC World Cup - 14th ODI - Australia v India - London
</br>
Match -Id : Matches/MatchScorecard_ODI.asp?MatchCode=4316
Lets take Mitchell Starc , if we see his bowling stats he took 1 wicket with no maiden overs. Since he bowled 10 overs he is elligible for econmy points. His economy was 7.40
Lets calculate his points

Points  =  1 x 25 + 0 x 4 + (-2) 

 Which makes 23, if you look at his csv file under zip2 in the row matching the id , we see the score as 23

## Wicket Keeping

| Type | Points Assigned |
| ---- | --------------- |
| Catch | 8 points    |
| Stumping   | 12 points     |

</br></br>

Thats the scoring table, simple isn't it!!
