from datetime import datetime
from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import string
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exam.db'

db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    kode = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    nama = db.Column(db.String(50))
    status = db.Column(db.String(50),default = '0')
    isLogin = db.Column(db.String(50),default = '0')
    waktu = db.Column(db.DateTime ,default =datetime.now)
class Roomed(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    kodeRoom = db.Column(db.String(50))
    kodeUser = db.Column(db.String(50))
    status = db.Column(db.String(50))
    waktu = db.Column(db.DateTime ,default =datetime.now)
class Answered(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    kode = db.Column(db.String(50))
    kodeQuest = db.Column(db.String(50))
    kodeUser = db.Column(db.String(50))
    answer = db.Column(db.String(1000))
    status = db.Column(db.String(50))
    nilai = db.Column(db.String(50),default = '0')
    waktu = db.Column(db.DateTime ,default =datetime.now)
class Room(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    kode = db.Column(db.String(50))
    kodeRoom = db.Column(db.String(50))
    nama = db.Column(db.String(50))
    waktu = db.Column(db.DateTime ,default =datetime.now)
class Question(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    kode = db.Column(db.String(50))
    kodeRoom = db.Column(db.String(50))
    question = db.Column(db.String(1000))
    answer = db.Column(db.String(1000))
    optionD = db.Column(db.String(1000))
    optionA = db.Column(db.String(1000))
    optionB = db.Column(db.String(1000))
    optionC = db.Column(db.String(1000))
    optionD = db.Column(db.String(1000))
    status = db.Column(db.String(50),default ="1")
    waktu = db.Column(db.DateTime ,default =datetime.now)

def randomKode(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/api/register/user', methods=['POST'])
def regUser():
    getJson = request.json
    user = User.query.filter_by(username=getJson['username']).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return '{"status" : "2"}'#user sudah ada
    register = User(kode = randomKode(8),username = getJson['username'],password = getJson['password'],nama = getJson['nama'],status = getJson['status'])
    db.session.add(register)
    db.session.commit()
    return '{"status" : "1"}'
@app.route('/api/login/user', methods=['POST'])
def loginUser():
    getJson = request.json
    user = User.query.filter_by(username = getJson['username'] ).first()
    
    if user:
        if getJson['password'] == user.password:
            
            user.isLogin = '1'
            db.session.commit()
            response = {'status':'1','kode':'%s'%(user.kode),'pangkat':'%s'%(user.status)}
            return jsonify(response) #sukses Login
    else:
        return  jsonify(2) #Akun Belum Terdaftar
    return  jsonify(0) #username atau password salah 
@app.route('/api/req/user/data/<kode>', methods=['GET'])
def dataUser(kode):
    #getJson = request.json
    user = User.query.filter_by(kode = kode ).first()
    response = {'username':'%s'%(user.username),'nama':'%s'%(user.nama)}
    return  jsonify(response) #username atau password salah 
@app.route('/api/register/room',methods=['POST'])
def regRoom():
    getJson = request.json
    # check = User.query.filter(kode= getJson['kodeUser'],nama = getJson['nama'] ).first()
    # if check :
    #     return "Anda sudah membuat Room Dengan Nama Tersebut"
    kodeRoom = randomKode(8)
    room = Room(kode = getJson['kodeUser'],kodeRoom=kodeRoom ,nama = getJson['nama'])
    db.session.add(room)
    db.session.commit()
    
    response = {'status':'1','kodeRoom' : '%s'%(kodeRoom),'nama':'%s'%(getJson['nama'])}
    return jsonify(response)

@app.route('/api/req/room/data/<kode>', methods=['GET'])
def dataRoom(kode):
    check = Room.query.filter_by(kode=kode ).first()
    
    if not check:
        return jsonify(0)
    json = '['
    #getJson = request.json
    room = Room.query.filter_by(kode=kode).all()
    #response = {'username':'%s'%(user.username),'nama':'%s'%(user.nama)}
    for i in room:
        json+='{"kodeRoom" : "%s","nama":"%s"},'%(i.kodeRoom,i.nama)
       
    json=json[:-1]
    json+=']'
    return  json #username atau password salah
@app.route('/api/check/correct/<kodeUser>/<kodeRoom>', methods=['GET'])
def checkCorrect(kodeUser,kodeRoom):
    benar = 0
    salah = 0
    check = Answered.query.filter_by(kode= kodeRoom,kodeUser = kodeUser).all()
    for i in check:
        if i.status == "benar":
            benar+=1
        else:
            salah+=1
    return '{"benar" : "%s","salah":"%s"}'%(benar,salah)
@app.route('/api/check/answered/all/<kodeUser>/<kodeRoom>', methods=['GET'])
def checkAllAnswered(kodeUser,kodeRoom):
    check = Answered.query.filter_by(kode= kodeRoom,kodeUser = kodeUser).all()
    for i in check:
        if i.answer != "A" and i.answer != "B" and i.answer != "C" and i.answer != "D" :
            return jsonify(0)
    return jsonify(1)
@app.route('/api/check/room/<kodeRoom>', methods=['GET'])
def checkRoom(kodeRoom):
    check = Room.query.filter_by(kodeRoom=kodeRoom ).first()
    if check:
        return jsonify(1)
    return jsonify(0) #username atau password salah 

@app.route('/api/req/room/name/<kodeRoom>', methods=['GET'])
def nameRoom(kodeRoom):
    room = Room.query.filter_by(kodeRoom = kodeRoom ).first()
    json='{"nama" : "%s"}'%(room.nama)
    return json #username atau password salah 

@app.route('/api/req/question/data/<kodeRoom>', methods=['GET'])
def dataQuestion(kodeRoom):
    check = Question.query.filter_by(kodeRoom=kodeRoom ).first()
    
    if not check:
        return jsonify(0)
    json = '['
    #getJson = request.json
    questions = Question.query.filter_by(kodeRoom=kodeRoom).all()
    #response = {'username':'%s'%(user.username),'nama':'%s'%(user.nama)}
    for i in questions:
        json+='{"kodeQuest" : "%s","question":"%s","answer":"%s","optionA":"%s","optionB":"%s","optionC":"%s","optionD":"%s"},'%(i.kode,i.question,i.answer,i.optionA,i.optionB,i.optionC,i.optionD,)
        
        print(questions)
    json=json[:-1]
    json+=']'
    return  json #username atau password salah 
@app.route('/api/req/answered/data/<kodeUser>/<kodeRoom>', methods=['GET'])
def dataAnswered(kodeUser,kodeRoom):
    json = '['
    answered = Answered.query.filter_by(kodeUser=kodeUser,kode=kodeRoom ).all()
    if not answered:
        return jsonify(0)
    for i in answered:
        json+='{"kodeQuest" : "%s","answer" : "%s","status":"%s"},'%(i.kodeQuest,i.answer,i.status,)
    json=json[:-1]
    json+=']'
    return  json #username atau password salah 
@app.route('/api/req/question/single/data/<kodeQuest>', methods=['GET'])
def dataSingleQuestion(kodeQuest):
    question = Question.query.filter_by(kode=kodeQuest).first()  
    json ='{"kodeQuest" : "%s","question":"%s","answer":"%s","optionA":"%s","optionB":"%s","optionC":"%s","optionD":"%s"}'%(question.kode,question.question,question.answer,question.optionA,question.optionB,question.optionC,question.optionD,)
    return  json #username atau password salah 
@app.route('/api/register/roomed',methods=['POST'])
def regRoomed():
    getJson = request.json
    check = Roomed.query.filter_by(kodeRoom= getJson['kodeRoom'],kodeUser = getJson['kodeUser']).first()
    if check:
        check.status = getJson['status']
        db.session.add(check)
        db.session.commit()
        return "updated"
    roomed = Roomed(kodeRoom = getJson['kodeRoom'],kodeUser = getJson['kodeUser'],status = getJson['status'])
    db.session.add(roomed)
    db.session.commit()
    return jsonify(getJson)
@app.route('/api/check/isOpen/<kodeUser>/<kodeRoom>', methods=['GET'])
def checkRoomed(kodeUser,kodeRoom):
    check = Roomed.query.filter_by(kodeRoom= kodeRoom,kodeUser = kodeUser).first()
    if check:
        return '{"status" : "1","isOpen" : "%s" }'%(check.status)
    return '{"status" : "0","isOpen" : "no" }' #username atau password salah 

@app.route('/api/req/roomed/data/<kodeUser>', methods=['GET'])
def dataRoomed(kodeUser):
    check = Roomed.query.filter_by(kodeUser=kodeUser ).first()
    
    if not check:
        return jsonify(0)
    json = '['
    #getJson = request.json
    roomed = Roomed.query.filter_by(kodeUser= kodeUser).all()
    #response = {'username':'%s'%(user.username),'nama':'%s'%(user.nama)}
    for i in roomed:
        json+='{"kodeRoom" : "%s","status":"%s"},'%(i.kodeRoom,i.status,)
    json=json[:-1]
    json+=']'
    return  json #username atau password salah 
@app.route('/api/register/quest',methods=['POST'])
def regQuest():
    getJson = request.json
    check = Question.query.filter_by(kode= getJson['kodeQuest']).first()
    if check:
        check.question = getJson['question']
        check.answer = getJson['answer']
        check.optionA = getJson['optionA']
        check.optionB = getJson['optionB']
        check.optionC = getJson['optionC']
        check.optionD = getJson['optionD']
        db.session.add(check)
        db.session.commit()
        return jsonify(0)
    quest = Question(kode= randomKode(8),kodeRoom = getJson['kodeRoom'],question = getJson['question'],answer = getJson['answer'],optionA = getJson['optionA'],optionB = getJson['optionB'],optionC = getJson['optionC'],optionD = getJson['optionD'])
    db.session.add(quest)
    db.session.commit()
    return jsonify(getJson)

@app.route('/api/register/answer',methods=['POST'])
def regAnswer():
    getJson = request.json
    check = Answered.query.filter_by(kodeQuest=getJson['kodeQuest']).first()
    if check:
        check.answer = getJson['answer']
        db.session.add(check)
        db.session.commit()
        return "updated"
    
    answer = Answered(kode= getJson['kodeRoom'],kodeQuest = getJson['kodeQuest'],kodeUser = getJson['kodeUser'],answer = getJson['answer'],status = getJson['status'])
    db.session.add(answer)
    db.session.commit()
    return jsonify(getJson)

@app.route('/api/req/quest/answer/<kodeUser>/<kodeQuest>', methods=['GET'])
def answeredQuest(kodeUser,kodeQuest):
    search = Answered.query.filter_by(kodeUser = kodeUser,kodeQuest = kodeQuest).first()
    if not search:
        return '{"status" : "0"}'
    json='{"answer" : "%s","kode" : "%s","status" : "1"}'%(search.answer,search.kode)
    print(search.answer)
    return json #username atau password salah 

@app.route('/api/check/result/<kodeUser>/<kodeRoom>', methods=['GET'])
def checkResult(kodeUser,kodeRoom):
    check = Answered.query.filter_by(kode= kodeRoom,kodeUser = kodeUser).all()
    for i in check:
        question = Question.query.filter_by(kode=i.kodeQuest).first()
        if i.answer == question.answer:
            i.status = "benar"
        else:
            i.status = "salah"
        db.session.add(i)
        db.session.commit()
        print(i.status)
    return jsonify(1) #username atau password salah 
if __name__ == "__main__":
    app.run(debug=True)