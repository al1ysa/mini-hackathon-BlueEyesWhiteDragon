from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json  # Get data from the request
        # Process data here (e.g., save to database)
        return jsonify({"message": "Data received!", "data": data}), 201
    else:
        return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
