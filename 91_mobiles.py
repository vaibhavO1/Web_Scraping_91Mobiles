from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Define the driver path
driver_path = Service("C:/chromedriver.exe")

# Set the different options for the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Ignore the certificate and SSL errors
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
                             
# Maximize the browser window
chrome_options.add_argument("start-maximized")

# Define the driver and open the browser
chrome_driver = webdriver.Chrome(service=driver_path, options=chrome_options)

chrome_driver.get('http://google.com')
time.sleep(1)

# fetch the search input box using xpath
user_input = chrome_driver.find_element(by=By.XPATH, value='//*[@id="APjFqb"]')
user_input.send_keys('91 Mobiles')
time.sleep(1)

user_input.send_keys(Keys.ENTER)
time.sleep(1)

chrome_driver.find_element(by=By.XPATH, value='//*[@id="rso"]/div[1]/div/div/div/div/div/div/div/div[1]/div/span/a/div/div/div/div[2]/cite').click()
time.sleep(1)

chrome_driver.find_element(by=By.XPATH, value='//*[@id="mobile"]/ul/li[2]/span').click()
time.sleep(1)

chrome_driver.find_element(by=By.XPATH, value='/html/body/div[4]/div/div[1]/div[2]/ul/li[1]/a').click()
time.sleep(1)

chrome_driver.execute_script('window.scrollBy(0, 5000)')
time.sleep(2)

html = chrome_driver.page_source
soup = BeautifulSoup(html,'lxml')

name=[]
rating=[]
price=[]
os=[]
data1=[]
data2=[]

for i in soup.find_all('div', class_='finder_snipet_wrap'):
  try:
    name.append(i.find('a', class_='hover_blue_link name gaclick').text.strip())
  except:
    name.append(np.nan)  

  try:
    rating.append(i.find('div', class_='various3 fancybox.iframe pointer gaclick').text.strip())
  except:
    rating.append(np.nan)  

  try:
    os.append(i.find('div', class_='os_icon_cat').text.strip())
  except:
    os.append(np.nan)     
 
  try:
    try:
      price.append(i.find('span', class_='price price_padding').text.strip())
    except:
      price.append(i.find('span', class_='price price_float').text.strip())   
  except:
    price.append(np.nan)      

  try:
    data1.append(i.find('div', class_='filter-grey-bar filter_gray_bar_margin grey_bar_custpage').text.strip())
  except:
    data1.append(np.nan)      

  try:
    s = ''
    temp = str(i.find('div', class_='filter filer_btm_margin'))
    # Parse the HTML using BeautifulSoup
    t_soup = BeautifulSoup(temp, 'lxml')

    # Extract and print the data-title values
    for element in t_soup.find_all(['div', 'span'], {'data-title': True}):
      s = s + str(element['data-title'])
    data2.append(s)  
  except:
    data2.append(np.nan)

# with open('91_mobiles.html','w',encoding='utf-8') as f:
#     f.write(html)

chrome_driver.find_element(by=By.XPATH, value='//*[@id="finder_pagination"]/div/div[2]/span').click()
time.sleep(2)

while True:

    try:
        chrome_driver.execute_script('window.scrollBy(0, 4500)')
        time.sleep(2)
        
        html = chrome_driver.page_source
        soup = BeautifulSoup(html,'lxml')

        for i in soup.find_all('div', class_='finder_snipet_wrap'):
            try:
                name.append(i.find('a', class_='hover_blue_link name gaclick').text.strip())
            except:
                name.append(np.nan)  

            try:
                rating.append(i.find('div', class_='various3 fancybox.iframe pointer gaclick').text.strip())
            except:
                rating.append(np.nan)  

            try:
                os.append(i.find('div', class_='os_icon_cat').text.strip())
            except:
                os.append(np.nan)     
            
            try:
              try:
                price.append(i.find('span', class_='price price_padding').text.strip())
              except:
                price.append(i.find('span', class_='price price_float').text.strip())   
            except:
              price.append(np.nan)      

            try:
                data1.append(i.find('div', class_='filter-grey-bar filter_gray_bar_margin grey_bar_custpage').text.strip())
            except:
                data1.append(np.nan)      

            try:
                s = ''
                temp = str(i.find('div', class_='filter filer_btm_margin'))
                # Parse the HTML using BeautifulSoup
                t_soup = BeautifulSoup(temp, 'lxml')

                # Extract and print the data-title values
                for element in t_soup.find_all(['div', 'span'], {'data-title': True}):
                    s = s + str(element['data-title'])
                data2.append(s)  
            except:
                data2.append(np.nan)

        # with open('91_mobiles.html','a',encoding='utf-8') as f:
        #     f.write(html)

        chrome_driver.find_element(by=By.XPATH, value='//*[@id="finder_pagination"]/div/div[4]/span').click()
        time.sleep(2)

        
    except:
        break

df=pd.DataFrame({'Mobile':name,
  'Spec_Score':rating,
  'Operating_System':os,
  'Price':price,
  'Per_Dis_Cam_Bat':data1,
  'Other_Features':data2,
  })

df.to_csv('91_mobiles_2.csv', index=False)