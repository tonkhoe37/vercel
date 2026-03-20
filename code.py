from flask import Flask, jsonify, request
from flasgger import Swagger
import yaml
import os

app = Flask(__name__)

# Load OpenAPI YAML
try:
    with open("openapi.yaml", "r", encoding="utf-8") as f:
        template = yaml.safe_load(f)
except Exception as e:
    print("Error loading OpenAPI:", e)
    template = {}

swagger = Swagger(app, template=template)

# Fake database
books = [
    {"id": "1", "title": "Clean Code", "author": "Robert C. Martin", "price": 30},
    {"id": "2", "title": "Atomic Habits", "author": "James Clear", "price": 25},
]


@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(books)


@app.route("/api/books/<id>", methods=["GET"])
def get_book(id):
    for b in books:
        if b["id"] == id:
            return jsonify(b)
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.json:
        return jsonify({"error": "Invalid input"}), 400

    data = request.json
    books.append(data)
    return jsonify(data), 201


@app.route("/api/books/<id>", methods=["PUT"])
def update_book(id):
    if not request.json:
        return jsonify({"error": "Invalid input"}), 400

    for b in books:
        if b["id"] == id:
            data = request.json
            b.update(data)
            return jsonify(b)
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books/<id>", methods=["DELETE"])
def delete_book(id):
    global books
    books = [b for b in books if b["id"] != id]
    return jsonify({"message": "Book deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
