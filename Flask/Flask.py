# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:43:19 2020

@author: Raviprasad
"""

from flask import Flask, request, render_template, redirect, url_for, session
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
    #team1 = session['match'].split()[0]
    #team2 = session['match'].split()[2]
    
    return render_template("result.html", t1 = session["match"])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)