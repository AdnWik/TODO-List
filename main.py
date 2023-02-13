import os
import datetime
from peewee import *


dataBaseName = 'todo'+'.db'

# TODO:


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


def reset_database():
    if os.path.exists(dataBaseName):
        os.remove(dataBaseName)
    SqliteDatabase(dataBaseName)
    initialization_data()


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
    print('='*82)
    print(f'You have {len(response)} tasks:\n')
    for task in response:
        print(
            f"Id: {task.id:<3} | Task: {task.task:<30} | State: {task.state.state:<8}")
    db.close()
    print('='*82)

# TODO:


def update_task():
    print('U'*82)
    print('Enter task ID to update:')
    taskIdToUpdate = int(input('-> '))
    db.connect()
    task = Task.select().where(Task.id == taskIdToUpdate).get()
    print('\nSelected task:')
    print(
        f'Task id: {task.id:<3} | Task name: {task.task:<30} | Task status: {task.state.state:<8}')

    print('\nWhat do you want to change ?')
    print('1 - Task name\n2 - Task status\n3 - Dead line')
    choiceUpdate = int(input('-> '))
    if choiceUpdate == 1:
        print('Eneter new task name')
        updateName = input('->')
        task.task = updateName
        print(f'Task name changed to: {updateName}')

    if choiceUpdate == 2:
        print('\nChose new state')
        response = TaskState.select()
        for state in response:
            print(f'{state.id} -> {state.state}')
        choseState = int(input('-> '))
        for _ in response:
            if _.id == choseState:
                print(_.state)
                task.state = TaskState.select().where(TaskState.state == _.state).get()
                print(f'Status changed to: {_.state}')

    if choiceUpdate == 3:
        pass

    task.save()
    db.close()
    print('U'*82)


def delete_task():
    print('Enter task ID to delete:')
    taskIdToDelete = int(input('-> '))
    db.connect()
    Task.select().where(Task.id == taskIdToDelete).get().delete_instance()
    db.close()


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

    if choice == 919:
        reset_database()
