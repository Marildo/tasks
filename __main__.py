# http://turing.com.br/material/flask/index.html
# https://demos.creative-tim.com/material-dashboard-dark/docs/2.0/components/card.html
# https://www3.ntu.edu.sg/home/ehchua/programming/webprogramming/Python3_Flask.html
# https://fonts.google.com/icons?selected=Material+Icons:add_circle_outline&icon.query=down

from csv import writer
from datetime import datetime, timedelta

import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, abort

import model.ActionDao as actionDao
import model.OrderDao as orderDao
import model.TaskDao as taskDao
import model.TaskTypeDao as taskTypeDao
from model.ModelSqlite import ModelSQLITE, Task, TaskType, Order, Action

app = Flask('VoooHelp', static_folder='static', template_folder='template')


def locate_html(page: str) -> str:
    return f'pages/{page}.html'
    # TODO : Testar se arquivo existe


def load_task_types():
    task_types = taskTypeDao.load()

    def set_selected(item):
        item.selected = item.name == 'N3'
        return item

    return list(map(set_selected, task_types))


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


@app.route('/settings/')
def settings():
    task_types = taskTypeDao.load()
    return render_template(locate_html('settings'), task_types=task_types)


@app.route('/tasks/', methods=['GET', 'POST'])
def tasks():
    try:
        sumary_date = datetime.now().strftime('%Y-%m-%d') \
            if request.method == 'GET' else request.form['sumary_date']

        search = request.form['search'] if 'search' in request.form else None
        if search:
            tasks = taskDao.load_by_search(search)
        else:
            tasks = taskDao.load_by_date(sumary_date)

        for task in tasks:
            actions = task.Action.Task.actions
            task.Task.running = any([not action.finished for action in actions])

        sumary = orderDao.sumary(sumary_date)
        task_types = load_task_types()
        return render_template(locate_html('tasks'), tasks=tasks, task_types=task_types, sumary=sumary,
                               sumary_date=sumary_date)
    except Exception as e:
        abort(500, description=e)


@app.route('/addtask/', methods=['POST'])
def add_task():
    task = Task()
    task.type_id = request.form['type']
    taskDao.save(task)
    return redirect(url_for('task', id=task.id, ))


@app.route('/addTypeTask/', methods=['POST'])
def addTypeTask():
    task_type = TaskType(request.form['name'])
    taskTypeDao.save(task_type)
    return redirect(url_for('settings'))


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


@app.route('/finalize/', methods=['POST'])
def finalize_action():
    form = request.form
    task_id = form['taskId']
    finish = datetime.strptime(form['finish'].replace('T', ' '), '%Y-%m-%d %H:%M')

    action = actionDao.load_running(task_id)
    action.finish = finish
    action.finished = True
    action.description = action.description + '\n' + form['description']
    actionDao.save(action)

    return redirect(url_for('task', id=action.task_id))


@app.route('/exportCSV/', methods=['POST'])
def export_csv():
    sumary_date = request.form['sumary_date']
    sumary = orderDao.load_form_export(sumary_date)

    week_days = ('domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado')
    months = (
    'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro',
    'dezembro')

    date = datetime.strptime(sumary_date, '%Y-%m-%d')
    filename = f"day-{datetime.strftime(date, '%d-%m-%Y')}.csv"

    with open(filename, 'w', encoding='utf-8', newline='') as file:
        pointer = writer(file)
        total_hours = datetime(year=1, month=1, day=1)
        for task_id, type, description, number, init, seconds in sumary:
            date = datetime.strptime(init, '%Y-%m-%d')
            week_day = datetime.strftime(date, '%w')
            week_day = week_days[int(week_day)]
            month_day = datetime.strftime(date, '%d')
            month = datetime.strftime(date, '%m')
            month = months[int(month) - 1]
            year = datetime.strftime(date, '%Y')

            flag = seconds % 60
            flag = 60 - flag
            hours = datetime(year=1, month=1, day=1) + timedelta(seconds=seconds + flag)
            total_hours = total_hours + timedelta(seconds=seconds)

            if type == 'N3':
                activity = f'N3 Id: {number}'
            else:
                activity = f'{type} {description}'

            day = f'{week_day}, {month_day} de {month} de {year}'
            hours = datetime.strftime(hours, '%H:%M:%S')
            pointer.writerow([day, activity, hours])

        total_hours = datetime.strftime(total_hours, '%H:%M:%S')
        pointer.writerow(['', 'Total', total_hours])

    return redirect(url_for('tasks', sumary_date=sumary_date), code=307)


@app.errorhandler(404)
def page_not_found(e):
    return render_template(locate_html('error'), msg='Pagina não encontrada'), 404  # Not Found


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(locate_html('error'), msg=e), 500  # Internal Server Error


if __name__ == '__main__':
    modelSqlite = ModelSQLITE(app)
    modelSqlite.connect()
    app.run(debug=True, port=3000)
