from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User
from .services import UserService
from extensions import db


users_bp = Blueprint("users", __name__, url_prefix="/api/users")
service = UserService()


@users_bp.route("/signUp", methods=["POST"])
def sign_up():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 409

    try:
        new_user = service.create_user(
            email=data["email"], password=data["password"]
        )

        return (
            jsonify(
                {
                    "id": new_user.id,
                    "email": new_user.email,
                }
            ),
            201,
        )

    except Exception as e:
        print(e)
        return jsonify({"message": str("Something wrong happened")}), 500


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return (
        jsonify(
            {
                "access_token": access_token,
                "user_id": user.id,
            }
        ),
        200,
    )


@users_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get authenticated user's profile"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(
        {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at.isoformat() if user.created_at else None,
        }
    )


@users_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    """Update authenticated user's profile (email or password)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    if "email" in data:
        if User.query.filter(
            User.id != current_user_id, User.email == data["email"]
        ).first():
            return jsonify({"message": "Email already in use"}), 409
        user.email = data["email"]

    if "password" in data:
        if not data.get("current_password"):
            return (
                jsonify({"message": "Current password required to change password"}),
                400,
            )

        if not user.check_password(data["current_password"]):
            return jsonify({"message": "Current password is incorrect"}), 401
        user.set_password(data["password"])

    try:
        db.session.commit()
        return jsonify(
            {
                "id": user.id,
                "email": user.email,
                "message": "Profile updated successfully",
            }
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500
