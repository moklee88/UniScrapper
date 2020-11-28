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

url = "https://future-students.uq.edu.au/study/programs/bachelor-advanced-business-honours-2139"

option = webdriver.ChromeOptions()
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=exec_path, options=option)

"""
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/ucq_bachelor_links_file'
course_links_file = open(course_links_file_path, 'r')
"""

driver.get(url)
pure_url = url.strip()
program_code = pure_url[-4:]  # get the program code for finding other information

each_url = driver.page_source

soup = bs4.BeautifulSoup(each_url, 'html.parser')

course_data = {'Level_Code': '', 'University': 'University Of Queenlands', 'City': '', 'Course': '', 'Faculty': '',
               'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years', 'Duration': '',
               'Duration_Time': '', 'Full_Time': '', 'Part_Time': '',
               'Prerequisite_1': '', 'Prerequisite_2': '', 'Prerequisite_3': '',
               'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
               'Website': '', 'Course_Lang': 'English', 'Availability': 'A', 'Description': '', 'Career_Outcomes': '',
               'Country': 'Australia', 'Online': 'No', 'Offline': 'Yes', 'Distance': 'No', 'Face_to_Face': '',
               'Blended': 'No', 'Remarks': ''}

# Find information container
fees_details = soup.find('dl').find_next('dl')

# find international fees
imperfect = fees_details.find('a')
fees = imperfect.text[2:-21]

# New webpage for more data
data_url = "https://my.uq.edu.au/programs-courses/program.html?acad_prog=" + program_code.__str__() + \
           "&year=2021#international"
driver.get(data_url)
detail_url = driver.page_source
detail_soup = bs4.BeautifulSoup(detail_url, 'html.parser')

# Find Duration Value
duration_full = detail_soup.find(id='program-international-duration')
clean_duration = duration_full.text.strip().replace(" ", '')[0]
print(clean_duration)

# Find Faculty
faculty = detail_soup.find(id="program-international-faculty").text

# Find Description
description = detail_soup.find('div', {'class', 'usercontent'}).find_next('p').find_next('p').text

# Find Pre