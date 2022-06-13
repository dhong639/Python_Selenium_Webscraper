#   import selenium API for web scraping
#   for this specific example, Microsoft Edge was the browser
#       this script was not tested on any other browser
#   does not use the deprecated find_elements_by_.+ functions
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
#   used to avoid the following error
#       stale element reference: element is not attached to the page document
#   error caused by document not fully loading after a button is pressed
import time
#   used to write to csv file
#   pandas is not used because requirements did not state required csv API
import csv

#   options to make browser window big and stop warnings
#       usb: usb_device_handle_win.cc:1048 Failed to read descriptor from node connection: 
#           A device attached to the system is not functioning.
#       EDGE_IDENTITY: Get Default OS Account failed: 
#           Error: Primary Error: kImplicitSignInFailure, 
#           Secondary Error: kAccountProviderFetchError, Platform error: 0, 
#           Error string: 
options = webdriver.EdgeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#   driver for microsoft edge
#       version 102.0.1245.39
#       https://msedgewebdriverstorage.z22.web.core.windows.net/
#   expects file named located as ./msedgedriver/msedgedriver.exe
service = Service('./msedgedriver/msedgedriver')

#   load webpage
driver = webdriver.Edge(service=service, options=options)
driver.get('https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops')

#   path for buttons
#   format to click specific button
PATH_BUTTON = '//div[@class="btn-group pagination"]/button[@data-id="{}"]'

#   path to each item to draw data from
#       each item is contained within a div with the "thumbnail" class
#       html elements are traversed via xpath
#       everything but name is stored as text
#   items will be drawn as a list
PATH_THUMBNAIL = '//div[@class="thumbnail"]'
PATH_CAPTION = '/div[@class="caption"]'
PATH_PRICE = '/h4[@class="pull-right price"]'
PATH_NAME = '/h4/a[@class="title"]'
PATH_DESCRIPTION = '/p[@class="description"]'
PATH_RATINGS = '/div[@class="ratings"]/p[@class="pull-right"]'

#   store end results
list_ = []

#   only need to draw data from 5 pages
for i in range(5):
    #   click button
    #   document must load fully to avoid "stale data" error
    #       use timer to ensure that all elements load
    button = driver.find_element(By.XPATH, PATH_BUTTON.format(i + 1))
    button.click()
    time.sleep(1)

    #   get data for each entry
    #       there are a total of 6 entries per page
    #       path for each entry determined by combining constant PATH variables
    #   note that names will not display fully, use "title" attribute instead
    #   note that reviews are technically integers, "reviews" substring is redundant

    path_name = PATH_THUMBNAIL + PATH_CAPTION + PATH_NAME
    list_name = [item.get_attribute('title') for item in driver.find_elements(By.XPATH, path_name)]

    path_price = PATH_THUMBNAIL + PATH_CAPTION + PATH_PRICE
    list_price = [item.text for item in driver.find_elements(By.XPATH, path_price)]

    path_description = PATH_THUMBNAIL + PATH_CAPTION + PATH_DESCRIPTION
    list_description = [item.text for item in driver.find_elements(By.XPATH, path_description)]

    path_ratings = PATH_THUMBNAIL + PATH_RATINGS
    list_ratings = [int(item.text.split()[0]) for item in driver.find_elements(By.XPATH, path_ratings)]

    #   append each entry to list_ as a dictionary
    #       note that prior lists are acquired in the order that they are listed in the HTML
    for j in range(6):
        dict_ = {
            'Name': list_name[j],
            'Price': list_price[j],
            'Description': list_description[j],
            'Review': list_ratings[j]
        }
        list_.append(dict_)

#   exit webpage
driver.quit()

#   write results to csv
#       do not let windows write a carriage return
#   file stored in current directory
fields = ['Name', 'Price', 'Review', 'Description']
with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(list_)
