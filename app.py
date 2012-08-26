from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
from models import User, Task, Tasklist
import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import *
import uuid
import inspect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TASKY_DB.db' #set db uri
app.config['SQLALCHEMY_ECHO'] = False #disable this when not in debug
app.secret_key = "\x8d\xd4\x9b\xef\x8fB\xa2\x02\xd9\x9a\xd5\xd4\x8eD\x1b'\xdf\n\x8b4\x8fhB\xbb" #4 da sessunz
db = SQLAlchemy(app) #build the associated db
login_manager = LoginManager()
login_manager.setup_app(app) #make sure logins work
@login_manager.user_loader
def load_user(userid):
    """
    Given a user id, returns a User object associated with that id.
    Used by login manager for login stuff
    """
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    return User.query.filter_by(id=userid).first()

@app.route('/')
def root():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    if request.method == 'POST': 
        user = User(request.form['username'],request.form['password']) #make a new user object (not pushed to DB yet)
        if user.is_authenticated(): #if this user object is legit and is in the DB and the password is right
            login_user(user) #we will mark the user logged in
            print 'current user is now %s' %(user)
            return redirect(url_for('home'))
        else:
            return 'User was not successfully authenticated'
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    db.session.commit()
    logout_user()
    return 'goodbye'

@app.route('/newaccount',methods=['POST'])
def create_account():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    new_user = User(request.form['username'],request.form['password'])
    if not new_user.exists():
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        flash("You already exist")
        return 'you already exist'


@app.route('/home')
@login_required
def home():
    current_user_id = session['user_id']
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    my_tasklists = Tasklist.query.filter_by(parent_user_id=current_user_id)
    my_tasks = Task.query.filter_by(parent_user_id=current_user_id)
    task_data = {}
    for tasklist in my_tasklists:
        task_data[tasklist.id] = [task for task in my_tasks if task.parent_tasklist_id == tasklist.id]
    return render_template('home.html',task_data = task_data)

@app.route('/createtasklist',methods=['GET','POST'])
@login_required
def create_tasklist():
    if request.method == 'POST':
        print 'Creating tasklist....'
        current_user_id = session['user_id']
        tasklist_title = request.form['newTasklistTitle']
        tasklist_priority = request.form['newTasklistPriority']
        new_tasklist = Tasklist(current_user_id,tasklist_title,tasklist_priority)
        db.session.add(new_tasklist)
        db.session.commit()
        return 'true'
    else:
        print 'Why is this a get request...'
        return redirect(url_for('home'))


@app.route('/updatetasklists')
@login_required
def update_tasklists():
    current_user_id = session['user_id']
    tasklists = Tasklist.query.filter_by(parent_user_id=current_user_id)
    tasklists_serializable = [ {'tasklistTitle' : tasklist.title, 'tasklistPriority' : tasklist.priority,'tasklistID' : str(tasklist.id),'tasklistArchived' : 'true' if tasklist.archived else 'false'} for tasklist in tasklists]
    return(json.dumps(tasklists_serializable))

@app.route('/newtask',methods=['POST'])
@login_required
def create_task():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
    current_user_id = session['user_id']
    task_content = request.form['task_content']
    deadline = request.get('deadline',None)
    priority = request.get('priority',0)
    parent_tasklist_id = request['parent_tasklist_id']
    new_task = Task(parent_tasklist_id,current_user_id,task_content,deadline,priority)
    db.session.add(new_task)
    return 'true'

@app.route('/updateTasks',methods=['GET'])
def update_tasks():
    # print "I am %s and my daddy is %s" % (whoami(),whosmydaddy())
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
    parent_user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    parent_tasklist_id = db.Column(db.BigInteger,db.ForeignKey('tasklists.id'))



    #initializes the instance with default values.
    def __init__(self,parent_tasklist_id,parent_user_id,content,deadline=None,priority=0):
        self.content = content
        self.deadline = deadline
        self.priority = priority
        self.completed = False
        self.date_created = datetime.utcnow()
        self.id = uuid.uuid4().hex
        self.archived = False
        self.parent_tasklist_id = parent_tasklist_id
        self.parent_user_id = parent_user_id

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
    parent_user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    tasks = db.relationship('Task')



    def __init__(self,parent_user_id,title,priority=0):
        self.parent_user_id = parent_user_id
        self.title = title
        self.priority = priority
        self.id = uuid.uuid4().hex
        self.date_created = datetime.utcnow()
        self.archived = False

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
    tasklists = db.relationship('Tasklist')

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
        user_query = User.query.filter_by(username=self.username).first()
        if user_query is not None:
            if user_query.password == self.password:
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
        return (not (User.query.filter_by(username=self.username).first() == None))

def whoami():
    return inspect.stack()[1][3]

def whosmydaddy():
    return inspect.stack()[2][3]


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)
