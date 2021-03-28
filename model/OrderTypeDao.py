from model.ModelSqlite import db, OrderType


def save(order_type):
    db.session.add(order_type)
    db.session.commit()
    return order_type


def load():
    return OrderType.query.all()

