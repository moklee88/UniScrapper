import csv
from pathlib import Path
import time
from telnetlib import EC

from selenium import webdriver
import bs4 as bs4
import requests
import os

from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://future-students.uq.edu.au/study/programs?level[Undergraduate]=Undergraduate&year=2021'
# url = 'https://my.uq.edu.au/programs-courses/browse.html?level=ugpg'

option = webdriver.ChromeOptions()
# option.add_argument(" - incognito")
# option.add_argument("headless")
# option.add_argument('--no-sandbox')
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=exec_path, options=option)

course_type_links = []
course_links = []
driver.get(url)
pure_url = url.strip()
each_url = driver.page_source

end_result = False
# Find the existence of next button then trigger the button for next page result
while not end_result:
    time.sleep(3)

    # Get result table
    result = driver.find_element_by_css_selector(".grid.spacing--bottom-xxl").find_elements_by_tag_name('a')

    # Find the course link
    for link in result:
        course_links.append(link.get_attribute('href'))
    print(course_links)

    # test
    try:
        driver.find_element_by_xpath("//a[@title='Go to next page']").click()

    except ElementNotInteractableException:
        print("No such element")
        break

driver.close()
course_links_file_path = os.getcwd().replace('\\', '/') + '/links_file.txt'
course_links_file = open(course_links_file_path, 'w')
for i in course_links:
    course_links_file.write(i.strip()+'\n')

course_links_file.close()
