from flask import Flask, request, jsonify

app = Flask(__name__)

data = []

@app.route('/get', methods=['GET'])
def get_data():
    return {"data": data}

# Home route
@app.route("/")
def home():
    return "Finance Tracker API Running"

# Add Transaction API
@app.route("/add", methods=["POST"])
def add_transaction():
    new_data = request.json   # 👈 name change

    amount = new_data.get("amount")
    t_type = new_data.get("type")
    category = new_data.get("category")

    # Validation
    if not amount or not t_type:
        return jsonify({"error": "Amount and type required"}), 400

    data.append(new_data)   # 👈 MOST IMPORTANT LINE

    return jsonify({
        "message": "Transaction added successfully",
        "data": new_data
    })

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_data(index):
    if index < 0 or index >= len(data):
        return {"error": "Invalid index"}, 400

    deleted = data.pop(index)

    return {
        "message": "Deleted successfully",
        "data": deleted
    }

@app.route('/update/<int:index>', methods=['PUT'])
def update_data(index):
    if index < 0 or index >= len(data):
        return {"error": "Invalid index"}, 400

    new_data = request.json
    data[index] = new_data

    return {
        "message": "Updated successfully",
        "data": new_data
    }

@app.route('/summary', methods=['GET'])
def get_summary():
    total_income = 0
    total_expense = 0

    for item in data:
        if item.get("type") == "income":
            total_income += item.get("amount", 0)
        elif item.get("type") == "expense":
            total_expense += item.get("amount", 0)

    balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance
    }

@app.route('/filter/<string:type>', methods=['GET'])
def filter_data(type):
    filtered = []

    for item in data:
        if item.get("type") == type:
            filtered.append(item)

    return {"data": filtered}


if __name__ == "__main__":
    app.run(debug=False)

