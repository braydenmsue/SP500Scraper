from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# installs chromedriver so there is no need to include paths
chromedriver_autoinstaller.install()

# set driver to access s&p500 table and maximise the window
driver = webdriver.Chrome()
website = 'https://markets.businessinsider.com/index/components/s&p_500'
driver.get(website)
driver.maximize_window()

# Find last page number to determine amount of loops for pagination
pagination = driver.find_element(By.XPATH, "//div[@class = 'finando_paging margin-top--small']")
pages = pagination.find_elements(By.TAG_NAME, 'a')
lastPage = int(pages[-2].text)
print("last page = ", lastPage)

# initialise lists
date = []
company = []
percentChange = []
currentPage = 1

while currentPage <= lastPage:
    table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@class = 'table__tbody']")))
    stocks = WebDriverWait(table, 10).until(EC.presence_of_all_elements_located((By.XPATH, './tr')))

    for stock in stocks:
        date.append(stock.find_element(By.XPATH, './td[5]').text.replace('\n', ' '))
        company.append(stock.find_element(By.XPATH, './td[1]').text)
        percentChange.append(stock.find_element(By.XPATH, './td[4]').text.replace('\n', ' ').split()[-1])

    # Only scrape first page until pagination is fixed
    currentPage = lastPage+1

# No next button on this website, pagination is a WIP
    # currentPage += 1
    # nextPageXPATH = "//a[text()[contains(.,'" + str(currentPage) + "')]]"
    # try:
    #    nextPage = pagination.find_element(By.XPATH, nextPageXPATH)
    #    nextPage.click()
    # except:
    #    pass


# Create pandas dataframe from a dictionary
df = pd.DataFrame({'Date & Time': date, 'Company Name': company, 'Percent Change': percentChange})

# save as .csv file
df.to_csv('stock_data.csv', index=False)

