import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import requests
import os
import copy

from selenium.common.exceptions import ElementNotInteractableException

import data
import tools

option = webdriver.ChromeOptions()
exec_path = Path(os.getcwd().replace('\\', '/'))
chrome_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
driver = webdriver.Chrome(executable_path=chrome_path, options=option)

# read the url from each file into a list
course_links_file_path = exec_path.__str__() + '/links_file.txt'

all_url = [""]
# all_url = open(course_links_file_path, 'r')
level_key = tools.level_key

possible_cities = {}
prerequisite_subjects = {}

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
                      'Subject_or_Unit_1', 'Subject_Objective_1', 'Subject_Description_1',
                      'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                      'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                      'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                      'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                      'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                      'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                      'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                      'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                      'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                      'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                      'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                      'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                      'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                      'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                      'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                      'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                      'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                      'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                      'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                      'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                      'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                      'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                      'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                      'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                      'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                      'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                      'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                      'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                      'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                      'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                      'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                      'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                      'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                      'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                      'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                      'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                      'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                      'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                      'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40',
                      'Course_Delivery_Mode',
                      'Free TAFE']

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/Uni.csv'
change_to_int = False
with open(csv_file, 'a', encoding='utf-8', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=desired_order_list)
    dict_writer.writeheader()

    for each_url in all_url:
        course_data = {'Level_Code': '', 'University': 'University Of Queenlands', 'City': '', 'Course': '',
                       'Faculty': '',
                       'Int_Fees': '', 'Local_Fees': 'fees not listed', 'Currency': 'AUD', 'Currency_Time': 'Years',
                       'Duration': '',
                       'Duration_Time': 'Years', 'Full_Time': 'No', 'Part_Time': 'No',
                       'Prerequisite_1': '', 'Prerequisite_2': '', 'Prerequisite_3': '',
                       'Prerequisite_1_grade_1': '', 'Prerequisite_2_grade_2': '', 'Prerequisite_3_grade_3': '',
                       'Website': '', 'Course_Lang': 'English', 'Availability': 'A', 'Description': '',
                       'Career_Outcomes': '',
                       'Country': 'Australia', 'Online': 'No', 'Offline': 'Yes', 'Distance': 'No',
                       'Face_to_Face': 'Yes',
                       'Blended': 'No', 'Remarks': '', 'Course_Delivery_Mode': 'Normal', 'Free TAFE': 'No',
                       'Subject_or_Unit_1': '', 'Subject_Objective_1': '', 'Subject_Description_1': '',
                       'Subject_or_Unit_2': '', 'Subject_Objective_2': '', 'Subject_Description_2': '',
                       'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
                       'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
                       'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
                       'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
                       'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
                       'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
                       'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
                       'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
                       'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
                       'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
                       'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
                       'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
                       'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
                       'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
                       'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
                       'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
                       'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
                       'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
                       'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
                       'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
                       'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
                       'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
                       'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
                       'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
                       'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
                       'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
                       'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
                       'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
                       'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
                       'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
                       'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
                       'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
                       'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
                       'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
                       'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
                       'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
                       'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
                       'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''
                       }
        driver.get(each_url)
        time.sleep(2)
        pure_url = each_url.strip()
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

        # Find location
        location_tag = []
        locations = location_tag.text.strip()
        actual_cities = []

        for i in possible_cities:
            if i in locations:
                actual_cities.append(i)

        if len(actual_cities) == 1 and "External" in actual_cities:
            course_data['Offline'] = "No" \
                                     ""
        # check duplicate city
        actual_cities = list(dict.fromkeys(actual_cities))

        # Find Duration Value
        duration_tag = details[0].find('dd').find_next('dd').text.strip()
        duration_text = re.sub(r'\s+', ' ', duration_tag)
        duration = duration_text[:duration_text.index(' ')]
        course_data['Duration'] = duration

        # Find full time, part time
        if "full-time" in duration_text:
            course_data['Full_Time'] = "Yes"
        elif "only available as part-time study" in duration_text:
            course_data['Part_Time'] = "Yes"
        else:
            course_data['Full_Time'] = 'Yes'
            course_data['Part_Time'] = 'Yes'
            course_data['Blended'] = 'Yes'

        # Find Description


        # Find career outcomes
        career_tag = []

        # Find Subject
        subjects = []
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

        # Find Faculty

        for i in actual_cities:
            course_data['City'] = i
            print(i)
            dict_writer.writerow(course_data)
        del actual_cities
driver.close()
output_file.close()
