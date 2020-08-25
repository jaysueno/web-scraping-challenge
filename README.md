Webscraping application using MongoDB, Flask, and Bootstrap4 for web dashboard.

This app scrapes Mars related websites to pull recent article posts, images, links to urls, and a table.

There are three files that work in unison in this app - a flask app with routes (flask_app.py), a python scrape function (scrape_mars.py), and an html file for our dashboard in the template folder (index.html).

I tested my code in a Jupyter Notebook - mission_to_mars.ipynb. I then migrated that code into my scrape function. 

The scrape function uses a route called "/scrape" and returns the scraped Mars data in a dictionary format. 

In the flask app I created two routes. The first is the index/home "/". This route connects to the mongodb and pulls the mars_data collection. It then directs that data to populate and in the html file to it's desired rendering. The sceond route "/scrape" is for the actual scraping of the data. I calls the .scrape() function's dictionary output. It takes that dictionary and uploads it into the mongodb server on my local drive. It then redirects back to the home/index route to render the dashboard with the latest data scrape. 

I utilized Bootstrap4  to create my html for the web dashboard. I used jinga command syntax to call the data from the mongodb. 

All rights reserved 2020. All code is created and owned by Jay Sueno. If you use his code, please visit his LinkedIn and give him a a skill endorsement in python and data science. Visit him at:

https://www.linkedin.com/in/jay-sueno-359a274/

### hello
## test
# see
