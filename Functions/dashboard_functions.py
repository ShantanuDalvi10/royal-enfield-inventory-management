from models import db,Parts

def add_part(part_id,part_name,price,stock):
    part_id = part_id.strip()
    part_name = part_name.strip()

    if not part_id or not part_name:
        return False,"Please entered the required fields."

    if len(part_id) > 50 or len(part_name) > 100:
        return False, "Price or Part_ID cannot be too long."

    if stock < 0:
        return False,"Stock cannot be negative."

    if price < 0:
        return False, "Price cannot be negatve."

    existing_part = db.session.execute(
        db.select(Parts).filter(Parts.part_id==part_id)
    ).scalar_one_or_none()

    if existing_part:
        return False, "Part is already existed"

    new_part = Parts(
        part_id=part_id,
        part_name=part_name,
        price=price,
        stock=stock
    )

    try:
        db.session.add(new_part)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True, "New part added successfully."

def get_all_parts():
    return db.session.execute(
        db.select(Parts).order_by(Parts.id.asc())
    ).scalars().all()

def search_part(search_value):
    search_value = search_value.strip()

    if not search_value:
        return None

    part = db.session.execute(
        db.select(Parts).filter(Parts.part_id==search_value)
    ).scalar_one_or_none()

    if part is not None:
        return part

    part = db.session.execute(
        db.select(Parts).filter(Parts.part_name.ilike(f"%{search_value}%"))
    ).scalars().first()

    return part


def get_part_by_part_id(part_id):
    return  db.session.execute(
        db.select(Parts).filter(Parts.part_id==part_id)
    ).scalar_one_or_none()

def edit_part(old_part_id,new_part_id,part_name,price,stock):
    old_part_id=old_part_id.strip()
    new_part_id=new_part_id.strip()
    part_name=part_name.strip()

    if not old_part_id or not new_part_id or not part_name:
        return False,"All fiels are required."

    if len(new_part_id) > 50 or len(part_name) > 100:
        return False,"Part ID or Part Name is too long."

    if price < 0 or stock < 0:
        return False,"Negative values are not allowed."

    part = get_part_by_part_id(old_part_id)

    if part is None:
        return False,"Part is not found."

    existing_part = db.session.execute(
        db.select(Parts).filter(Parts.part_id==new_part_id,Parts.id != part.id)
    ).scalars().first()

    if existing_part:
        return False,f"Another part uses same part id : {new_part_id}"

    part.part_id = new_part_id
    part.part_name = part_name
    part.price = price
    part.stock = stock

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()

    return True,"Part is successfully edited."

def update_stock(part_id, new_stock):
    part = get_part_by_part_id(part_id=part_id.strip())

    if part is None:
        return False, "Part not found."

    if new_stock < 0:
        return False, "Stock cannot be negative"

    part.stock = new_stock

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True,"Stock updated successfully."

def delete_part(part_id):
    part = get_part_by_part_id(part_id=part_id.strip())

    if part is None:
        return False,"Part is not found."

    try:
        db.session.delete(part)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return True,"Part deleted successfully."


