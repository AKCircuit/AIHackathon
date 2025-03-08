from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()  # Parse JSON input
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        # Example processing: Echoing back received data
        response = {"message": "Data received", "data": data}
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Runs on http://127.0.0.1:5000