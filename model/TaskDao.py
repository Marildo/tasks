from model.ModelSqlite import db, Task, Action, Order, TaskType
from sqlalchemy import and_, func



def save(task):
    db.session.add(task)
    db.session.commit()
    return task


def load_by_date(sumary_date):
    query = db.session.query(Task, Action, TaskType, Order) \
        .join(Action, Action.task_id == Task.id) \
        .join(TaskType, TaskType.id == Task.type_id) \
        .outerjoin(Order, Order.id == Task.order_id) \
        .filter(Action.init >= sumary_date)\
        .group_by(Task.id)
    return query.all()


def load_by_search(search):
    filters = [Order.number == search] if search.isnumeric() else [TaskType.name == search]
    query = db.session.query(Task, Action, TaskType, Order) \
        .join(Action, Action.task_id == Task.id) \
        .join(TaskType, TaskType.id == Task.type_id) \
        .outerjoin(Order, Order.id == Task.order_id) \
        .filter(and_(*filters)).group_by(Task.id)\
        .group_by(Task.id)
    return query.all()


def load_by_id(id: int):
    return Task.query.filter(Task.id == id).first()


def set_order(order):
    db.session.query(Task).filter(Task.id == order.task_id).update({"order_id": order.id})
    db.session.commit()
