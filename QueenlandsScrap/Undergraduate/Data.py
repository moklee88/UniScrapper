import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import requests
import os
import copy

import data
import tools

each_url = "https://future-students.uq.edu.au/study/programs/bachelor-dental-science-honours-2367"

option = webdriver.ChromeOptions()
exec_path = Path(os.getcwd().replace('\\', '/'))
chrome_path = exec_path.parent.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_path, options=option)

# read the url from each file into a list
course_links_file_path = exec_path.__str__() + '/links_file.txt'

all_url = open(course_links_file_path, 'r')
level_key = tools.level_key

possible_cities = {'St Lucia', 'Gatton', 'Herston', 'Pharmacy Aust Cntr Excellence'}

prerequisite_subjects = {'General English subject': ['Units 3 & 4, C'],
                         'Mathematical Methods or Specialist Mathematics': ['Units 3 & 4, C'],
                         ' UCAT (domestic* only)': [],
                         'IELTS': ['7', '6.5'],
                         'Bachelor of Environmental Science': ['4']}

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
csv_file = csv_file_path.__str__() + '/Queenlands_NoFees.csv'

with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()
    for each_url in all_url:
        course_data = {'Level_Code': '', 'University': 'University Of Queenlands', 'City': '', 'Course': '',
                       'Faculty': '',
                       'Int_Fees': '', 'Local_Fees': 'fees not listed', 'Currency': 'AUD', 'Currency_Time': 'Years',
                       'Duration': '',
                       'Duration_Time': '', 'Full_Time': 'No', 'Part_Time': 'No',
                       'Prerequisite_1': '', 'Prerequisite_2': '', 'Prerequisite_3': '',
                       'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                       'Website': '', 'Course_Lang': 'English', 'Availability': 'A', 'Description': '',
                       'Career_Outcomes': '',
                       'Country': 'Australia', 'Online': 'No', 'Offline': 'Yes', 'Distance': 'No',
                       'Face_to_Face': 'Yes',
                       'Blended': 'No', 'Remarks': '', 'Course_Delivery_Mode': 'Normal', 'Free TAFE': 'No'}
        driver.get(each_url)
        driver.find_element_by_xpath('.//*[@id="overview"]/div[1]/div/section[1]/article/div[1]/a').click()
        pure_url = each_url.strip()
        program_code = pure_url[-4:]  # get the program code for finding other information

        url = driver.page_source

        soup = bs4.BeautifulSoup(url, 'html.parser')

        # Find website
        course_data['Website'] = pure_url

        # Find Course Title
        title = soup.find('div', {'class', 'hero__text'}).text.strip()

        title = re.sub(r'\s+', ' ', title)
        course_data['Course'] = title

        print(course_data['Course'])

        # Decide level code
        course_data['Level_Code'] = data.course_title(course_data['Course'])

        if "Honours" in course_data['Course'] or "honours" in course_data['Course']:
            course_data['Level_Code'] += 'H'

        # Find information container
        details = soup.find_all('dl')

        # find international fees
        imperfect = details[1].find('a').text
        imperfect = tools.cleaner(imperfect)

        fees = imperfect[:imperfect.index('(')]
        course_data['Int_Fees'] = fees
        # print(course_data['Int_Fees'])

        # Find location
        location_tag = details[0].find('dd')
        locations = location_tag.text.strip()
        actual_cities = []

        for i in possible_cities:
            if i in locations:
                actual_cities.append(i)

        # check duplicate city
        actual_cities = list(dict.fromkeys(actual_cities))

        # Find Duration Value
        duration_tag = details[0].find('dd').find_next('dd').text.strip()
        duration_text = re.sub(r'\s+', ' ', duration_tag)
        duration = duration_text[:duration_text.index(' ')]

        # Find full time, part time
        if "full-time" in duration_text:
            course_data['Full_Time'] = "Yes"
        else:
            course_data['Full_Time'] = 'Yes'
            course_data['Part_Time'] = 'Yes'
            course_data['Blended'] = 'Yes'

        # Find Description
        description = soup.find('div', {'class', 'page__sections'}).find('div', {'class', 'collapsible'}).text
        course_data['Description'] = description
        print(description)

        # Find career outcomes
        career_tag = []
        sections = soup.find_all('section',
                                 {'class',
                                  'section section--narrow-floated section--mobile-accordion accordion processed'})
        for section in sections:
            if "Career possibilities" in section:
                career_tag = section.find('article')

        course_data['Career_Outcomes'] = career_tag.text

        # Find Subject
        subject_url = each_url + "#entry-requirements"
        driver.get(subject_url)
        page = driver.page_source
        subject_soup = bs4.BeautifulSoup(page, 'html.parser')

        prerequisites_subject_tag = subject_soup.find_all \
            ('section', {'class', 'section section--narrow-floated spacing--bottom-m'})

        subjects = []
        for tag in prerequisites_subject_tag:
            if "Prerequisites" in tag.find('h3').text:
                subjects = tag.find('div').text

        subjects = prerequisites_subject_tag.split(';')

        ielts_tags = subject_soup.find_all \
            ('div', {'class', 'section section--narrow-floated section--mobile-accordion accordion processed'})

        ielts = []
        for tag in ielts_tags:
            if "English language requirements" in tag.text:
                ielts = tag.find('p').text

        subjects.append(ielts)

        num = 1
        for subject in subjects:
            for p_subject in prerequisite_subjects:
                if p_subject in subject:
                    course_data['Prerequisite_' + num.__str__()] = p_subject

                    for subject_grade in prerequisite_subjects[p_subject]:
                        if subject_grade in subject:
                            course_data['Prerequisite_' + num.__str__() + '_grade_' + num.__str__()] = subject_grade
                            break
                    num += 1
                    break
            if num == 4:
                break

        # New webpage for faculty
        data_url = "https://my.uq.edu.au/programs-courses/program.html?acad_prog=" + program_code.__str__() + \
                   "&year=2021#international"
        driver.get(data_url)
        detail_url = driver.page_source
        detail_soup = bs4.BeautifulSoup(detail_url, 'html.parser')

        # Find Faculty
        faculty = detail_soup.find(id="program-international-faculty").text
        course_data['Faculty'] = faculty

        for i in actual_cities:
            course_data['City'] = i
            dict_writer.writerow(course_data)
        del actual_cities


driver.close()
output_file.close()



