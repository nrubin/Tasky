"""
Class structure for my task list. This will organize the rest of the project.
"""

import uuid
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean

Base = declarative_base()

class Task(Base):

	#Initialize what we need for mapping between SQL and an instance object
	__tablename__ = 'tasks'
	id = Column(BigInteger, primary_key=True)
	date_created = Column(DateTime)
	content = Column(String)
	deadline = Column(DateTime)
	priority = Column(Integer)
	completed = Column(Boolean)
	archived = Column(Boolean)

	#initializes the instance with default values.
	def __init__(self,content,deadline=None,priority=0):
		self.content = content
		self.deadline = deadline
		self.priority = priority
		self.completed = False
		self.date_created = datetime.datetime.now()
		self.id = uuid.uuid4().int
		self.archived = False

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

class Tasklist(Base):

	__tablename__ = 'tasklists'
	id = Column(BigInteger, primary_key=True)
	date_created = Column(DateTime)
	title = Column(String)
	priority = Column(Integer)
	archived = Column(Boolean)

	def __init__(self,title,priority=0):
		self.tasks = {}
		self.title = title
		self.priority = priority
		self.id = uuid.uuid4().int
		self.date_created = datetime.datetime.now()
		self.archived = False

	def __repr__(self):
		return "Tasklist: \'%s\' with id %s" % (self.title,self.id)

	def archive(self):
		self.archive = True

	def un_archive(self):
		self.archive = False



class User(Base):

	__tablename__ = 'users'
	id = Column(BigInteger, primary_key=True)
	username = Column(String)
	password = Column(String)
	email = Column(String)
	date_created = Column(DateTime)

	def __init__(self,username,password,email):
		self.id = uuid.uuid4().int
		self.username = username
		self.password = password
		self.email = email
		self.date_created = datetime.datetime.now()

	def __repr__(self):
		return "User %s with id %s" % (self.username,self.id)



# class Task(object):

# 	def __init__(self,content,deadline=None,priority=0):
# 		self.content = content
# 		self.deadline = deadline
# 		self.priority = priority
# 		self.completed = False
# 		self.date_created = datetime.datetime.now()
# 		self.id = uuid.uuid4()
# 		self.archived = False

# 	def complete(self):
# 		self.completed = True

# 	def uncomplete(self):
# 		self.completed = False

# 	def toDict(self):
# 		"""
# 		Makes this object easy to serialize :)
# 		"""
# 		return vars(self)

# class Tasklist(object):

# 	def __init__(self,title,priority=0):
# 		self.tasks = {}
# 		self.title = title
# 		self.priority = priority
# 		self.id = uuid.uuid4()
# 		self.date_created = datetime.datetime.now()
# 		self.archived = False

# 	def add_task(self,task):
# 		if task.id not in self.tasks:
# 			self.tasks[task.id] = task

# 	def remove_task(self,task):
# 		if task.id in self.tasks:
# 			del self.tasks[task.id]
# 		else:
# 			raise KeyError, 'Task is not in %s tasklist' % self.title

# 	def remove_task_by_id(self,id):
# 		if id in self.tasks:
# 			del self.tasks[id]
# 		else:
# 			raise KeyError, 'Task is not in %s tasklist' % self.title


if __name__ == '__main__':
	a = Task('Hello World')
	print a.id
