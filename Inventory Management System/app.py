from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
from datetime import datetime
import os
import pandas as pd

app = Flask(__name__)

MONGO_URI = "--------------Add database  link--------------------------------"
client = MongoClient(MONGO_URI)

db = client["arshdb"]
collection = db["inventory"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_item', methods=['POST'])
def add_item():
    data = {
        "name": request.form['name'],
        "price": float(request.form['price']),
        "expiry": request.form.get('expiry', ''),
        "in_stock": "Yes" if request.form.get('in_stock') == 'on' else "No",
        "date_added": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    collection.insert_one(data)
    return jsonify({"success": True, "message": "Item added successfully!"})

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = []
    for item in collection.find():
        if query in item["name"].lower():
            item["_id"] = str(item["_id"])
            results.append(item)
    return jsonify(results)

@app.route('/download')
def download():
    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    file_path = "inventory_export.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
