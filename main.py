import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time


url = 'https://qavanin.ir/'

driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)


def switch_to_end_tab():
    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])


def close_tabs():
    if len(driver.window_handles) == 1:
        return
    else:
        switch_to_end_tab()
        driver.close()
        close_tabs()


def next_page(pagenumber):
    next = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[2]/tbody/tr/td[1]/select')
    nextnumber = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[2]/tbody/tr/td[1]/select/option[' + str(pagenumber) + ']')
    next.click()
    nextnumber.click()
    time.sleep(random.random().real)


def save_csv(laws):
    # print('laws:', laws)
    print('save data')
    df = pd.DataFrame(laws, columns=['title', 'date', 'authority', 'link', 'desc'])
    # , index=[law[0] for law in laws])
    df.to_csv('laws.csv', encoding='utf-8-sig')



laws = []
try:
    pages = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[2]/tbody/tr/td[3]/select')
    page1000 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[2]/tbody/tr/td[3]/select/option[6]')
    pages.click()
    page1000.click()
    # time.sleep(random.random().real)
    # len_law = int(page1000.text)
    len_law = 1000
    pagenumbers = 155

except Exception as e:
    len_law = 25
    pagenumbers = 6171
    print('\nerror:', e)

print('len laws:', len_law)


try:
    for pagenumber in range(3, pagenumbers):
        next_page(pagenumber)
        for i in range(100, len_law+1):
            link = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[1]/tbody[1]/tr[' + str(i) + ']/td[2]/a')
            date = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[1]/tbody[1]/tr[' + str(i) + ']/td[3]')
            authority = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/form/table[1]/tbody[1]/tr[' + str(i) + ']/td[4]')

            link.click()
            switch_to_end_tab()
            time.sleep(random.random().real)

            try:
                treeText = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div[2]/div/form/div/table/tbody/tr/td[2]/div')
                desc = treeText.text.replace("\n", " ")
            except Exception as e:
                desc = ''
                print('\nerror:', e)

            close_tabs()
            switch_to_end_tab()
            time.sleep(random.random().real)

            law = [link.text, date.text, authority.text, link.get_attribute('href'), desc]
            print(law, i)
            laws.append(law)

            if i % 50 == 0:
                save_csv(laws)

except Exception as e:
    print('\nerror:', e)


save_csv(laws)
driver.quit()