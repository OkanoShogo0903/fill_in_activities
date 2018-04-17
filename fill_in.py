#from selenium import webdriver
#driver = webdriver.Chrome()
#driver.get("https://qiita.com/Taro56/items/7cb048f5e8e8bae192e0")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
#options.add_argument('--headless') # headlessにする方法
#options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)
#driver.get('http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546')

# Trelloのログイン画面に移動
driver.get('https://trello.com/login?returnUrl=%2Fb%2FlSPupn89%2Frobocup2018-montr%25C3%25A9al-canada')

time.sleep(1)

# ID/PASSを入力
id = driver.find_element_by_id('user')
id.send_keys('okano')
password = driver.find_element_by_id('password')
password.send_keys('shogo')

time.sleep(1)

# ログインボタンをクリック
#login_button = driver.find_element_by_name("login")
#login_button.click()

# サイト内で他の画面に遷移させたければ
driver.get('https://trello.com/b/lSPupn89/robocup2018-montr%C3%A9al-canada')

print(driver.page_source)
