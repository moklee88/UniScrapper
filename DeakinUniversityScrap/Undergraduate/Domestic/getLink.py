import csv
from pathlib import Path
import time

from selenium import webdriver
import bs4 as bs4
import requests
import os
from selenium.webdriver.support.ui import Select

url = 'https://www.deakin.edu.au/courses/find-a-course'

option = webdriver.ChromeOptions()
# option.add_argument(" - incognito")
# option.add_argument("headless")
# option.add_argument('--no-sandbox')
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=exec_path, options=option)

course_links = []
driver.get(url)
pure_url = url.strip()
each_url = driver.page_source

time.sleep(5)

# Select value change into all result
select = Select(driver.find_element_by_name('undergrad_course_resultset_length'))
select.select_by_value('-1')

# Set the delay for page to load
time.sleep(6)

# Get result table
result = driver.find_element_by_css_selector(".results-body").find_elements_by_css_selector('.course-title.sorting_1')

# Find the course link
for course in result:
    link = course.find_element_by_tag_name('a')
    course_links.append(link.get_attribute('href'))
print(course_links)

driver.close()

course_links_file_path = os.getcwd().replace('\\', '/') + '/links_file.txt'
course_links_file = open(course_links_file_path, 'w')
for i in course_links:
    course_links_file.write(i.strip()+'\n')

course_links_file.close()
