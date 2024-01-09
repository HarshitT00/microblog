import datetime
import os
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()
def create_app():
    app = Flask(__name__)
    uri = os.getenv("MONGODB_URI")
    client = MongoClient(uri)
    app.db = client.microblog

    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date1 = datetime.datetime.today().strftime("%Y-%m-%d")
            formatted_date2 = datetime.datetime.today().strftime("%b-%d")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date1, "show_date": formatted_date2})
        entries = [
            (
                entry["content"],
                entry["date"],
                entry["show_date"]
            )
            for entry in app.db.entries.find()
        ]
        return render_template("index.html", entries=entries)
    return app