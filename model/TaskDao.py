from model.ModelSqlite import db, Task


def save(task):
    db.session.add(task)
    db.session.commit()
    return task


def load():
    return Task.query.all()


def load_by_id(id: int):
    all = Task.query.filter(Task.id == id).all()
    return all[0] if len(all) > 0 else None
