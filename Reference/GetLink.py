import csv


def write_link(subject_list, file):
    links = []

    with open(file, 'at', encoding='UTF-8', newline='') as List:
        writer = csv.writer(List)

        for name in subject_list:
            for cell in name.find_all('a'):
                link = cell.get('href')
                # writer.writerow([link])
                links.append(link)
        List.close()

    return links

"""
# Find the existence of next button then trigger the button for next page result
while not end_result:

    driver.implicitly_wait(100)
    time.sleep(1)

    # Get page soup
    each_url = driver.page_source
    soup = bs4.BeautifulSoup(each_url, 'html.parser')

    # Find the course link
    target_link_tag = soup.find('div', {'class': 'grid spacing--bottom-xxl'})
    for link in target_link_tag.find_all('a'):
        course_links.append(link.get('href'))
    print(course_links)

    # set delay for the page to load
    driver.implicitly_wait(100)

    # test
    if driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[5]').text == "…":
        button = driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[6]/a')
        button.click()
    else:
        if driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[7]').text == "…":
            button = driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[8]/a')
            button.click()
        elif driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[8]').text == "…":
            button = driver.find_element_by_xpath('//*[@id="programs"]/nav/ul/li[9]/a')
            button.click()

        else:
            end_result = True

    driver.implicitly_wait(45)
"""