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
    Team = Team[0]
    
    players = []
    for i in range(11):
        if Team[i] == "Nathan Coulter":
            players.append("Nathan Coulter Nile")
        elif "Eoin Morgan" in Team[i]:
            players.append("Eoin Morgan")
        elif "Jason Roy" in Team[i]:
            players.append("Jason Roy")
        elif "Liam Plunkett" in Team[i]:
            players.append("Liam Plunkett")
        else:
            players.append(Team[i][:Team[i].find('\xa0')])
    
    return render_template("result.html", t1=players[0], t2=players[1], t3=players[2]
                           , t4=players[3], t5=players[4], t6=players[5], t7=players[6]
                           , t8=players[7], t9=players[8], t10=players[9], t11=players[10])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)