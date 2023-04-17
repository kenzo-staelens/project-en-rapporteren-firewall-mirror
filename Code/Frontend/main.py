#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3 as sql
import json
import random
# applicatie herstarten na elke aanpassing, inclusief aanpassingen aan html/css/etc.

config_object=[None]#issues met concurrency en shared references

# maak je eigen sleutels!!!
# openssl req -x509 -newkey rsa:4096 -nodes -out flaskcert.pem -keyout flaskkey.pem -days 365
# of gebruik onderaan de adhoc versie
keyfile = "Frontend/flaskkey.pem"
certfile ="Frontend/flaskcert.pem"

print(keyfile)

app = Flask('app')
token = "" # one time use token for auth
apitoken = "259355acc5f86bbd0f9a9f708209a15595cafcecd8fb79c00b061d3456f64ba8"
# apitoken hoort nrml in een dotenv bestand, nrml zou ik ook iets meer security willen, dit is gewoon omdat dan tests kunnen gedaan worden met de api zonder veel moeite

def retrieveUsers(username, password): #database query login details
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users where username=? and password=?",(username, password))
	user = cur.fetchone()
	con.close()
	return user

#ik krijg flask_login niet deftig in orde, this has to do
@app.route('/', methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    global token
    if request.method == "POST": # als post request van login scherm
        info = json.loads(request.data) #over json want query https is veilig
        username = info.get('username', 'guest')
        password = info.get('password', '')
        user=None
        user = retrieveUsers(username, password) # get user from query
        if user: #als user bestaat
            #return new one time login token
            token=''.join(random.choice('0123456789abcdef') for n in range(64))
            return json.dumps({"token": token}),200,{'ContentType':'application/json'}
        else:
            #anders invalid login
            return json.dumps({"reason": "Username or Password Error"}),401,{'ContentType':'application/json'}
    if request.method == "GET":
        Token = request.args.get("token")
        if Token == None: # token is a one time use token for authentication
            return render_template("login.html")
            Token = None
        elif Token!=token:
            return render_template("unauthorized.html")
        else:
            return render_template("index.html",apitoken=apitoken)

    
#used error codes:
#200: ok -> processed correctly
#400 bad request -> values not valid
#401: unauthorized -> invalid auth token
#500: internal server error -> something else failed
def ProcessTheData(jsonData):
    global apitoken
    try:
        if(jsonData['apitoken']!=apitoken):
            return 401
        #process here
        return 200
    except:
        return 500
    
@app.post("/api")
def api():
    httpStatus = ProcessTheData(request.json) 
    if(httpStatus == 200):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), httpStatus, {'ContentType':'application/json'}

def main(config):
    config_object[0]=config
    app.run(host="0.0.0.0",port=8080, ssl_context=(certfile,keyfile))

if __name__ == "__main__":
    main(None)
    #app.run(host='0.0.0.0', port=8080, ssl_context=(certfile,keyfile))
    #app.run(host="0.0.0.0",port=8080,ssl_context='adhoc')

