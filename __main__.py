# http://turing.com.br/material/flask/index.html

from flask import Flask, jsonify, render_template, redirect, url_for, request
from model.ModelSqlite import ModelSQLITE, Task, TaskType
import model.TaskDao as taskDao
import model.TaskTypeDao as taskTypeDao
import mysql.connector

"""
host='mysql.vooo.ws',
user='root',
password='te4356sfh',
database='vooo_prod_backend'
"""


class DAO:
    def load_clients(self):
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='si411225',
            database='vooo_homolog_backend'
        )

        cursor = conn.cursor()
        cursor.execute('Select id, name, trading, economic_group_id, headquarter_id, status from client')
        result =  cursor.fetchall()
        cursor.close()
        return result


def locate_html(page:str) -> str:
    return f'pages/{page}.html'
    # TODO : Testar se arquivo existe


app = Flask('VoooHelp', static_folder='static', template_folder='template')

@app.route('/')
def index():
    #return jsonify(msg='Server is running', data=datetime.now())
    return render_template(locate_html('index'))


@app.route('/dashboard/')
def dashboard():
    return render_template(locate_html('dashboard'))    


@app.route('/clientes/')
def clients():
    dao = DAO()
    query = dao.load_clients()
    return render_template(locate_html('clients'), clients=query)


@app.route('/conectores/')
def connectors():
    return render_template(locate_html('connectors'))


@app.route('/tasks/')
def tasks():
    task_types = taskTypeDao.load()

    def set_selected(item):
        item.selected = item.name == 'N3'
        return item

    task_types = list(map(set_selected, task_types))

    tasks = taskDao.load() 
    return render_template(locate_html('tasks'), tasks=tasks, task_types=task_types)


@app.route('/tasks/', methods=['POST'])
def addTask():
    task = Task()
    task.name = request.form['type']
    taskDao.save(task)
    return redirect(url_for('tasks'))


@app.route('/addTypeOrder/', methods=['POST'])    
def addTypeOrder():
    task_type = TaskType(request.form['name'])
    taskTypeDao.save(task_type)
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    modelSqlite = ModelSQLITE(app)
    modelSqlite.connect()
    app.run(debug=True, port=3000)


