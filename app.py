from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
from models import User, Task, Tasklist
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import *
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TASKY_DB.db'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = "\x8d\xd4\x9b\xef\x8fB\xa2\x02\xd9\x9a\xd5\xd4\x8eD\x1b'\xdf\n\x8b4\x8fhB\xbb"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User(request.form['username'],request.form['password'])
        if user.is_authenticated() and user.exists(): 
            login_user(user)
            flash("Logged In successfuly")
            return "here are your tasks"
            #return redirect(url_for('view_tasks'))
        else:
            return 'User was not successfully authenticated'
    return render_template('login.html')

@app.route('/newaccount',methods=['POST'])
def create_account():
    new_user = User(request.form['username'],request.form['password'])
    if not new_user.exists():
        db.session.add(new_user)
        db.session.commit()
        return "here are your tasks"
        #return redirect(url_for('view_tasks'))
    else:
        flash("You already exist")
        return 'you already exist'



def view_tasks():
    return "here are your tasks"

def create_task_list():
    pass

@app.route('/newtask',methods=['POST'])
@login_required
def create_task():
    newTaskContent = request.form['newTaskContent']
    newTask = Task(newTaskContent)
    tasks.append(newTask)
    return 'true'

@app.route('/updateTasks',methods=['GET'])
def update_tasks():
    return render_template('task.html',tasks=sorted(tasks, key=lambda task: task.date_created,reverse=True))


class Task(db.Model):

    #Initialize what we need for mapping between SQL and an instance object
    __tablename__ = 'tasks'
    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime)
    content = db.Column(db.String)
    deadline = db.Column(db.DateTime)
    priority = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    archived = db.Column(db.Boolean)

    #relate it to a user and a task list
    # tasklist_id = db.Column(db.BigInteger, db.ForeignKey('tasklist.id'))
    # user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))


    #initializes the instance with default values.
    def __init__(self,content,deadline=None,priority=0):
        self.content = content
        self.deadline = deadline
        self.priority = priority
        self.completed = False
        self.date_created = datetime.utcnow()
        self.id = uuid.uuid4().hex
        self.archived = False
        self.tasklist = tasklist
        self.user = user

    def __repr__(self):
        return "Task: \'%s\' with id %s" % (self.content,self.id)

    #helper/instance methods
    def complete(self):
        self.completed = True

    def uncomplete(self):
        self.completed = False

    def archive(self):
        self.archive = True

    def un_archive(self):
        self.archive = False

class Tasklist(db.Model):

    __tablename__ = 'tasklists'
    id = db.Column(db.BigInteger, primary_key=True)
    date_created = db.Column(db.DateTime)
    title = db.Column(db.String)
    priority = db.Column(db.Integer)
    archived = db.Column(db.Boolean)
    # tasks = db.relationship("Task",backref="tasklists")



    def __init__(self,title,priority=0):
        self.tasks = {}
        self.title = title
        self.priority = priority
        self.id = uuid.uuid4().hex
        self.date_created = datetime.utcnow()
        self.archived = False
        self.user = user

    def __repr__(self):
        return "Tasklist: \'%s\' with id %s" % (self.title,self.id)

    def archive(self):
        self.archive = True

    def un_archive(self):
        self.archive = False



class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    date_created = db.Column(db.DateTime)

    # tasks = db.relationship("Task",backref="users")
    # tasklists = db.relationship("Tasklist",backref="users")

    def __init__(self,username,password):
        self.id = uuid.uuid4().hex
        self.username = username
        self.password = password
        self.date_created = datetime.utcnow()

    def __repr__(self):
        return "User %s with id %s" % (self.username,self.id)

    def is_authenticated(self):
        """
        Need to deal with three cases:
        either the user exists and has the right password,
        or the user exists but has the wrong password,
        or the user doesn't exist and therefore the password doesn't matter
        """
        print 'authenticating'
        user_query = User.query.filter_by(username=self.username).first()
        if user_query is not None:
            print 'username exists'
            if user_query.password == self.password:
                print 'password works'
                return True
        return False


    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        user_query = User.query.filter_by(username=self.username).first()
        return unicode(user_query.id)

    def exists(self):
        print self.id, self.username, self.password
        return (not (User.query.filter_by(username=self.username).first() == None))


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)
