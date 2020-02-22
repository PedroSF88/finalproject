from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

import pandas as pd
from keras import backend as K


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/index.html")
def index():

    # Find one record of data from the mongo database
    mars_app = mongo.db.mars_app.find_one()

    # Return template and data
    return render_template("index.html", mars_app=mars_app)


# Route that will trigger the scrape function
@app.route("/prediction")
def dataframe():
    mars_app = mongo.db.mars_app
    prediction = scrape_mars.prediction()
    mars_app.update({},  prediction,upsert=True)
    K.clear_session()
    return redirect("/index.html", code=302)


@app.route("/data.html")
def data():
    """Return the homepnameGiven."""
    return render_template("/data.html")

@app.route("/code.html")
def code():
    """Return the homepnameGiven."""
    return render_template("/code.html")

@app.route("/contributors.html")
def contributors():
    """Return the homepnameGiven."""
    return render_template("/contributors.html")

@app.route("/exploratory.html")
def exploratory():
    """Return the homepnameGiven."""
    return render_template("/exploratory.html")

@app.route("/home.html")
def home():
    """Return the homepnameGiven."""
    return render_template("home.html")

@app.route("/")
def home1():
    """Return the homepnameGiven."""
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
