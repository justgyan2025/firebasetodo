from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Firebase configuration
service_account_key_path = os.environ.get("SERVICE_ACCOUNT_KEY_PATH")
cred = credentials.Certificate(service_account_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestore collection
todos_collection = db.collection("todos")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        todo = request.form.get("todo")
        todos_collection.add({"task": todo, "completed": False})
        return redirect(url_for("index"))

    todos = []
    for doc in todos_collection.stream():
        todo = doc.to_dict()
        todo["id"] = doc.id
        todos.append(todo)
    return render_template("index.html", todos=todos)

@app.route("/delete/<id>")
def delete(id):
    todos_collection.document(id).delete()
    return redirect(url_for("index"))

@app.route("/update/<id>", methods=["POST"])
def update(id):
    completed = request.form.get("completed") == "on"
    todos_collection.document(id).update({"completed": completed})
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=False)
