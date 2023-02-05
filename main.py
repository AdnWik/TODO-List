import os
import datetime
from peewee import *


dataBaseName = 'todo'+'.db'

# TODO:
if os.path.exists(dataBaseName):
    os.remove(dataBaseName)

if not os.path.exists(dataBaseName):
    db = SqliteDatabase(dataBaseName)  # ':memory:'


class BaseModel(Model):
    class Meta:
        database = db


class TaskState(BaseModel):
    state = CharField(null=False)


class Task(BaseModel):
    task = CharField(null=False)
    createDate = DateTimeField(default=datetime.datetime.now)
    deadLine = DateTimeField()
    state = ForeignKeyField(TaskState, null=False, default=1)


def initialization_data():
    db.connect()
    db.create_tables([Task, TaskState])

    todo = TaskState(state='To Do')
    todo.save()

    inp = TaskState(state='In progress')
    inp.save()

    done = TaskState(state='Done')
    done.save()

    db.close()


initialization_data()


while True:

    print('\nThis is test message')
    print('\n0 - END\n1- Add task\n')
    choice = int(input('\n-> '))

    if choice == 0:
        break

    if choice == 1:
        print('Processing ......')
        db.connect()
        task1 = Task(task='test', deadLine="2023-02-07", state=1)
        task1.save()
        db.close()
