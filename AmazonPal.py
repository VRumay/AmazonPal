"""
AmazonPal is a webscraper for Amazon.com that gathers data for Item Name & Item Price 
from the items that come as a result of user search (input) and save it in an excel file through a pandas dataframe.

The goal is to use that data for price and location analysis, maybe gain some competitve advantage too!.  

Amazon US makes a really good effort in dinamically changing classnames in their HTML (new classnames every day!), so scraping can be really difficult.

Amazon.es is not as heavily guarded though.

The scraper is working as of Sept 19, 2020. Using it after that date, might require some tweaking.

"""

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time



# Webdriver and site
webdriver_path = r'YOUR_LOCATION\chromedriver.exe'

# Url definition based on search term of user.
searchterm = input('Type in the item you want to search for: ')         
searchterm.replace(' ','+') # White spaces need to be replaced with a '+' for the URL
url = f'https://www.amazon.com/s?k={searchterm}&page=1'

# Browse from chromedriver 
browser = webdriver.Chrome(webdriver_path)
browser.get(url)


# Create a list for each object that will be scraped (one for title, one for price, etc)
tList = []
pList = []

# Create a dataframe that will be populated with the contents of the lists once the while loop is done scraping
column_names = ['productName', 'productPrice']
primarydf = pd.DataFrame(columns = column_names)


# Set minimum amount of pages in case there is no more than one:
pageLimit = 1
nextpage = 1

# Find how many pages come up after search and use the number as a limit for iterations in while loop:
totalPages = browser.find_elements_by_class_name("a-disabled")
for element in totalPages:
    try:    
        pageLimit = (int(element.text) + 1) 
        print(f"Got'em! {pageLimit} pages to iterate")
        nextpage = 2

    except:
        print("Oops, that wasn't it")



# Main Scraping Loop
while nextpage <= pageLimit:
    item_titles = browser.find_elements_by_class_name("a-size-base-plus.a-color-base.a-text-normal")
    item_prices = browser.find_elements_by_class_name('a-price-whole')
    for t, p in zip(item_titles, item_prices):
        tList.append(t.text) 
        pList.append(p.text)
        print(f'{t.text}  {p.text}')
    
    newurl = f'https://www.amazon.com/s?k={searchterm}&page={nextpage}'
    browser.get(newurl)

    nextpage += 1
       
    time.sleep(2)

# Lists to dataframe
primarydf['productName']  = tList
primarydf['productPrice']  = pList
print (primarydf)

# Saving CSV file
primarydf.to_csv(f'{searchterm}.csv', index=False, encoding='utf-8')

#print(primarydf)
browser.close()

# headless chrome