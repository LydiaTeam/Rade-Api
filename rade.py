#@LydiaTeam 

#Libs
import requests, json
from flask import Flask, escape, request
from flask import json

#info
site = "https://my.rade.ir/panel"
username = "" #Rade Username
password = "" #Rade Password
ip = "localhost"
port = 8000
#info

datacard = []
dicdatacard = {}

#Headers
rade_headers = {
    'Host': 'my.rade.ir',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chromium/80.0.3987.160 Chrome/80.0.3987.163 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': 'https://my.rade.ir',
    'Connection': 'keep-alive',
}


app = Flask(__name__)

@app.route("/")
def hello():
    name = request.args.get("name", "@LydiaTeam")
    return f'Hello, {escape(name)}!'

@app.route("/getinfo", methods = ['POST', 'GET'])
def getinfo():
    global dicdatacard, datacard
    postcard = request.args.get("card")
    if postcard.isdigit():
        if str(postcard) in datacard: 
            print("iam in the list")
            return dicdatacard[postcard]
        else:    
            resultt = get_card_information(postcard)
            if resultt:
                dicdatacard[f"{postcard}"] = resultt
                datacard.append(str(postcard))
                print(datacard)
                return resultt
            else:
                return "Login request executed refresh the page"
    else:
        return "what the fuck budy ?"
        

session = requests.session()
#Defs
def login():
    global rade_headers

    csrf = session.get('https://my.rade.ir/api/v2/csrf-cookie', headers=rade_headers)
    rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in csrf.cookies])

    payload = {

       "username":f"{username}",
       "password":f"{password}",
       "captcha":"",
       "reference":None
    }

    res = session.post('https://my.rade.ir/api/v2/login', json=payload, headers=rade_headers)
    rade_headers['Cookie'] = '; '.join([x.name + '=' + x.value for x in res.cookies])

    if res.status_code == 200:
        return True
    else:
        return False
    
    
def get_card_information(card):
    global rade_headers
    try:
        payload = {
            'card_number':	f"{card}"
        }

        response = session.post('https://my.rade.ir/api/v2/service/cardToIban', json=payload, headers=rade_headers)

        if response.status_code == 200:
            jsondata = json.loads(response.text)
            return jsondata['data']

        else:
           print(response.text)
           login()
           return False
           
    except Exception as e:
        print(e)
        
#get_card_information('6037997347404429')
#login()

if __name__ == '__main__':
    app.run(host=ip, port=port)

#👤 OwnerName: resultt['result']['result']['depositOwners']
#🗂 Shabah: resultt['result']['result']['IBAN']
#🔘 Hesab : resultt['result']['result']['deposit']