from datetime import datetime, timedelta

from model.ModelSqlite import db, Order, Action, Task, TaskType


# TODO: Metodos semelhamentes, usar herança e generics

def save(order):
    db.session.add(order)
    db.session.commit()
    return order


def load(id: int):
    return Order.query.filter(Order.id == id).first()


def sumary(sumary_date: str):
    sumary_date = datetime.strptime(sumary_date, '%Y-%m-%d')
    finish = sumary_date + timedelta(hours=23, minutes=59, seconds=59)
    query = db.session.query(Task.id, Action, TaskType, Order) \
        .outerjoin(Action, Action.task_id == Task.id) \
        .join(TaskType, TaskType.id == Task.type_id) \
        .outerjoin(Order, Order.id == Task.order_id) \
        .filter(Action.init >= sumary_date, Action.finish <= finish)
    return query.all()


def load_form_export(sumary_date: str):
    sql = "SELECT t.id, tt.name,  a.description, o.number, date(init), " +\
          "sum(CAST ((julianday(a.finish) - julianday(a.init)) * 24 * 60 * 60 + 1 as INTEGER)) seconds " +\
          "FROM task t " +\
          "LEFT JOIN action a on a.task_id = t.id " +\
          "LEFT JOIN 'order' o on o.id = t.order_id " +\
          "INNER JOIN tasktype tt on tt.id = t.type_id " +\
          "WHERE date(init) = '" + sumary_date + "' GROUP BY t.id"

    connection = db.session.connection()
    query = connection.execute(sql)
    return query.all()
