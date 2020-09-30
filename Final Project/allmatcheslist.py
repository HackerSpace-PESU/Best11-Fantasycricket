import pandas as pd
from tqdm import tqdm
import os
allm=pd.read_csv("cricket/all.csv")
allm=allm[allm['Date']>='2019-01-01']
print(allm['Date'].head())
match={}
for i in tqdm(os.listdir('cricket/data/zip')):
	if i!='players.csv':
		x=pd.read_csv('cricket/data/zip/'+i)
		for j in allm['Match-ID']:
			if j not in match:
				match[j]=[]
			x1=x[x['matchid']==j]
			if x1.empty==False:
				match[j].append(i)
deletion=[]
for i in match:
	if len(match[i])<22:
		deletion.append(i)
for i in deletion:
	del match[i]
deletion=[]
for i in match:
	deletion.append([i,match[i][0],match[i][1],match[i][2],match[i][3],match[i][4],match[i][5],match[i][6],match[i][7],match[i][8],match[i][9],match[i][10],,match[i][10],,match[i][11],match[i][12],match[i][13],match[i][14],match[i][15],match[i][16],match[i][17],match[i][18],match[i][19],match[i][20],match[i][21]])
x=pd.DataFrame(deletion,columns=['match','player0','player1','player2','player3','player4','player5','player6','player7','player8','player9','player10','player10','player11','player12','player13','player14','player15','player16','player17','player18','player19','player20','player21'])
x.to_csv("cricket/data/list")