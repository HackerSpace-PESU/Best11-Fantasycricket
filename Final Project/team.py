import pandas as pd
from tqdm import tqdm
import numpy as np
import os
from collections import Counter
from sklearn.linear_model import LinearRegression

def teams(Id,value=5):
    def predict_score(player, position, date): # position: batsman, all-rounder, wk, bowler
    #date format yyyy-mm-dd
    # When assigning position, make sure the file exists in github repo
      f=""
      for i in player:
        if i!='(':
          f+=i
        else:
          break
      f=f.strip()
      for i in tqdm(os.listdir('data/zip')):
        if f in i:
          f=i
          break
      #Data Extraction
      dates = pd.read_csv('data/zip/'+f)
      
      if position == 'all':
        batting_score = pd.read_csv('data/zip2/' +f)
        bowling_score = pd.read_csv('data/bowl/' +f)
        
        scores = batting_score.merge(bowling_score,how='left', left_on='match_id', right_on='Match_id')
        scores = dates.merge(scores,how='left', left_on='matchid', right_on='match_id')
    
        scores = scores.sort_values(by='date',ascending=True).reset_index(drop=True)
        x=scores[scores['date'] == date].index.to_list()[0]
        scores=scores.iloc[0:x,:]
        scores.drop(['Match_id', 'how dismissed','Wicket', 'Economy', 'Maidens', 'Unnamed: 0', 
                     'batting position', '6s', '4s', 'strike rate', 'match_id', 'date'], axis=1, inplace=True)
    
        scores['score'] = scores['score'].apply(lambda x : 0 if x == '-' else x)
        scores['score'] = scores['score'].apply(pd.to_numeric)
        scores['Score'] = scores['Score'].apply(pd.to_numeric)
    
        scores['Total'] = scores['score'] + scores['Score']
        scores.dropna(inplace=True)
        scores = scores[['Total']]    
        #print(scores[:5])
        #print(scores)
        y = list(scores['Total'])
        #print(y)
        #print(scores[:30])
        #return 
      elif position == 'bat':
        batting_score = pd.read_csv('data/zip2/' + f)
        scores = dates.merge(batting_score,how='left', left_on='matchid', right_on='match_id')
    
        scores = scores.sort_values(by='date',ascending=True).reset_index(drop=True)
        x=scores[scores['date'] == date].index.to_list()[0]
        #print(x)
        scores=scores.iloc[0:x,:]
        #print(scores)
        scores.drop(['strike rate', '4s', '6s', 'how dismissed', 'batting position', 'matchid'], axis=1, inplace=True)
    
        scores.dropna(inplace=True)
        scores = scores[scores['score'] != '-']
        #print(scores[:5])
        y = list(scores['score'])
        #print(y);print(scores)
        #print(scores[:30])
        #return
      elif position == 'wk':
        wk_score = pd.read_csv('data/wk/' + f)
        batting_score = pd.read_csv('data/zip2/' + f)
        scores = batting_score.merge(wk_score,how='left', left_on='match_id', right_on='MATCH_ID')
        scores = dates.merge(scores,how='left', left_on='matchid', right_on='match_id')
        scores = scores.sort_values(by='date',ascending=True).reset_index(drop=True)
        x=scores[scores['date'] == date].index.to_list()[0]
        #print(x)
        scores=scores.iloc[0:x,:]
        scores.dropna(inplace=True)
        #print(scores[:5])
        scores.drop(['match_id','MATCH_ID', 'how dismissed','Unnamed: 0', 
                     'batting position', '6s', '4s', 'strike rate', 'date'], axis=1, inplace=True)
    
        scores['score'] = scores['score'].apply(lambda x : 0 if x == '-' else x)
        scores['score'] = scores['score'].apply(pd.to_numeric)
        scores['SCORE'] = scores['SCORE'].apply(pd.to_numeric)
    
        scores['Total'] = scores['score'] + scores['SCORE']
        scores.dropna(inplace=True)
        scores = scores[['Total']]    
        #print(scores[:5])
        #print(scores)
        y = list(scores['Total'])
        #print(y)#y = list(scores['SCORE'])
      else:
        bowling_score = pd.read_csv('data/bowl/' + f)
        scores = dates.merge(bowling_score,how='left', left_on='matchid', right_on='Match_id')
        scores = scores.sort_values(by='date',ascending=True).reset_index(drop=True)
        x=scores[scores['date'] == date].index.to_list()[0]
        #print(x)
        scores=scores.iloc[0:x,:]
        scores.drop(['Economy', 'Wicket', 'Maidens'], axis=1, inplace=True)
        scores.dropna(inplace=True)
        #print(scores[:5])
        y = list(scores['Score'])
        #print(y)
    
        #print(scores[:30])
        #return
    
    
      regr = LinearRegression(fit_intercept=True)
      y_train = np.array(y[len(y)-value:]).reshape(-1,1)
     #rint(y_train)
      X_train = np.array(range(value)).reshape(-1,1)
      try:
        regr.fit(X_train, y_train)           
      except:
        return -1
      pred = regr.predict(np.array(value).reshape(1,-1))
      if pred[0][0] < 0:
        y.append(5)
      else:  
        y.append(pred[0][0])
    
      return y[-1]
    def returnteam(position,files,f,counting):
      team={}
      #print(position,f.split("%")[2][:-4])
      for i in files.name:
        #print(i)
        if i.split('-')[0] not in team:
          team[i.split('-')[0]]=None
        team[i.split('-')[0]]=predict_score(i.split('-')[0],position,f.split("%")[2][:-4])
      wkt=sorted(team.items(), key=lambda x: x[1], reverse=True)
      wkteam={i[0]:i[1] for i in wkt}
      return wkteam
    
    def team(match):
      team1=match.split('vs')[0].strip()
      team2=match.split('vs')[1].strip().split('Semi')[0].strip()
      player={}
      f=""
      for i in tqdm(os.listdir('data/6 Matches (Final)')):
        #print(i)
        if 'England vs Australia' in match:
          if 'Semi' not in match:
            f="EnglandvsAustralia%Matches@MatchScorecard_ODI.asp?MatchCode=4336%2019-06-25.csv"
          else:
            f='EnglandvsAustraliaSemi%Matches@MatchScorecard_ODI.asp?MatchCode=4354%2019-07-11.csv'
        elif match in i.split("%")[0]:
            #print(i)
            f=i
            break
         
      #print(f)
      files=pd.read_csv('data/6 Matches (Final)/'+f)
      count={'wk':4,'bat':6,'ball':6,'all':4}
      for i in list(np.unique(files['role'])):
        filewk=files[files['role']==i]
        if i =='wk':
          wkteam=returnteam(i,filewk,f,count[i])
          #print(wkteam)
        elif i =='bat':
          batteam=returnteam(i,filewk,f,count[i])
          #print(batteam)
        elif i =='all':
          allteam=returnteam(i,filewk,f,count[i])
          #print(allteam)
        elif i =='ball':
          ballteam=returnteam(i,filewk,f,count[i])
          #print(ballteam)
      count1=0
      count2=0
      for i in wkteam:
       maxs=wkteam[i]
       wk=i
       break
      for i in wkteam:
        if wkteam[i]>maxs:
          wk=i
          maxs=wkteam[i]
      if team1 in wk:
        count1+=1
        #print(count1)
      elif team2 in wk:
        count2+=1
        #print(count2)
      if wk not in player:  
        print("a")
        player[wk]=maxs
      for i in allteam:
        maxs=allteam[i]
        wk=i
        break
      for i in allteam:
        if allteam[i]>maxs:
          wk=i
          maxs=allteam[i]
      if team1 in wk:
        count1+=1
        #print(count1)
      elif team2 in wk:
        count2+=1
        #print(count2)
      elif 'Nathan' in wk:
        if team1=='Australia':
          count1+=1
          #print(count1)
        elif team2=='Australia':
          count2+=1
          #print(count2)
      if wk not in player:  
        print("a")
        player[wk]=maxs
      k = Counter(batteam) 
      high = k.most_common(3)
      print(len(high))
      for i in high:
        if i[0] not in player:
          print("a")
        if team1 in i[0]:
          count1+=1
        #print(count1)
        elif team2 in i[0]:
          count2+=1  
        player[i[0]]=i[1]  
      """
      bat={}
      for i in batteam:
        bat[i]=batteam[i]
        if len(bat)>2:
          break
      for i in batteam:
        for j in bat:
          if batteam[i]>=max2[0]:
          max2[0]=batteam[i]
          bat[0]=i
        elif batteam[i]>=max2[1]:
          max2[1]=batteam[i]
          bat[1]=i
        elif batteam[i]>=max2[2]:
          max2[2]=batteam[i]
          bat[2]=i 
      for i in bat:
        if team1 in i:
          count1+=1
          #print(count1)
        elif team2 in i:
          count2+=1
          #print(count2)
        player.append(i)
      max2=[]
      bat=[]
      for i in ballteam:
        max2.append(ballteam[i])
        bat.append(i)
        if len(max2)>2:
          break
      for i in ballteam:
        if ballteam[i]>=max2[0]:
          max2[0]=ballteam[i]
          bat[0]=i
        elif ballteam[i]>=max2[1]:
          max2[1]=ballteam[i]
          bat[1]=i
        elif ballteam[i]>=max2[2]:
          max2[2]=ballteam[i]
          bat[2]=i 
      for i in bat:
        if team1 in i:
          count1+=1
          #print(count1)
        elif team2 in i:
          count2+= 1
          #print(count2)
        player.append(i)
      """
      k = Counter(ballteam) 
      high = k.most_common(3)
      print(len(high))
      for i in high:
        print("a")
        if team1 in i[0]:
          count1+=1
        #print(count1)
        elif team2 in i[0]:
          count2+=1  
        player[i[0]]=i[1]    
      count=0
      rm=[]
      while(count<3):  
        print(count,count1,count2)
        restteam={}
        for i in wkteam:
          if i not in player and i not in rm:
            restteam[i]=wkteam[i]
        for i in allteam:
          if i not in player and i not in rm:
            restteam[i]=allteam[i]
        for i in ballteam:
          if i not in player and i not in rm:
            restteam[i]=ballteam[i]
        for i in batteam:
          if i not in player and i not in rm:
            restteam[i]=batteam[i]
        lists=[float(restteam[i]) for i in restteam]
        #print(lists)
        if value==5:
          print(player)
        maximum=max(lists)
        for i in restteam:
          if restteam[i]>=maximum:
            new=i
            maximum=restteam[i]
        if team1 in new:
          if count1<7:
            player[new]=maximum
            count+=1
            count1+=1
          else:
            rm.append(new)  
        if team2 in new:
          if count2<7:
            player[new]=maximum
            count+=1
            count2+=1
          else:
            rm.append(new)
        elif 'Nathan' in new:
          if team1=='Australia':
            if count1<7:
              player[new]=maximum
              count+=1
              count1+=1
            else:
              rm.append(new)
          elif team2=='Australia':
            if count2<7:
              player[new]=maximum
              count2+=1
              count+=1
            else:
              rm.append(new)
      
      k = Counter(player) 
  
# Finding 3 highest values 
      high = k.most_common(2)
      for i in high:
        max2=i[1]
        captain=i[0]
        break
      for i in high:
        if max2<=i[1]:
          captain=i[0]
          max2=i[1]
        else:
          vcaptain=i[0]
      return player,captain,vcaptain,wkteam,allteam,ballteam,batteam
  
    if Id == 'a':
        a=team('England vs Australia SemiFinal')
    elif Id == 'b':    
        a=team('England vs Australia')
    elif Id == 'c':
        a=team('Bangladesh vs India')
    elif Id == 'd':
        a=team('England vs India')
    elif Id == 'e': 
        a=team('Australia vs India')
    elif Id=='f':
        a=team('India vs New Zealand')
    
    '''print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)'''
    
    return a
def filename(ID):
  if ID=='a':
    return "England vs Australia Semi%Matches@MatchScorecard_ODI.asp?MatchCode=4354%2019-07-11.csv"
  elif ID=='b':
    return "England vs Australia%Matches@MatchScorecard_ODI.asp?MatchCode=4336%2019-06-25.csv"
  elif ID=='c':
    return "Bangladesh vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4345%2019-07-02.csv"
  elif ID=='d':
    return "England vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4342%2019-06-30.csv"
  elif ID=='e':
    return "Australia vs India%Matches@MatchScorecard_ODI.asp?MatchCode=4316%2019-06-09.csv"
  elif ID=='f':
    return "India vs New Zealand%Matches@MatchScorecard_ODI.asp?MatchCode=4353%2019-07-09.csv"
