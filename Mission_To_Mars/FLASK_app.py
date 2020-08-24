# Flask application to launch a dashboard of live web-scraped data stored in a MongoDB database
# Written by Jay Sueno

# Import modules including the python scrape code I developed - 'mission_to_mars'
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars 

# Create an instance of Flask
app = Flask(__name__)

# TEST Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
# mongo = PyMongo(app)

# Or set inline
# TEST Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():

    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    scraped_data = scrape_mars.scrape()
    mars_data.update({}, scraped_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)