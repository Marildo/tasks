from model.ModelSqlite import db, TaskType


def save(type_type):
    db.session.add(type_type)
    db.session.commit()
    return type_type


def load():
    return TaskType.query.all()

