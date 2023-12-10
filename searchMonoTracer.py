from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas
import os
import time

def searchMonoTracer(driver : webdriver,i, data_row):
    print('jan:' + data_row[3])
    driver.get('https://www.mono-tracer.com/#/list?q=' + data_row[3])
    time.sleep(5)
    driver.execute_script("window.scrollTo(10,10);") #操作をしないとグラフの描画がされないっぽい？　Maybe webdriver wait to show graph until I touch at webpage.
    time.sleep(2)

    prodauct_names = driver.find_elements(By.CLASS_NAME, "product-name")
    if len(prodauct_names) >= 2:
        name = prodauct_names[1].find_element(By.TAG_NAME, 'a').text
        work_data.iloc[i,4] = name

    price_table = driver.find_elements(By.CLASS_NAME, 'price-table')
    if len(price_table) >= 1 :
        for tabel_row in price_table[0].find_elements(By.TAG_NAME, 'tr'):
            clms = tabel_row.find_elements(By.TAG_NAME, 'td') 
            if clms[0].text == '新品':
                price_new = clms[1].text
                stock_new = clms[2].text
                work_data.iloc[i,5] = price_new
                work_data.iloc[i,6] = stock_new
            if clms[0].text == '中古':
                price_used = clms[1].text
                stock_used = clms[2].text
                work_data.iloc[i,7] = price_used
                work_data.iloc[i,8] = stock_used



driver = webdriver.Chrome()

raw_data = pandas.read_csv('***input_file***', dtype=str)
work_data = raw_data.assign(prodauct_names="").assign(price_new="").assign(stock_new="").assign(price_used="").assign(stock_used="")
print(work_data)

for i, data_row in enumerate(work_data.itertuples()):
    searchMonoTracer(driver ,i ,data_row)

work_data.to_csv('***input_file***')