from model.ModelSqlite import db, TypeOrder


def save(typeOrder):
    db.session.add(typeOrder)
    db.session.commit()
    return typeOrder

def load():
    return TypeOrder.query.all()

