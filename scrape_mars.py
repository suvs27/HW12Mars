from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter.exceptions import ElementDoesNotExist
import time



def scrape_info():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scraping Nasa Mars News
    # Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) 
    # and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    source = requests.get('https://mars.nasa.gov/news/').text
    soup = bs(source, 'html.parser')
    article = soup.find_all('div', class_='content_title')
    
    news_title0 = article[0].a.text
    news_title1 = article[1].a.text
    news_title2 = article[2].a.text

    description = soup.find_all('div', class_="rollover_description_inner")
    news_p0 = description[0].text
    news_p1 = description[1].text
    news_p2 = description[2].text

    # Scraping JPL Mars Space Images - Featured Image
    # Return featured_img_url


    #Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
    #Use splinter to navigate the site 
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    try:
        browser.click_link_by_id('full_image')
    except:
        browser.click_link_by_partial_text('FULL IMAGE')
    else:
        print("Scraping Full Image Complete")

    
    check = 0
    try:
        links_found = browser.find_link_by_partial_href('spaceimages/details')
        url2 = links_found[0]["href"]
        browser.click_link_by_partial_text('more info')
        links_found2 = browser.find_link_by_partial_href('spaceimages/images/largesize')
        f1 = links_found2[0]["href"]
        check = 1
    except:
        browser.visit(url2)
        links_found3 = browser.find_link_by_partial_href('spaceimages/images/largesize')
        f2 = links_found3[0]["href"]
    else:
        print("Scraping More Info Complete")
        

    if check ==1:
        featured_image_url = f1
    else:
        featured_image_url = f2

    # Mars Weather
    # Returns (mars_weather)


    #Visit the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en) 
    #and scrape the latest Mars weather tweet from the page. 
    #Save the tweet text for the weather report as a variable called `mars_weather`
    source3 = requests.get('https://twitter.com/marswxreport?lang=en').text
    soup = bs(source3, 'html.parser')
    tweets = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    #print(tweets[0].text)

    mars_weather = tweets[0].text   

    #Mars Facts
    # Returns (mars_facts_table)

    facts = pd.read_html("https://space-facts.com/mars/")

    mars_facts_df = facts[1]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df.set_index("Description", inplace=True)
    mars_facts_df.head()
    mars_facts_table = mars_facts_df.to_html()
    mars_facts_table = mars_facts_table.replace('\n', '')

    # Mars Hemispheres
    # Returns hemisphere_image_urls


    hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi)
    html = browser.html

    # Get titles for all four mars pictures
    soup = bs(html, 'html.parser')
    hemi_class = soup.find_all('h3')
    cerberus_title = hemi_class[0].text
    schiaparelli_title = hemi_class[1].text
    syrtis_title = hemi_class[2].text
    valles_title = hemi_class[3].text

    # Get Cerberus Information
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')
    link1 = (browser.find_link_by_partial_text('Original'))
    cerberus_link = (link1[0]["href"])
    browser.back()

    # Get Schiaparelli Information
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')
    link2 = (browser.find_link_by_partial_text('Original'))
    schiaparelli_link = (link2[0]["href"])

    browser.back()

    # Get Syrtis Major Information
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')
    link3 = (browser.find_link_by_partial_text('Original'))
    syrtis_link = (link3[0]["href"])
    browser.back()

    # Get Valles Major Information
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')
    link4 = (browser.find_link_by_partial_text('Original'))
    valles_link = (link4[0]["href"])
    browser.back()
    


    marsdata = {"news_title0": news_title0, 
                "description0": news_p0,
                "news_title1": news_title1,
                "description1": news_p1,
                "news_title2": news_title2, 
                "description2": news_p2,
                "JPL_link": featured_image_url,
                "weather_tweet": mars_weather,
                "facts_table": mars_facts_table,
                "title": cerberus_title, 
                "img_url": cerberus_link,
                "title": schiaparelli_title, 
                "img_url": schiaparelli_link,
                "title": syrtis_title, 
                "img_url": syrtis_link,
                "title": valles_title, 
                "img_url": valles_link}
    

    # Close the browser after scraping
    browser.quit()


    # Return results
    return marsdata


#a = scrape_info()
#print(a)

