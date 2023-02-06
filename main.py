import os
import datetime
from peewee import *


dataBaseName = 'todo'+'.db'

# TODO:
"""
if os.path.exists(dataBaseName):
    os.remove(dataBaseName)
"""
# if not os.path.exists(dataBaseName):
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
    print('\n0 - END\n1- Add task\n2 - Show all tasks\n')
    choice = int(input('\n-> '))

    if choice == 0:
        break

    if choice == 1:
        print('Create new task')
        taskName = input('Eneter task name -> ')
        deadLine = input('Enter deadline (YYYY-MM-DD) -> ')
        db.connect()
        task1 = Task(task=taskName, deadLine=deadLine, state=1)
        task1.save()
        db.close()

    if choice == 2:
        db.connect()
        print('\nAll task:\n')
        for task in Task.select(Task, TaskState).join(TaskState):
            print(
                f"Id: {task.id:<5} Task: {task.task:<50} State: {task.state.state:<8}")
        db.close()
