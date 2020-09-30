from flask import Flask, request, render_template, redirect, url_for, session

#import sys
#sys.path.insert(1, '/cricket/Final Project')

from team import teams

app = Flask(__name__)
app.secret_key = "lol"

@app.route("/", methods=['GET', 'POST'])
def home():
     if request.method == "POST":
         session['match'] = request.form['match']       
         return redirect(url_for("result"))
     else:
         return render_template("index.html")
     
@app.route("/results", methods=['GET', 'POST'])
def result():
    Id = session["match"]
    Team = teams(Id)
    Captain=Team[1]
    VCaptain=Team[2]
    Team = Team[0]

    print(Team)
    
    players = []

    for i in Team:
        if i==Captain:
            x="(C)"
        elif i==VCaptain:
            x="(VC)"
        else:
            x=""    
        if i == "Nathan Coulter":
            players.append("Nathan Coulter Nile"+x)
        elif "Eoin Morgan" in i:
            players.append("Eoin Morgan"+x)
        elif "Jason Roy" in i:
            players.append("Jason Roy"+x)
        elif "Liam Plunkett" in i:
            players.append("Liam Plunkett"+x)
        else:
            players.append(i[:i.find('\xa0')]+x)
    c=[0,0,0,0,0,0,0,0,0,0,0]
    v=[0,0,0,0,0,0,0,0,0,0,0]
    for i in range(len(players)):
        if '(C)' in players[i]:
            c[i]="(C)"
            v[i]=""
            players[i]=players[i][:-3]
        elif '(VC)' in players[i]:
            v[i] ="(VC)"
            c[i]=""
            players[i]=players[i][:-4]
        else:
            v[i]=""
            c[i]=""
    return render_template("result.html", c1=c[0],v1=v[0],t1=players[0], c2=c[1],v2=v[1],t2=players[1], c3=c[2],v3=v[2],t3=players[2]
                           ,c4=c[3],v4=v[3], t4=players[3], c5=c[4],v5=v[4],t5=players[4],c6=c[5],v6=v[5], t6=players[5],c7=c[6],v7=v[6], t7=players[6]
                           ,c8=c[7],v8=v[7], t8=players[7],c9=c[8],v9=v[8],t9=players[8], c10=c[9],v10=v[9],t10=players[9], c11=c[10],v11=v[10],t11=players[10])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
