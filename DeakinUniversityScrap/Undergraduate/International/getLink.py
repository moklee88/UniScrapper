import csv
from pathlib import Path
import time

from selenium import webdriver
import bs4 as bs4
import requests
import os
from selenium.webdriver.support.ui import Select

option = webdriver.ChromeOptions()
# option.add_argument(" - incognito")
# option.add_argument("headless")
# option.add_argument('--no-sandbox')
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
link_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = link_path.__str__() + '/domestic_links.txt'
all_url = open(course_links_file_path, 'r')

course_links = []
for each_url in all_url:
    each_url.rstrip()
    int_url = each_url.__str__() + '-international'
    driver.get(int_url)
    pure_url = int_url
    url = driver.page_source
    time.sleep(1)
    soup = bs4.BeautifulSoup(url, 'html.parser')
    text = soup.find('h1').text
    if text == "Page not found":
        print('International not available')
    else:
        print(pure_url)
        course_links.append(pure_url.replace('\n', ''))
print(course_links, sep='\n')
driver.close()


course_links_file_path = os.getcwd().replace('\\', '/') + '/links_file.txt'
course_links_file = open(course_links_file_path, 'w')
for i in course_links:
    course_links_file.write(i.strip()+'\n')

course_links_file.close()
