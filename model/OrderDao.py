from model.ModelSqlite import db, Order

#TODO: Metodos semelhamentes, usar herança e generics

def save(order):
    db.session.add(order)
    db.session.commit()
    return order


def load(id: int):
    all = Order.query.filter(Order.id == id).all()
    return all[0] if len(all) > 0 else None

