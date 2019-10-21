# Import dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars
import os


# Create an instance file
app = Flask(__name__)

# Use flask_pymongo to set up connection 
#app.config["MONGO_URI"]= os.environ.get('authentication')
#mongo = PyMongo(app)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index html 
@app.route("/")
def home():

    #Find data
    mars_info = mongo.db.scrape_mars_info.find_one()
    print(mars_info.keys())

    # Return template and data
    return render_template("index.html", mars_info=mars_info)

# Route that will trigger the scrape function 
@app.route("/scrape")
def scrape():
    # Run scraped functions
    mars_info = mongo.db.scrape_mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/") 

if __name__ == "__main__":
    app.run(debug=True)

