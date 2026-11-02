from models import db,User
from werkzeug.security import generate_password_hash,check_password_hash

def register_user(username,password,registration_pin,correct_pin):
    username = username.strip()

    if not username or not password or not registration_pin:
        return ValueError("All Fields are required.")

    if not correct_pin:
        raise RuntimeError("Registration PIN is not configured.")

    if registration_pin != correct_pin:
        raise ValueError("Invalid Registration PIN.")

    existing_user = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if existing_user:
        raise ValueError("Username already exists.")

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



def authenticate_user(username,password):
    username = username.strip()

    if not username or not password:
        raise ValueError("Please complete the required fields.")

    user = db.session.execute(
        db.select(User).filter(User.username == username)
    ).scalar_one_or_none()

    if not user:
        return None

    if not check_password_hash(user.password,password):
        raise ValueError("Incorrect username or password.")


    return user
