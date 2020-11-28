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
    time.sleep(1)
    driver.get(each_url)
    pure_url = each_url.strip()
    time.sleep(5)
    url = driver.page_source
    soup = bs4.BeautifulSoup(url, 'html.parser')
    course_data = {'Level_Code': '', 'University': 'Deakin University', 'City': '', 'Course': '', 'Faculty': '',
                   'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'Years', 'Duration': '',
                   'Duration_Time': 'Year', 'Full_Time': 'No', 'Part_Time': 'No',
                   'Prerequisite_1': '', 'Prerequisite_2': '', 'Prerequisite_3': '',
                   'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                   'Website': '', 'Course_Lang': 'English', 'Availability': 'I', 'Description': '',
                   'Career_Outcomes': '',
                   'Country': 'Australia', 'Online': 'No', 'Offline': 'Yes', 'Distance': 'No', 'Face_to_Face': 'Yes',
                   'Blended': 'No', 'Remarks': '', 'Course_Delivery_Mode': 'Normal', 'Free TAFE': 'No'}
    time.sleep(10)
    # Find website
    course_data['Website'] = pure_url

    # Find cost
    time.sleep(10)
    containers = soup.find_all('div', {'class', 'module__content-panel--text module__content-panel--text--course'})
    cost_container = []
    cost = []
    for container in containers:
        title = container.find('div', {'class', 'module__key-information--item-title'})
        if title:
            if "Estimated tuition fee" in title.text:
                cost_container = container.find('div', {'class', 'module__key-information--item-content'}).text
                cost_container = tools.cleaner(cost_container)
                cost_text = cost_container
                cost = cost_text[:cost_text.index('f')]
                break

    del cost_container
    course_data['Int_Fees'] = cost
    print(cost)

    # Find course title
    title = soup.find('h1')
    course_data['Course'] = title.text
    print(title.text)
    # Decide level code
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
                break
        if course_data['Level_Code'] != '':
            break

    if "Honours" in course_data['Course']:
        course_data['Level_Code'] += 'H'

    # Find Description
    description_tag = soup.find('div',
                                {'class',
                                 'module__overview--content module__overview--course--content module__toggle-content'})
    description = description_tag.find('p').text.strip()

    course_data['Description'] = description

    # Find container
    containers = soup.find('div', {'class', 'course--keyfacts module__content-panel module__course-stacked-content'}). \
        find_all('div', {'class', 'module__content-panel--wrapper module__content-panel--wrapper--content-spacing'})

    # Find part time and full time
    duration_tag = []
    for tag in containers:
        if "Duration" in tag.text:
            duration_tag = tag.find('div',
                                    {'class',
                                     'module__content-panel--text module__content-panel--text--course'})
            if "full-time" in duration_tag.text or "full time" in duration_tag.text:
                course_data['Full_Time'] = "Yes"
            if "part-time" in duration_tag.text and "International students are required to study full-time" \
                    not in duration_tag.text or "part time" in duration_tag.text:
                course_data['Part_Time'] = "Yes"
            duration = duration_tag.text.strip().lower()
            course_data['Duration'] = duration[:duration.index('r')]
            break
        else:
            course_data['Duration'] = "Not given"
            course_data['Full_Time'] = "NA"
            course_data['Part_Time'] = "NA"

    # Find Location
    location_tag = []
    for tag in containers:
        if "Campuses" in tag.text:
            location_tag = tag.find('div',
                                    {'class',
                                     'module__content-panel--text module__content-panel--text--course campus--list'})
            break

    tag = location_tag.text
    actual_cities = []

    for i in possible_city:
        for j in possible_city[i]:
            if j in tag:
                actual_cities.append(i)

    # check duplicate city
    actual_cities = list(dict.fromkeys(actual_cities))

    # Find Online
    for city in actual_cities:
        if "Cloud" in city:
            course_data['Online'] = "Yes"
            actual_cities.remove('Cloud')

    time.sleep(3)
    # Find faculty
    faculty_tag = []
    faculty_text = []
    tags = soup.find_all('div', {'class', 'module__content-panel'})
    for tag in tags:
        if "Contact information" in tag.text:
            faculty_tag = tag.find('div',
                                   {'class', 'module__content-panel--text module__content-panel--text--course'})
            faculty_text = faculty_tag.find('p').text
            for faculty in possible_faculty:
                if faculty in faculty_text:
                    course_data['Faculty'] = faculty
                    break
            break
        else:
            course_data['Faculty'] = "No Faculty Listed"

    time.sleep(5)

    # Find Prerequisite subjects
    subjects_list = []
    try:
        subjects_list = driver.find_element_by_xpath('//*[@id="tab__2--1"]/div/p[3]').text
    except NoSuchElementException:
        subject_container = []
        containers = soup.find_all('div',
                                   {'class',
                                    'module__content-panel--wrapper module__content-panel--wrapper--content-spacing'})
        for container in containers:
            if "Entry requirements" in container.text or "Higher education experience" in container.text or \
                    "Entry information" in container.text:
                subject_container = container.find \
                    ('div', {'class', 'module__content-panel--text module__content-panel--text--course'})
                break
        subjects_list = subject_container.text

    num = 1
    subjects = subjects_list.split('; ')
    print(subjects)

    for subject in subjects:
        for p_subject in prerequisite_subjects:
            if p_subject in subject:
                course_data['Prerequisite_' + num.__str__()] = p_subject

                for subject_grade in prerequisite_subjects[p_subject]:
                    if subject_grade in subject:
                        course_data['Prerequisite_' + num.__str__() + '_grade_' + num.__str__()] = subject_grade

                num += 1
                break

        if num == 4:
            break

    if not course_data['Prerequisite_1']:
        course_data['Prerequisite_1'] = "Minimum English requirement: refer to websites: " \
                                        "https://www.deakin.edu.au/international-students/getting-into-deakin/" \
                                        "entry-requirements/english-language-requirements"

    # Find Career outcome
    containers = soup.find_all('div', {'class',
                                       'module__content-panel--wrapper module__content-panel--wrapper--content-spacing'})
    career_outcome_text = ''

    for tag in containers:
        if "Career outcomes" in tag.text:
            career_outcome_tag = tag
            career_outcome_text = career_outcome_tag.find(
                'div', {'class', 'module__content-panel--text module__content-panel--text--course'}).text
            course_data['Career_Outcomes'] = career_outcome_text.strip()
            print(course_data['Career_Outcomes'])
            break

    for i in actual_cities:
        course_data['City'] = i
        all_course_data.append(copy.deepcopy(course_data))
    del actual_cities
    del faculty_text

print(*all_course_data, sep='\n')
driver.close()
desired_order_list = ['Level_Code',
                      'University',
                      'City',
                      'Course',
                      'Faculty',
                      'Local_Fees',
                      'Int_Fees',
                      'Currency',
                      'Currency_Time',
                      'Duration',
                      'Duration_Time',
                      'Full_Time',
                      'Part_Time',
                      'Prerequisite_1',
                      'Prerequisite_2',
                      'Prerequisite_3',
                      'Prerequisite_1_grade_1',
                      'Prerequisite_2_grade_2',
                      'Prerequisite_3_grade_3',
                      'Website',
                      'Course_Lang',
                      'Availability',
                      'Description',
                      'Career_Outcomes',
                      'Country',
                      'Online',
                      'Offline',
                      'Distance',
                      'Face_to_Face',
                      'Blended',
                      'Remarks',
                      'Course_Delivery_Mode',
                      'Free TAFE']
# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/Int_Postgraduate_Complete.csv'

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    dict_writer.writerows(all_course_data)

output_file.close()
