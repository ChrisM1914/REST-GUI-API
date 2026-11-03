# api.py
from flask import Flask, request, jsonify
 
app = Flask(__name__)
 
REQUIRED_FIELDS = ["product_id", "description", "price", "name", "email"]
 
 
@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
 
    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    name = str(data["name"]).strip()
    if len(name) < 5 or not name.replace(" ", "").isalpha():
        return jsonify({"error": "Name must be at least 5 characters and letters only"}), 400
 
    # Server-side check of the price rule (never trust the client alone)
    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number"}), 400
    if price <= 0 or price > 1000.00:
        return jsonify({"error": "Price must be greater than 0 and no more than 1000.00"}), 400
 
    print("Received purchase:", data)  # prints to the console where the API runs
    return jsonify({"status": "ok", "received": data}), 200
 
 
if __name__ == "__main__":
    app.run(port=5000, debug=True)