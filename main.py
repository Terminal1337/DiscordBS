from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import time
from helpers.hashpass import *

app = FastAPI()
templates = Jinja2Templates(directory="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/topup", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("credits.html", {"request": request})



@app.get("/discord", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})






def read_data():
    with open('database/database.json','r') as f:
        data = json.load(f)
        return data

@app.get('/api/balance')
async def checkBalance(token,action):
    try:
        if action == "0": # 0 = check balance
            data = read_data()
            for i in data:
                if data[i]['cookie'] == token:
                    return {'error': False, 'message':"Successfully Retrieved Balance","credits":data[i]['credits']}
            return  {'error': True,'message': "User Creds Mismatch"}

        if action == "1": # 1 = update balance with -1
            data = read_data()
            for i in data:
                if data[i]['cookie'] == token:
                    data[i]['credits'] -= 1
                    t = data[i]['credits']
                    with open('database/database.json','w') as f:
                        json.dump(data,f)
                    return {'error': False,"message":"Balance Updated Successfully","credits":t}
        else:
            return {'error':True,"message":"Invalid Parameters"}


    except Exception as e:
        return {'error': True,'message':str(e)}

@app.get('/api/topup')
async def apitopup(code,token):
    try:

        with open('database/vouchers.json','r') as f:
            data = json.load(f)
            for i in data:
                if code in data[i]['codes']:
                    data[i]['codes'].remove(code)
                    with open('database/vouchers.json','w') as f:
                        json.dump(data,f)
                    creds = i
                    data = read_data()
                    for j in data:
                        if data[j]['cookie'] == token:
                            data[j]['credits'] += int(creds)
                            with open('database/database.json','w') as f:
                                json.dump(data,f)
                            return {"error":False,"message":f"{creds} credits added successfully"}
                    return {'error':True,"message":"Invalid Session"}
                else:
                    return {'error':True,'message':"Invalid Voucher"}
    except Exception as e:
        return {"error":True,"message":str(e)}
@app.get('/api/register')
async def register(username,password):
    try:
        data = read_data()
        if username in read_data():
            return {"error":False,"message":"user already exists"}
        if len(password) < 8:
            return {"error":False,"message":"password must be 8 characters long"}
        data[username] = {
            "date": int(time.time()),
            "password": md5_hash_password(password),
            "cookie": generate_random_string(32),
            "credits":0
        }
        with open('database/database.json','w') as f:
            json.dump(data,f)
        return {"error":False,"message":"user created successfully"}
    except Exception as e:
        return {"error":True,"message":str(e)}
    

@app.get('/api/login')
async def register(username,password):
    try:
        data = read_data()
        if not username in read_data():
            return {"error":False,"message":"user does not exist"}
        if data[username]['password'] != md5_hash_password(password):
            return {"error":False,"message":"incorrect password"}
        cookie = data[username]['cookie']
        return {"error":False,"message":"user logged in successfully","token":cookie} 
    except Exception as e:
        return {"error":True,"message":str(e)}

@app.get('/api/dashboard')
def dashboard(token):
    try:
        data = read_data()
        for i in data:
            if data[i]['cookie'] == token:
                username = i
                password = data[i]['password']
                credits = data[i]['credits']
                registered = data[i]['date']
                return {"error":False,"message":"user found","data":{"username":username,"password":password,"credits":credits,"registered":registered}}
    except Exception as e:
        return {"error":True,"message":str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8000)