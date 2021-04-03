from model.ModelSqlite import db, Order, Action, Task, TaskType
from datetime import datetime, timedelta


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
