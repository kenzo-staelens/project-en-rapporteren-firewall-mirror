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

app = Flask(__name__, template_folder='templates')
token = "" # one time use token for auth
apitoken = "259355acc5f86bbd0f9a9f708209a15595cafcecd8fb79c00b061d3456f64ba8"
# apitoken hoort nrml in een dotenv bestand, nrml zou ik ook iets meer security willen, dit is gewoon omdat dan tests kunnen gedaan worden met de api zonder veel moeite

def retrieveUsers(username, password): #database query login details
    con = sql.connect("Frontend/database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users where username=? and password=?",(username, password))
    user = cur.fetchone()
    con.close()
    return user

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
                 
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
            return redirect(url_for(f"home",token=token))
            #return render_template("dashboard.html",apitoken=config_object[0]["apikey"])


@app.get('/home')
def home():
    global token
    Token = request.args.get("token")
    if Token == None:
        return redirect(url_for("login"), code=302)
    elif Token!=token:
        return redirect(url_for("unauthorized"), code=302)
    else:
        return render_template("home.html", logintoken=token)

@app.get('/dashboard')
def dashboard():
    global token
    Token = request.args.get("token")
    if Token == None:
        return redirect(url_for("login"), code=302)
    elif Token!=token:
        return redirect(url_for("unauthorized"), code=302)
    else:
        return render_template("dashboard.html", apitoken=config_object[0]["apikey"], logintoken=token)

@app.get("/settings")
def settings():
    global token
    Token = request.args.get("token")
    if Token == None:
        return redirect(url_for("login"), code=302)
    elif Token!=token:
        return redirect(url_for("unauthorized"), code=302)
    else:
        return render_template("settings.html", logintoken=token, apitoken=config_object[0]["apikey"])
    
@app.get("/traffic")
def traffic():
    global token
    Token = request.args.get("token")
    if Token == None:
        return redirect(url_for("login"), code=302)
    elif Token!=token:
        return redirect(url_for("unauthorized"), code=302)
    else:
        return render_template("traffic.html", logintoken=token)

@app.get('/unauthorized')
def unauthorized():
    return render_template("unauthorized.html")
    
#used error codes:
#200: ok -> processed correctly
#400 bad request -> values not valid
#401: unauthorized -> invalid auth token
#500: internal server error -> something else failed
def ProcessTheData(jsonData, module):
    #global apitoken
    try:
        if(jsonData['apitoken']!=config_object[0]["apikey"]):
            return 401
        #process here
        addedRules = jsonData["postdata"][0]["data"]
        modulename = module[3:]
        layer = f"{module[:2]}_modules"
        
        #returns status code
        return config_object[0][layer][modulename][0].postconfig(addedRules)
    except Exception as e:
        print("    ",end="")
        print(e)   
        return 500
    
@app.post("/api/settings/<module>")
def api(module):
    httpStatus = ProcessTheData(request.json, module) 
    #print("json: ", request.json)
    if(httpStatus == 200):
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), httpStatus, {'ContentType':'application/json'}

@app.get("/api/<endpoint>")
def apiget(endpoint):
    if endpoint == "InstalledModules":
        response = {"data":[]}
        for key in config_object[0]["L3_modules"]:
            response["data"].append({"name":f"L3-{key}", "displayName":f"{key}"})
        for key in config_object[0]["L4_modules"]:
            response["data"].append({"name":f"L4-{key}", "displayName":f"{key}"})
        return json.dumps(response), 200, {'ContentType':'application/json'}
    
    if endpoint == "Traffic":
        trafficTemplate = {
            "name" : "traffic",
            "displayName" : "Traffic captured",
            "data" : [{ "name": "All traffic", "type": "table", "data": [] }]
        }
        
        with open(config_object[0]["logfile"],"r") as f:
            logentries = []
            entrynum=1
            for line in f.readlines():
                logentries.append({"no.":entrynum, "entry": line})
                entrynum+=1
        trafficTemplate["data"][0]["data"]=logentries
        return json.dumps(trafficTemplate),200, {'ContentType':'application/json'}
    return json.dumps({}),404, {'ContentType':'application/json'}



@app.get("/api/settings/<module>")
def apigetsettings(module):
    modulename = module[3:]
    layer = f"{module[:2]}_modules"
    table = config_object[0][layer][modulename][0].getconfig()
    retobj = {"name":"module", "displayName":modulename,"data":[
            #{"name":"Enable", "desc":"enables module", "type":"bool","data":True}
        ]
    }
    if len(table)>0:
        retobj["data"].append({
            "name":"rules",
            "displayName":"rules",
            "type":"table","data":table
        })
    
    return json.dumps(retobj),200,{'ContentType':'application/json'}

def main(config):
    config_object[0]=config
    app.run(host="0.0.0.0",port=8080, ssl_context=(certfile,keyfile))

if __name__ == "__main__":
    main(None)
    #app.run(host='0.0.0.0', port=8080, ssl_context=(certfile,keyfile))
    #app.run(host="0.0.0.0",port=8080,ssl_context='adhoc')

