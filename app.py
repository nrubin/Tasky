from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
import datetime
from Tasky import Task, Tasklist
import json
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "\x8d\xd4\x9b\xef\x8fB\xa2\x02\xd9\x9a\xd5\xd4\x8eD\x1b'\xdf\n\x8b4\x8fhB\xbb"
tasks = []
tasklists = {}

def setup_db(server_address='sqlite:///TASKY_DB.db',echo=True,convert_unicode=True):
    engine = create_engine(server_address,echo)
    metadata = MetaData(engine)
    #loaded necessary tables
    users = Table('users',metadata,autoload=True)
    tasks = Table('tasks',metadata,autoload=True)
    tasklists = Table('tasklists',metadata,autoload=True)




@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        if request.form['email'] != None:
            #someone is signing up
            print 'now we add their info to the db'
            return redirect(url_for('view_tasks'))
        else:
            #someone is loggin i
            print 'now we log them in and make sure they are in the db'
            return redirect(url_for('view_tasks'))
    return render_template('login.html')


@app.route('/login',methods=['GET','POST'])
def view_tasks():
    # if request.method == 'POST':
    #     #select all of the user's tasklists and tasks from db, populate page with them
    # session['tasks'] = {}
    return render_template('welcome.html',now=str(datetime.datetime.now()),tasks=[])

# def create_task_list():

@app.route('/newtask',methods=['POST'])
def create_task():
    newTaskContent = request.form['newTaskContent']
    newTask = Task(newTaskContent)
    tasks.append(newTask)
    return 'true'

@app.route('/updateTasks',methods=['GET'])
def update_tasks():
    return render_template('task.html',tasks=sorted(tasks, key=lambda task: task.date_created,reverse=True))


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)