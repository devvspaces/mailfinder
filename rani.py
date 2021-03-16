import requests
from bs4 import BeautifulSoup
from requests import Session
from robobrowser import RoboBrowser
from lxml import html

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys





session = Session()
useragent = 'Mozilla/5.0 (Linux; Android 4.4; Nexus 5 Build/_BuildID_) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'
browser = RoboBrowser(user_agent=useragent, session=session, parser='html.parser', history=True)

url = 'https://web.facebook.com/events/172698764285893'
cl='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 a8c37x1j p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl l9j0dhe7 abiwlrkh p8dawk7l'
cd = 'bo bp bq'
imgc = 'ji94ytn4 r9f5tntg d2edcug0 r0294ipz'

FB_EMAIL = '09033295156'
FB_PASSWORD = 'alakio12345@#2*6*7*0*8'

def login():
    try:
        print('Logging in to facebook...')
        browser.open("https://facebook.com") # Facebook profile's language need to be EN-US!
        login_form = browser.get_form(id='login_form')
        login_form['email'].value = FB_EMAIL
        login_form['pass'].value = FB_PASSWORD
        browser.submit_form(login_form)
    except Exception as e:
        print(str(e))

# Login facebook with selenium webdriver
driver = webdriver.Chrome('/Users/HP6460B/Downloads/driver_all/chromedriver')
# driver.get('http://www.facebook.com')^

# username = driver.find_element_by_id('email')
# username.send_keys(FB_EMAIL)
# sleep(0.5)

# password = driver.find_element_by_id('pass')
# password.send_keys(FB_PASSWORD)
# sleep(0.5)

# sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
# sign_in_button.click()
# sleep(0.5)

print('Scraping link started')
driver.get(url)
sleep(5)


print('Scrape complete')


link=driver.find_element_by_xpath("//a[@rel='theater']")
# print(link, link.get_attribute('href'))
# link=driver.find_element_by_css_selector('div.'+'uiScaledImageContainer')
link.click()
sleep(10)


# Getting the image now
#
img=driver.find_element_by_xpath("//img[@class='spotlight']")
print(img.get_attribute('src'))