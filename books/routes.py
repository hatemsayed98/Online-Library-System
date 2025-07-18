from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from books.validations import BookQuerySchema
from .services import BookService

books_bp = Blueprint("books", __name__, url_prefix="/api/books")
service = BookService()


@books_bp.route("", methods=["GET"])
def get_books_simple():
    schema = BookQuerySchema()

    try:
        params = schema.load(request.args)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    page = params.pop("page")
    size = params.pop("size")
    filters = {k: v for k, v in params.items() if v is not None}

    result = service.get_all_books(page=page, per_page=size, filters=filters)
    
    return jsonify(result)



@books_bp.route("", methods=["POST"])
@jwt_required()
def create_book():
    data = request.get_json()
    book = service.create_book(data)
    return jsonify(book.to_dict()), 201


@books_bp.route("/<int:id>", methods=["GET"])
def get_book(id):
    book = service.get_book_by_id(id)
    if book:
        return jsonify(book.to_dict())
    return jsonify({"message": "Not found"}), 404


@books_bp.route("/<int:book_id>", methods=["PATCH"])
@jwt_required()
def update_book(book_id):
    data = request.get_json()

    try:
        updated_book = service.update_book(book_id, data)
        if not updated_book:
            return jsonify({"message": "Not found"}), 404

        return jsonify(updated_book.to_dict())
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": str("Something wrong happened")}), 500


@books_bp.route("/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    try:
        success = service.delete_book(book_id)
        if not success:
            return jsonify({"message": "Not found"}), 404

        return "", 204
    except Exception as e:
        print(e)
        return jsonify({"message": str("Something wrong happened")}), 500
