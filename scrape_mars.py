# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser, browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    #display the current title content
    title = slide_elem.find("div", class_="content_title")
    #title

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find("div", class_="content_title").get_text()
    #news_title

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    #news_p

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    image = browser.links.find_by_partial_text('FULL IMAGE')
    image.click()

    # Parse the resulting html with soup
    html = browser.html
    mars_soup = soup(html, 'html.parser')

    # find the relative image url
    img_url_rel = mars_soup.find('img', class_='fancybox-image')['src']
    #img_url_rel

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    #img_url

    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    # hint use index 0 to find the table
    MarsEarth = pd.read_html('https://galaxyfacts-mars.com/')
    MarsEarthDF = MarsEarth[0]
    #MarsEarthDF.head()

    # Rename columns and set index to Description
    MarsEarthDF.columns=["Description", "Mars", "Earth"]
    MarsEarthDF.set_index("Description", inplace=True)
    #MarsEarthDF

    # Convert dataframe to HTML
    MEDF = MarsEarthDF.to_html()

    # Visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemi = {}
            
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item img')[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample = browser.find_by_text('Sample').first
        hemi["img_url"] = sample['href']
        
        # Get Hemisphere title
        hemi["title"] = browser.find_by_css("h2.title").text
        #print(hemi)
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi)
        
        # Finally, we navigate backwards
        browser.back()

    # Print list of dictionaries
    #hemisphere_image_urls

    mars_info = {
        "news_title": news_title,
        "news_p": news_p,
        "mars_featured_image": img_url,
        "mars_df": MEDF,
        "mars_hemis": hemisphere_image_urls
    }
    browser.quit()

    return mars_info