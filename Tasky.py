"""
Class structure for my task list. This will organize the rest of the project.
"""

import uuid
import datetime

class Task(object):

	def __init__(self,content,deadline=None,priority=0):
		self.content = content
		self.deadline = deadline
		self.priority = priority
		self.completed = False
		self.id = uuid.uuid4()

	def complete(self):
		self.completed = True

	def uncomplete(self):
		self.completed = False

class Tasklist(object):

	def __init__(self,title,priority=0):
		self.tasks = {}
		self.title = title
		self.priority = priority
		self.id = uuid.uuid4()

	def add_task(self,task):
		if task.id not in self.tasks:
			self.tasks[task.id] = task

	def remove_task(self,task):
		if task.id in self.tasks:
			del self.tasks[task.id]
		else:
			raise KeyError, 'Task is not in %s tasklist' % self.title

	def remove_task_by_id(self,id):
		if id in self.tasks:
			del self.tasks[id]
		else:
			raise KeyError, 'Task is not in %s tasklist' % self.title


if __name__ == '__main__':
	a = Task('Hello World')
	print a.id
