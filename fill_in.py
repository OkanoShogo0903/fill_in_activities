#from selenium import webdriver
#driver = webdriver.Chrome()
#driver.get("https://qiita.com/Taro56/items/7cb048f5e8e8bae192e0")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)
#driver.get('http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546')
driver.get('https://trello.com/b/lSPupn89/robocup2018-montr%C3%A9al-canada')
print(driver.page_source)

