import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
from bs4 import Comment
import requests
import os
import copy

from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException

import tools

option = webdriver.ChromeOptions()
exec_path = Path(os.getcwd().replace("\\", '/'))
chrome_path = exec_path.parent.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_path, options=option)

# read the url from each file into a list
course_links_file_path = exec_path.__str__() + '/links_file.txt'
all_url = open(course_links_file_path, 'r')

level_key = tools.level_key
all_course_data = []

possible_city = {'Melbourne': ['Burwood (Melbourne)', 'Burwood (Melbourne)*'],
                 'Geelong': ['Waurn Ponds (Geelong)', 'Waterfront (Geelong)'],
                 'Warrnambool': ['Warrnambool'],
                 'Cloud': ['Cloud']}

possible_faculty = {'Student Services Network', 'Faculty of Business and Law', 'Prospective Student Enquiry Centre',
                    'Faculty of Science, Engineering and Built Environment', 'Faculty of Arts and Education',
                    'No Faculty Listed'}

prerequisite_subjects = {'English EAL': ['25', '30'],
                         'English (EAL)': ['30'],
                         'Maths: Mathematical Methods or Maths: Specialist Mathematics': ['20'],
                         'WAM': ['65'],
                         'ATAR': ['70.00'],
                         'three-year major sequence in psychology': ['65']}

# all_url = ["https://www.deakin.edu.au/course/bachelor-early-childhood-and-primary-education-international"]
for each_url in all_url:
    driver.get(each_url)
    pure_url = each_url.strip()
    time.sleep(2)
    url = driver.page_source
    soup = bs4.BeautifulSoup(url, 'html.parser')
    title = soup.find('h1')
    print(title.text)

