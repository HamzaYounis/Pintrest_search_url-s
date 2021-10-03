import requests
from bs4 import *
from selenium import webdriver
import pandas as pd
import argparse
import re
import os
from selenium.webdriver.support import ui
import time
from webdriver_manager.chrome import ChromeDriverManager


## Email and Password
## Enter credentials path here
with open(r'\email&pass.txt','r',encoding='latin') as infile:
    for row in infile:
        email=row.split(',')[0]
        password=row.split(',')[1].replace('\n','')

login_name=email
login_pass=password

parser = argparse.ArgumentParser()
parser.add_argument(
    '--saveto', help='Target CSV to save the Image URLs', action='store', dest='CSVname')
parser.add_argument('--category', help='Product category to be searched ',
                    action='store', dest='category')
parser.add_argument('--username', help='username',
                    action='store', dest='login_name')
parser.add_argument('--password', help='password',
                    action='store', dest='login_pass')
args = parser.parse_args()

if(args.category):
    item_category = str(args.category)
else:
    item_category = str(
        input('Enter the search category (Ex : Nike Black shoes): '))

if(args.CSVname):
    csv_name = str(args.CSVname)
else:
    csv_name = item_category + '.csv'

csv_name = csv_name.replace(" ", "_")


# Initialize and launch the chrome driver
driver  = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get("https://www.pinterest.com")

driver.implicitly_wait(20)


def page_is_loaded(driver):
    return driver.find_element_by_tag_name("body") != None


def login(driver, username, password):
    if driver.current_url != "https://www.pinterest.com/login/?referrer=home_page":
        driver.get("https://www.pinterest.com/login/?referrer=home_page")
    wait = ui.WebDriverWait(driver, 10)
    wait.until(page_is_loaded)
    email = driver.find_element_by_xpath("//input[@type='email']")
    password = driver.find_element_by_xpath("//input[@type='password']")
    email.send_keys(login_name)
    password.send_keys(login_pass)
    # driver.find_element_by_xpath("//div[@data-reactid='30']").click()
    password.submit()
    print("Teleport Successful!")


login(driver, login_name, login_pass)
driver.implicitly_wait(30)
time.sleep(3)


# import pdb;pdb.set_trace()


# prepare the URL for search
url = 'https://in.pinterest.com/search/pins/?q=' + item_category.replace(" ", "%20")

# wait and get the query page
driver.get(url)
time.sleep(3)

# driver.implicitly_wait(30)

all_pin_data = []

while 1:
    # scroll
    driver.execute_script("window.scrollBy(0,10000)")
    time.sleep(3)
    driver.execute_script("window.scrollBy(0,10000)")
    time.sleep(3)

    # get the html now
    page_source = driver.page_source
    page = BeautifulSoup(page_source, 'html.parser')

    # 'GrowthUnauthPinImage' is the class of all the pins
    # Here we take divs which have a with href as pin number
    pin_data = page.find_all('div', "Yl- MIw Hb7")

    all_pin_data.extend(pin_data)
    all_pin_data = list(set(all_pin_data))

    print(len(pin_data))
    if len(all_pin_data) > 50:
        break


# get links for individual pages of all the Pins
for i in range(len(all_pin_data)):
    try:
        with open(item_category+'.csv','a',encoding='latin') as out:
            link=all_pin_data[i].find('img')['srcset'].split(',')[-1].replace('4x','').strip()
            out.write(link+'\n')
            out.close()
    except:
        pass
driver.close()

