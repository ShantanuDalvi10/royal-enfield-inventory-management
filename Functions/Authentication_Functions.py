from models import db,User
from werkzeug.security import generate_password_hash,check_password_hash

def register_user(username,password,registration_pin,correct_pin):
    username = username.strip()

    if not username or not password or not registration_pin:
        return False, "All fields are required."

    if not correct_pin:
        return False, "Problem in configuration."

    if registration_pin != correct_pin:
        return False , "Invalid Registration Pin"

    existing_user = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if existing_user:
        return False, "User is already existed."

    hash_password = generate_password_hash(password)

    new_user = User(
        username=username,
        password=hash_password
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return True, "Registration is Successsful"

def authenticate_user(username,password):
    username = username.strip()

    user = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if not user:
        return None

    if not check_password_hash(user.password,password):
        return None

    return user
