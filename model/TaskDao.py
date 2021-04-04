from sqlalchemy.sql.expression import update

from model.ModelSqlite import db, Task


def save(task):
    db.session.add(task)
    db.session.commit()
    return task


def load():
    return Task.query.all()


def load_by_id(id: int):
    return Task.query.filter(Task.id == id).first()


def set_order(order):
    db.session.query(Task).filter(Task.id == order.task_id).update({"order_id": order.id})
    db.session.commit()
