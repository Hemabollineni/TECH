from flask import Flask, request, jsonify

from lib.db import (
    initialize_db,
    add_item,
    get_all_items,
    get_item,
    update_item,
    delete_item
)

app = Flask(__name__)


# Create the table when the server starts
initialize_db()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "REST API is running",
        "endpoints": {
            "add_item": "POST /items",
            "get_all_items": "GET /items",
            "get_one_item": "GET /items/<item_id>",
            "update_item": "PUT /items/<item_id>",
            "delete_item": "DELETE /items/<item_id>"
        }
    }), 200


@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    name = data.get("name")
    description = data.get("description", "")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "A non-empty name is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be a string"}), 400

    item = add_item(name.strip(), description)

    return jsonify({
        "message": "Item created successfully",
        "item": item
    }), 201


@app.route("/items", methods=["GET"])
def list_items():
    items = get_all_items()

    return jsonify({
        "count": len(items),
        "items": items
    }), 200


@app.route("/items/<int:item_id>", methods=["GET"])
def retrieve_item(item_id):
    item = get_item(item_id)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item), 200


@app.route("/items/<int:item_id>", methods=["PUT"])
def replace_item(item_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    name = data.get("name")
    description = data.get("description")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "A non-empty name is required"}), 400

    if not isinstance(description, str):
        return jsonify({
            "error": "Description must be a string"
        }), 400

    item = update_item(
        item_id,
        name.strip(),
        description
    )

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({
        "message": "Item updated successfully",
        "item": item
    }), 200


@app.route("/items/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):
    deleted = delete_item(item_id)

    if not deleted:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({
        "message": "Item deleted successfully",
        "item_id": item_id
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
