from flask import Flask
from selenium.webdriver.common.by import By

from flask import render_template
app = Flask(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)




driver.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=CAD')
print(driver.title)
cad = driver.find_element(By.XPATH, '//*[@id="__next"]/div[4]/div[2]/section/div[2]/div/main/div/div[2]/div[1]/div/p[2]')

# print(cad.text)
@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/caps')
def caps(name=None):
    return render_template('caps.html', name=name, cad=cad.text)
