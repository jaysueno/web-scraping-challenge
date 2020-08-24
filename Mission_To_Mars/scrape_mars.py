# Application to run a web scrape of Mission to Mars Data
# Written by Jay Sueno

# Import all the needed python modules
import pandas as pd
import os
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import datetime as dt

# Create a function to initialize the webscraping browser with splinter 
def init_browser():
    # Establish chrome driver executable path. Make sure to define actual location on your drive.
    executable_path ={'executable_path': 'C:/Users/jaysu/chromedriver.exe'}
    # Open a splinter browser
    return Browser('chrome', **executable_path, headless=False)

# Create a callable function to scrape the data from the website    
def scrape(): 
### Initialize splitner broswer ###
    browser = init_browser()

### NASA Mars News ###
    # Define the the URL
    url = 'https://mars.nasa.gov/news'
    # Visit the defined URL on your splinter broswers
    browser.visit(url)

    # Give the broswer time to load 
    time.sleep(3)
    # Create a BeautifulSoup object with the splinter broswer.html object and parse the html with 'html.parser' or 'lxml'
    soup = bs(browser.html, 'html.parser')

    # Scrape the first instance of latest news title text and assign to a variable
    # Find the first article
    first_news_article = soup.find('li', class_="slide")
    # Find the title within that article summary and convert into .text or .get_text() and then .strip() of '/n'
    news_title = first_news_article.find('div', class_='content_title').text.strip()

    # Scrape the first instance of latest paragraph text and assign to a variable
    # Find the paragraph within that article summary and convert into .text and then .strip() of '/n'
    news_p = first_news_article.find('div', class_="article_teaser_body").text.strip()

    # Save the article link url
    article_link_string = first_news_article.find('a')['href']
    article_url = url + article_link_string

    print('Scrape of NASA Mars News - COMPLETE')

### JPL Mars Space Images - Featured Image ###
    # Open a splinter browser to scrape the desired images
    # Define the URL path
    url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Using the already established splinter engine, open the url in broswer
    # Visit the defined URL on your splinter broswers
    browser.visit(url_2)
    # delay action until browser loads
    time.sleep(1)
    # click on the sprinter browser link 'FULL IMAGE' to see the image we want to store
    browser.click_link_by_partial_text('FULL IMAGE')

    # delay action until browser loads
    time.sleep(1)
    # Scrape the web page for the image URL
    # First save the root webpage URL to add to the image source ('img src')
    jpl_url = 'https://www.jpl.nasa.gov'
    # Soupify the browser html
    soup = bs(browser.html, 'html.parser')
    # Locate the 'div' and class attribute where the image is found and 
    image_soup = soup.find('div', class_='fancybox-inner')
    # Isolate the image url image source string by .find() and calling the ['src']
    image_url_string = image_soup.find('img')['src']
    # Assign the string compound image url to a variable
    featured_image_url = jpl_url + image_url_string

    print('Scrape of JPL Mars Featured Image - COMPLETE')

### Mars Facts ###
    # We will use Pandas to scrape the table information from the space-fact.com website on Mars
    # Define the url
    url = 'https://space-facts.com/mars/'

    # Using pd.read_html() will pull a list dataframes of all the tables
    tables = pd.read_html(url)
    # We want to slice off the 1st table from the list
    mars_facts_tbl = tables[0]
    # Name the columns
    mars_facts_tbl.columns = ['Attribute', 'Value']
    # Set the index to the Atrributes column
    mars_facts_tbl.set_index('Attribute', inplace=True)
    
    # Convert the pandas dataframe table into html using .to_html()
    html_mars_tbl = mars_facts_tbl.to_html()

    print('Scrape of Mars Facts - COMPLETE')

### Mars Hemispheres ###
    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    # Define URL
    url_3 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    root_usgs_url = 'https://astrogeology.usgs.gov/'

    # Use splinter browser to open url site
    browser.visit(url_3)

    # delay action until browser loads
    time.sleep(1)
    #soupify
    soup = bs(browser.html, 'html.parser')

    # Create an empty list to store dictonary values for the keys of 'image_url' and 'title'
    hemisphere_image_list = []
    # Use .find_all() to slice out the html we will loop through to visit different webpages and scrape the data
    image_links = soup.find_all('div', class_='item')

    # Start the for loop
    for item in image_links:
        # Find the url link string from the 'a' tag and call the 'href' string
        link = item.find('a')['href']    
        # Combine the root url from above and the link url
        url_4 = root_usgs_url + link
        # Open the splinter browser using the url_4 link we just created
        browser.visit(url_4)
        # Let the browser load for 1 seconds before scraping data
        time.sleep(1)
        # Soupify the page
        soup = bs(browser.html, 'html.parser')
        
        # Find the link to the image in the 'ul' tag, then the 'a' tag, and then call the 2nd item 'href'
        # Store link string in variable 'image_link_hemi'
        image_link_hemi = soup.find('ul').find_all('a')[1]['href']
        
        # Find the title name using the 'h2' tag and class attribute 'title', and then pull the .text
        # Store title in variable 'title_text'
        title_text = soup.find('h2', class_='title').text
        
        # Append the hemisphere list with a dictionary of the keys and values
        hemisphere_image_list.append({
            'title': title_text, 
            'img_url': image_link_hemi
        })
        
        # Print out success message
        print(f'Scrape of {title_text} successful')
        time.sleep(1)

    print('Scrape of Mars Hemispheres - COMPLETE')

    # Create a dictionary of all the web scraped data
    dict_mars_scrape = {
        'news_title': news_title,
        'news_p': news_p,
        'article_url': article_url,
        'featured_image_url': featured_image_url,
        'html_mars_tbl': html_mars_tbl,
        'hemisphere_image_list': hemisphere_image_list,
        # Add the time of the scrape to the dictionary
        'scrape_time': dt.datetime.now()
    }

    # Close browser after scraping is complete
    browser.quit()

    print('Webscraping and data dictionary creation - COMPLETE')
    print(dict_mars_scrape)
    return dict_mars_scrape 

