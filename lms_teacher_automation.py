import os
import time
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from database import PostgreSQL
import chrome_version
import platform

timeout_limit = 200 # Set time out of waiting the page and element is detected
alert_timeout_limit = 15
timesleep = 1
web_address_lms_teacher = "https://lms-teacher.sokrates.xyz/"

os_system = platform.system()

chrome_options = Options()
# chrome_options.add_argument('--headless') # Comment this line if want to show Chrome GUI
# chrome_options.add_argument('--disable-gpu') # Comment this line if want to show Chrome GUI

print('Running on '+os_system)
chrome_version = "v"+chrome_version.get_chrome_version().split(".")[0] # Identified Chrome browser version. Chromedriver must be the same
# print('Running on '+chrome_version)

# set path ke file chromedriver to operate the Chrome browser.
if os_system == 'Windows':
    chrome_path = os.path.join('webdriver', 'chrome', os_system, chrome_version, 'chromedriver.exe')
elif os_system == 'Linux':
    chrome_path = os.path.join('webdriver', 'chrome', os_system, chrome_version, 'chromedriver')
else:
    chrome_path = os.path.join('webdriver', 'chrome', 'MacOS', chrome_version, 'chromedriver')

db = PostgreSQL(database='sokrates_dev_student') # Select the database

# Start to connect to Sokrates PostgreSQL Server
def get_data():
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student where student_id in (28799,15767)") # Select student table to load the data
    rows = cursor.fetchall()
    cursor.close()
    return rows

data = get_data()
# data = []

if(len(data) > 0) :
# if(len(data) == 0) :
    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    # Open the URL contains a form to be automated filling
    wait_page = WebDriverWait(driver, timeout_limit)
    driver.get(web_address_lms_teacher+"auth/login")

    wait_page.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    # Make sure that the URL page is open completely
    if 'SokratesLmsTeacherFrontend' in driver.page_source :
        button_fqdn = WebDriverWait(driver, timeout_limit).until(
                EC.presence_of_element_located((By.XPATH, '//nb-icon[@icon="settings-outline"]')))

        if button_fqdn:
            print('Button FQDN detected')
            button_fqdn.click()

            fqdn_tenant = WebDriverWait(driver, timeout_limit).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="fqdn"]')))

            fqdn_go = WebDriverWait(driver, timeout_limit).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text()," GO ") and @class="appearance-ghost size-medium shape-rectangle status-basic nb-transition"]')))

            fqdn_go_click = WebDriverWait(driver, timeout_limit).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text()," GO ") and @class="appearance-ghost size-medium shape-rectangle status-basic nb-transition"]')))

            if fqdn_tenant and fqdn_go:
                print('FQDN Tenant and Button Go detected')

                fqdn_tenant.send_keys('sokrates.api.sokrates.xyz')
                fqdn_go_click.click()

                wait_page.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

                username = WebDriverWait(driver, timeout_limit).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="username"]')))

                password = WebDriverWait(driver, timeout_limit).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
                
                btn_login = WebDriverWait(driver, timeout_limit).until(
                    EC.presence_of_element_located((By.XPATH, '//button[contains(text()," LOGIN ") and @class="appearance-filled full-width btn-disabled size-medium shape-rectangle status-primary nb-transition"]')))
                
                if username and password :
                    print('username and password detected')

                    username.send_keys("sokrates")
                    password.send_keys("password123")

                    btn_login.click()
                    wait_page.until(lambda driver: driver.execute_script("return document.readyState") == "complete")

                    icon_category = WebDriverWait(driver, timeout_limit).until(
                        EC.presence_of_element_located((By.XPATH, '//a[@title="Category" and @class="ng-tns-c135-1 ng-star-inserted"]')))
                    
                    if icon_category :
                        print('icon category detected')
                        icon_category.click()

                        for row in data:
                            wait_page.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                            button_add_category = WebDriverWait(driver, timeout_limit).until(
                                EC.presence_of_element_located((By.XPATH, '//button[contains(text()," Add Category ") and @class="status-success appearance-filled size-medium shape-rectangle ng-star-inserted nb-transition"]')))
                            
                            if button_add_category:
                                print("Button add category detected")
                                button_add_category.click()
                                wait_page.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                                
                                input_category = WebDriverWait(driver, timeout_limit).until(
                                    EC.presence_of_element_located((By.XPATH, '//input[@id="category_name" and @formcontrolname="category_name"]')))
                                
                                input_colour = WebDriverWait(driver, timeout_limit).until(
                                    EC.presence_of_element_located((By.XPATH, '//input[@class="input-full-width size-medium status-basic shape-rectangle nb-transition"]')))
                                
                                if input_category and input_colour:
                                    print("Input category and input colour detected")

                                    input_category.send_keys(row[2])
                                    input_colour.send_keys("#000000")
                                    input_colour.send_keys(Keys.ENTER)
                                else:
                                    print("Input category and input colour not detected")
                            else:
                                print("Button add category not detected")
                    else:
                        print('icon category not detected')
                else :
                    print('username and password not detected')
            else:
                print('FQDN Tenant and Button Go not detected')
        else:
            print('Button FQDN not detected')
    else:
        print('Web not found');
# After all data is stored and submitted, then close the DB Connection from Sokrates PostgreSQL database
db.close_connection()