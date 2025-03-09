from flask import Flask, request, jsonify
from flask_cors import CORS
import Database
import GenHints
import atexit

app = Flask(__name__)
CORS(app) #nb if we get cors-related errors after this disable this
app.config['UPLOAD FOLDER'] = "Back end/Uploads"

@app.route('/process', methods=['POST'])
def process_data():
    try:
        data = request.get_json()  # Parse JSON input
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        
        database = Database.Database()

        if "get_hint" in data.keys():
            hint, hintID = database.getHint(data["get_hint"]["module"], data["get_hint"]["paper_no"], data["get_hint"]["question_no"], data["get_hint"]["hint_no"])
            database.addStudentHint(data["get_hint"]["user_name"], hintID)
            response = {"hint":hint}
        elif "register_user" in data.keys():
            database.addUser(data["register_user"]["user_name"], data["register_user"]["pw"], data["register_user"]["role"])
            response={"valid":True, "role":data["register_user"]["role"]}
        elif "authenticate" in data.keys():
            valid, role = database.authenticateUser(data["authenticate"]["user_name"], data["authenticate"]["pw"])
            response = {"valid":valid, "role":role}
        elif "user_seen_hint" in data.keys():
            seen, hintText = database.userSeenHint(data["user_seen_hint"]["user_name"], data["user_seen_hint"]["module"], data["user_seen_hint"]["paper_no"], data["user_seen_hint"]["question_no"], data["user_seen_hint"]["hint_no"])
            response = {"seen_hint":seen, "hint":hintText}
        elif "get_num_questions" in data.keys():
            numQuestions = database.getNumQuestions()
            response = {"num_questions":numQuestions}
        else:
        # Example processing: Echoing back received data
            response = {"message": "Data received", "data": data}
        return jsonify(response)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route('/file_upload', methods=['POST'])
def file_upload():
    try:
        image = request.files['file']
        filename = app.config['UPLOAD FOLDER']+"/"+image.filename
        image.save(filename)
        ExPPath = GenHints.getExPPath(request.headers["X-Module"], request.headers["X-Paper-No"])
        hint = GenHints.genCustomHint(ExPPath, filename, request.headers["X-Question-No"])
        return hint
        
    except Exception as e:
        print(e)
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

