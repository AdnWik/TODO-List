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
    stateData = ('ToDo', 'In progress', 'Done')

    db.connect()
    db.create_tables([Task, TaskState])
    for state in stateData:
        TaskState.create(state=state)
    db.close()


def create_task():
    print('Create new task')
    taskName = input('Eneter task name -> ')
    deadLine = input('Enter deadline (YYYY-MM-DD) -> ')
    db.connect()
    task1 = Task(task=taskName, deadLine=deadLine, state=1)
    task1.save()
    db.close()


def show_all_task():
    db.connect()
    response = Task.select(Task, TaskState).join(TaskState)
    print('='*50)
    print(f'You have {len(response)} tasks:')
    for task in response:
        print(
            f"Id: {task.id:<5} Task: {task.task:<50} State: {task.state.state:<8}")
    db.close()
    print('='*50)

# TODO:


def update_task():
    print('Enter task ID to update:')
    taskIdToUpdate = int(input('--> '))
    db.connect()
    task = Task.select().where(Task.id == taskIdToUpdate).get()
    print(task.state.state)
    task.state = TaskState.select().where(TaskState.state == 'Done').get()
    task.save()
    db.close()


def delete_task():
    print('Enter task ID to delete:')
    taskIdToDelete = int(input('--> '))
    db.connect()
    Task.select().where(Task.id == taskIdToDelete).get().delete_instance()
    db.close()


initialization_data()
print('\nThis is test message')
while True:

    print('\n0 - END\n1 - Add task\n2 - Show all tasks\n3 - Update task\n4 - Delete task')
    choice = int(input('\n-> '))

    if choice == 0:
        break

    if choice == 1:
        create_task()

    if choice == 2:
        show_all_task()

    if choice == 3:
        update_task()

    if choice == 4:
        delete_task()
