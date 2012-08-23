from flask import Flask, session, render_template, request, redirect, url_for, abort, jsonify
import datetime
from Tasky import Task, Tasklist
import json

app = Flask(__name__)
tasks = {}
tasklists = {}

@app.route('/')
def hello_world():
    return render_template('welcome.html',now='Right now',tasks=[])

# def create_task_list():

@app.route('/newtask',methods=['POST'])
def create_task():
	newTaskContent = request.form['newTaskContent']
	newTask = Task(newTaskContent)
	tasks[str(newTask.id.int)] = [newTask.content]
	return 'true'

@app.route('/updateTasks',methods=['GET'])
def update_tasks():
	return json.dumps(tasks)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)