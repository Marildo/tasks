# http://turing.com.br/material/flask/index.html
# https://www3.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html

from datetime import datetime

import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, abort

import model.ActionDao as actionDao
import model.OrderDao as orderDao
import model.TaskDao as taskDao
import model.TaskTypeDao as taskTypeDao
from model.ModelSqlite import ModelSQLITE, Task, TaskType, Order, Action

"""
host='mysql.vooo.ws',
user='root',
password='te4356sfh',
database='vooo_prod_backend'
"""


# TODO: Melhorar a forma de identificar tipos de tarefas
# TODO: Adicionar um decorator para tratar exception

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
        result = cursor.fetchall()
        cursor.close()
        return result


def locate_html(page: str) -> str:
    return f'pages/{page}.html'
    # TODO : Testar se arquivo existe


app = Flask('VoooHelp', static_folder='static', template_folder='template')


@app.route('/')
def index():
    # return jsonify(msg='Server is running', data=datetime.now())
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
    try:
        fd = 2
        fd.uper()
        task_types = taskTypeDao.load()

        def set_selected(item):
            item.selected = item.name == 'N3'
            return item

        task_types = list(map(set_selected, task_types))

        tasks = taskDao.load()
        return render_template(locate_html('tasks'), tasks=tasks, task_types=task_types)
    except Exception as e:
        abort(500, description=e)


@app.route('/tasks/', methods=['POST'])
def add_task():
    task = Task()
    task.type_id = request.form['type']
    task = taskDao.save(task)
    return redirect(url_for('task', id=task.id))


@app.route('/addTypeTask/', methods=['POST'])
def addTypeTask():
    task_type = TaskType(request.form['name'])
    taskTypeDao.save(task_type)
    return redirect(url_for('tasks'))


@app.route('/task/<int:id>')
def task(id: int):
    task = taskDao.load_by_id(id)
    if not task:
        return render_template(locate_html('error'), msg='Tarefa não encontrada')

    is_n3 = task.task_type.name == "N3"
    task.running = any([not action.finished for action in task.actions])
    return render_template(locate_html('task'), task=task, isN3=is_n3)


@app.route('/addOrder/', methods=['POST'])
def add_order():
    form = request.form
    order = Order()
    order.number = form['orderNumber']
    order.client_id = form['clientId']
    order.client_name = form['clientName']
    order.aggregator = form['aggregator']
    order.task_id = form['taskId']
    orderDao.save(order)
    taskDao.set_order(order)
    return redirect(url_for('task', id=order.task_id))


@app.route('/addAction/', methods=['POST'])
def add_action():
    form = request.form
    action = Action()
    action.task_id = form['taskId']
    action.description = form['description']
    action.init = datetime.strptime(form['init'].replace('T', ' '), '%Y-%m-%d %H:%M')
    actionDao.save(action)
    return redirect(url_for('task', id=action.task_id))


@app.route('/finalize/<int:id>')
def finalize_action(id):
    action = actionDao.load_running(id)
    action.finish = datetime.now()
    action.finished = True
    actionDao.save(action)
    return redirect(url_for('task', id=action.task_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template(locate_html('error'), msg='Pagina não encontrada'), 404  # Not Found


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(locate_html('error'), msg = e), 500  # Internal Server Error


if __name__ == '__main__':
    modelSqlite = ModelSQLITE(app)
    modelSqlite.connect()
    app.run(debug=True, port=3000)
