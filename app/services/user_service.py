from app.models.user import User
from app.schemas.user_schema import user_schema
from app.utils.security import hash_password, check_password
from app.database import db

def create_user(data):
    data['password'] = hash_password(data['password'])
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user

def get_all_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None
    for key, value in data.items():
        if key == 'password':
            value = hash_password(value)
        setattr(user, key, value)
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def search_users(name):
    return User.query.filter(User.name.ilike(f"%{name}%")).all()

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password(password, user.password):
        return user
    return None
