from flask import Blueprint, request, jsonify
from app.schemas.user_schema import user_schema, users_schema
from app.services import user_service

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users", methods=["GET"])
def get_users():
    users = user_service.get_all_users()
    return users_schema.dump(users), 200

@user_bp.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404
    return user_schema.dump(user), 200

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    errors = user_schema.validate(data)
    if errors:
        return {"errors": errors}, 400
    user = user_service.create_user(data)
    return user_schema.dump(user), 201

@user_bp.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = user_service.update_user(user_id, data)
    if not user:
        return {"error": "User not found"}, 404
    return user_schema.dump(user), 200

@user_bp.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    return ({}, 204) if success else ({"error": "User not found"}, 404)

@user_bp.route("/search")
def search():
    name = request.args.get("name")
    users = user_service.search_users(name)
    return users_schema.dump(users), 200

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = user_service.login_user(data["email"], data["password"])
    if not user:
        return {"error": "Invalid credentials"}, 401
    return user_schema.dump(user), 200
