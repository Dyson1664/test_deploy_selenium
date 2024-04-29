from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for

from selenium.webdriver.common.by import By

from flask import render_template
app = Flask(__name__)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def sel():
    print('a')
    options = webdriver.ChromeOptions()
    print('b')
    options.add_argument('--headless=new')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    print('c')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    print('d')
    driver.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=CAD')
    print('e')
    print(driver.title)

    element = driver.find_element(By.XPATH,
                                  '//*[@id="__next"]/div[4]/div[2]/section/div[2]/div/main/div/div[2]/div[1]/div/p[2]')
    cad_text = element.text
    driver.quit()
    return cad_text

# print(cad.text)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        print('0')
        if request.form['submit_button'] == 'Do Something':
            print('1')
            cad_text = sel()
            print('2')
            print(cad_text, 'llllll')
            return redirect(url_for('caps', cad_text=cad_text))
    print('hiya')
    return render_template('home.html')

@app.route('/caps')
def caps():
    cad_text = request.args.get('cad_text', 'Default Value if None')
    return render_template('caps.html', cad_text=cad_text)


