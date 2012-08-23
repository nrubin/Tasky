import unittest
from Tasky import Task, Tasklist
import datetime

class TestTasky(unittest.TestCase):

	def setUp(self):
		self.foo = Task('foo')
		self.bar = Task('bar',datetime.datetime(2012,9,1),5)
		self.FooBar = Tasklist('FooBar')
		self.FooBar.add_task(self.foo)
		self.FooBar.add_task(self.bar)

	def test_init(self):
		#make sure the attributes are properly assigned
		self.assertEqual(self.foo.content,'foo')
		self.assertEqual(self.bar.deadline,datetime.datetime(2012,9,1))
		self.assertEqual(self.bar.priority,5)

	def test_insertion_and_removal(self):
		#make sure tasks are properly added to the Tasklist object
		self.assertTrue(self.foo in self.FooBar.tasks.values())
		self.FooBar.remove_task(self.foo)
		self.assertFalse(self.foo in self.FooBar.tasks.values())
		self.FooBar.remove_task_by_id(self.bar.id)
		self.assertFalse(self.bar in self.FooBar.tasks.values())


if __name__ == '__main__':
	unittest.main()