from model.ModelSqlite import db, Action

#TODO: Metodos semelhamentes, usar herança e generics

def save(action):
    db.session.add(action)
    db.session.commit()
    return action


def load(id: int):
    all = Action.query.filter(Action.id == id).all()
    return all[0] if len(all) > 0 else None

