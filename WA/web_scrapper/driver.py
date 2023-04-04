username = "8928393524"
passwd = "#JvBsSA@23"
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

# initialize the Chrome driver
driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")

# navigate to Facebook login page
driver.get("https://www.facebook.com")

# locate the email and password fields
email_field = driver.find_element(By.ID, "email")
password_field = driver.find_element(By.ID, "pass")

# enter email and password
email_field.send_keys(username)
password_field.send_keys(passwd)

# locate the login button and click it
login_button = driver.find_element(By.NAME, "login")
login_button.click()

time.sleep(2000)
