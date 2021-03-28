from model.ModelSqlite import db, Task


def save(task):
    db.session.add(task)
    db.session.commit()
    return task


def load():
    return Task.query.all()

