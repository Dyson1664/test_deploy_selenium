from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import WebDriverException


from flask import render_template
app = Flask(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import os
import psutil
process = psutil.Process(os.getpid())
def sel():
    print('a')
    options = webdriver.ChromeOptions()
    print('b')
    options.add_argument('--headless')  # corrected from '--headless=new' to '--headless'
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    print('c')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    print('d')
    try:
        driver.set_page_load_timeout(30)  # Set a reasonable timeout for page load
        driver.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=CAD')
    except WebDriverException as e:
        print(f"Exception during page load: {e}")
        driver.quit()
        return "Failed to load page"
    print('e')
    try:
        # Attempt to print the page title
        print(driver.title)
    except Exception as e:
        print(f"Failed to get title: {str(e)}")

    try:
        # Wait for the element to be visible before attempting to interact with it
        element_xpath = '//*[@id="__next"]/div[4]/div[2]/section/div[2]/div/main/div/div[2]/div[1]/div/p[2]'
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath))
        )
        cad_text = element.text
    except NoSuchElementException:
        print("Element not found")
        cad_text = "Element not found"
    except TimeoutException:
        print("Timed out waiting for page elements to load")
        cad_text = "Timed out"
    finally:
        driver.quit()  # Ensure the driver is quit properly even if an error occurs

    return cad_text


def wiki():
    options = webdriver.ChromeOptions()
    print('b')
    options.add_argument('--headless=new')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    print('c')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    print('d')
    try:
        driver.set_page_load_timeout(30)  # Set a reasonable timeout for page load
        driver.get('https://en.wikipedia.org/wiki/Main_Page')
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="mp-tfa"]/p/b[1]/a'))
        )
        cad_text = element.text
    except WebDriverException as e:
        print(f"Exception during page load: {e}")
        driver.quit()
        return "Failed to load page"

    return cad_text
# print(cad.text)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print('0')
        if request.form['submit_button'] == 'Do Something':
            print('1')
            # cad_text = sel()
            cad_text = wiki()
            print('2')
            print(cad_text, 'llllll')
            return redirect(url_for('caps', cad_text=cad_text))
    print('hiya')
    return render_template('home.html')

@app.route('/caps')
def caps():
    cad_text = request.args.get('cad_text', 'Default Value if None')
    return render_template('caps.html', cad_text=cad_text)


