import json
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_BINDS'] = {'chat': 'sqlite:///chat.db'}
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '' % self.username

class Chats(db.Model):
    __bind_key__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<chat %r>' % self.id

def hasUsername(user):
    names = Users.query.order_by(Users.username).all()
    for name in names:
        if name.username == user:
            return True
    return False

def getJSONList():
    chatList = []
    chats = Chats.query.order_by(Chats.id).all()
    if len(chats) == 0:
        print("YIKES")
        return ""
    for chat in chats:
        obj = {
            "name" : chat.sender,
            "chat" : chat.msg
        }
        chatList.append(obj)
    return chatList

@app.route("/")
def start():
    #db.drop_all()
    db.create_all()
    user = "Chat App Team"
    msg = "Welcome to the chat App, start typing to get started!"

    
    chats = Chats.query.order_by(Chats.id).all()
    if len(chats) == 0:
        chat = Chats(sender=user, msg=msg)
        db.session.add(chat)
        db.session.commit()

    return redirect(url_for("login"))

@app.route('/login/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form["user"]
        user_pass = request.form["pass"]

        users = Users.query.order_by(Users.username)

        for user in users:
            if user.username == user_name and user.password == user_pass:
                return redirect(url_for("profile",username=user_name))#,login=True
        
        return redirect(url_for("error"))

    return render_template('login.html')

@app.route('/register/', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form["user"]
        user_email = request.form["email"]
        pass1 = request.form["pass1"]
        pass2 = request.form["pass2"]

        if hasUsername(user_name): return redirect(url_for("error"))
        if(pass1 != pass2): return redirect(url_for("error"))
        if(pass1 == "" or user_name == "" or user_email == ""): return redirect(url_for("error"))

        user = Users(username = user_name, email = user_email, password = pass1)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("profile",username=user_name))#,login=True

    return render_template('register.html')

 

@app.route('/profile/<username>')
def profile(username):
    if not hasUsername(username):
        return render_template('error.html')

    return render_template('chat_page.html',username=username)

@app.route('/logout/')
def unlogger():
    return redirect(url_for("login"))

@app.route('/error')
def error():
    return render_template('error.html')

@app.route("/new_message/", methods=["POST"])
def new_message():
    user = request.form["username"]
    msg = request.form["message"]

    chat = Chats(sender=user, msg=msg)
    db.session.add(chat)
    db.session.commit()

    return json.dumps(getJSONList())

@app.route("/messages/")
def messages():
    return json.dumps(getJSONList())


if __name__ == "__main__":
    app.run(debug=True)
