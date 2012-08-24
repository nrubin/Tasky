from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
import datetime
from Tasky import Task, Tasklist
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "\x8d\xd4\x9b\xef\x8fB\xa2\x02\xd9\x9a\xd5\xd4\x8eD\x1b'\xdf\n\x8b4\x8fhB\xbb"
tasks = []
tasklists = {}
db = sqlite3.connect('TASKY_DB.db')

@app.route('/')
def login():
    session['tasks'] = {}
    session['tasklists'] = {}
    print db
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