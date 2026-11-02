from models import db,Parts
from services.validators import validate_price_and_stock

def add_part(part_id,part_name,price,stock):
    part_id = part_id.strip()
    part_name = part_name.strip()

    if not part_id or not part_name:
        raise ValueError("Please enter all required fields.")

    if len(part_id) > 50 or len(part_name) > 100:
        raise ValueError("Part ID or Part Name is too long.")

    price, stock = validate_price_and_stock(price, stock)

    existing_part = db.session.execute(
        db.select(Parts).filter(Parts.part_id==part_id)
    ).scalar_one_or_none()

    if existing_part:
        raise ValueError("Part already exists.")

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



def get_all_parts(page=1,per_page=10):
    return db.paginate(
        db.select(Parts).order_by(Parts.id.asc()),
        page=page,
        per_page=per_page,
        error_out=False
    )

def search_part(search_value,page=1,per_page=10):
    search_value = search_value.strip()

    if not search_value:
        return None

    query = db.select(Parts).filter(
        db.or_(
            Parts.part_id == search_value,
            Parts.part_name.ilike(f"%{search_value}%")
        )
    ).order_by(Parts.id.asc())

    return db.paginate(
        query,
        page=page,
        per_page=per_page,
        error_out=False
    )


def get_part_by_part_id(part_id):
    return  db.session.execute(
        db.select(Parts).filter(Parts.part_id==part_id)
    ).scalar_one_or_none()

def edit_part(old_part_id,new_part_id,part_name,price,stock):
    old_part_id=old_part_id.strip()
    new_part_id=new_part_id.strip()
    part_name=part_name.strip()

    if not old_part_id or not new_part_id or not part_name:
        raise ValueError("All fields are required.")

    if len(new_part_id) > 50 or len(part_name) > 100:
        raise ValueError("Part ID or Part Name is too long.")

    price, stock = validate_price_and_stock(price, stock)

    part = get_part_by_part_id(old_part_id)

    if part is None:
        raise ValueError("Part is not found.")

    existing_part = db.session.execute(
        db.select(Parts).filter(Parts.part_id==new_part_id,Parts.id != part.id)
    ).scalars().first()

    if existing_part:
        raise ValueError(f"Another part uses the same Part ID: {new_part_id}")

    part.part_id = new_part_id
    part.part_name = part_name
    part.price = price
    part.stock = stock

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise


def update_stock(part_id, new_stock):
    part = get_part_by_part_id(part_id=part_id.strip())

    if part is None:
        raise ValueError("Part not found.")

    _, new_stock = validate_price_and_stock(stock=new_stock)

    part.stock = new_stock

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise



def delete_part(part_id):
    part = get_part_by_part_id(part_id=part_id.strip())

    if part is None:
        raise ValueError("Part is not found.")

    try:
        db.session.delete(part)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise



