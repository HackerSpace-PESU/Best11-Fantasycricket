from flask import Flask, request, render_template, redirect, url_for, session
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
    
    return render_template("result.html", t1=players[0], t2=players[1], t3=players[2]
                           , t4=players[3], t5=players[4], t6=players[5], t7=players[6]
                           , t8=players[7], t9=players[8], t10=players[9], t11=players[10])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)