from flask import Flask, request, jsonify
import Database
import GenHints
import atexit

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()  # Parse JSON input
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        database = Database.Database()


        if "get_hint" in data.keys():
            hints = database.getHint(data["get_hint"]["module"], data["get_hint"]["paper_no"], data["get_hint"]["question_no"])
            response = {"hints":hints}
        elif "register_user" in data.keys():
            database.addUser(data["register_user"]["user_name"], data["register_user"]["pw"])
            response={"message":"User added"}
        elif "authenticate" in data.keys():
            valid = database.authenticateUser(data["authenticate"]["user_name"], data["authenticate"]["pw"])
            response = {"valid":valid}
        else:
        # Example processing: Echoing back received data
            response = {"message": "Data received", "data": data}
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def closeDB():
    db.close()

if __name__ == '__main__':
    db = Database.Database()
    if not db.hintsInDatabase():
        GenHints.addHintsToDatabase(db)
    db.close()
    atexit.register(closeDB)
    app.run(debug=True)  # Runs on http://127.0.0.1:5000

