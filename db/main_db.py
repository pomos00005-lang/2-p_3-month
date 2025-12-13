import sqlite3
from config import path_db
from db import queries

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TASKS)
    print("База данных подключена!!!")
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.INSERT_TASKS, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def get_tasks():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.SELECT_TASKS)
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id , new_task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.UPDATE_TASKS, (new_task, task_id))
    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASKS, (task_id,))
    conn.commit()
    conn.close()