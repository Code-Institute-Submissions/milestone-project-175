import os
from flask import (
    Flask, flash, render_template,
    redirect, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_categories")
def get_categories():
    categories = mongo.db.categories.find()
    recommendations = list(
        mongo.db.recommendations.find().sort("recommend_date", -1))
    return render_template(
        "index.html", categories=categories, recommendations=recommendations)


@app.route("/view_recommendation/<recommendation_id>")
def view_recommendation(recommendation_id):
    recommendation = mongo.db.recommendations.find_one(
            {"_id": ObjectId(recommendation_id)})
    return render_template(
            "recommendation.html", recommendation=recommendation)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")), debug=True)