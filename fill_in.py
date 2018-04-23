# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import types

import requests
from bs4 import BeautifulSoup
# [END LibInstall]

# [START General]
options = Options()
#options.add_argument('--headless') # headlessにする方法
#options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=options)
plain_trello_email = ""
plain_trello_pass = ""
trello_individual_url = 'https://trello.com/c/aIBEyEDk/21-bot%E3%83%86%E3%82%B9%E3%83%88'
trello_login_url = 'https://trello.com/login?returnUrl=%2Fb%2FlSPupn89%2Frobocup2018-montr%25C3%25A9al-canada'
trello_api_url = 'https://trello.com/app-key'
trello_token_url = ['https://trello.com/1/authorize?key=<','>&name=&expiration=never&response_type=token&scope=read,write']
# [END General]

def loadProfile():
    global plain_trello_email,plain_trello_pass
    email_pattern=r'(trello_email\s*:\s*)'
    pass_pattern=r'(trello_pass\s*:\s*)'
    with open('./user_data.txt') as f:
        for line in f: # テキストファイルからメアドとパスワードだけ抽出する
            e = re.match(email_pattern, line)
            p = re.match(pass_pattern, line)
            if e != None:
                plain_trello_email = line[e.end():-1]
            elif p != None:
                plain_trello_pass = line[p.end():-1]
    # dont raise error in mind


def TrelloLogin(_email, _password):
    global driver
    #driver.get('http://vaaaaaanquish.hatenablog.com/entry/2017/06/06/194546')

    # Trelloのログイン画面に移動
    driver.get(trello_login_url)

    # タイムアウトで10秒待つ
    driver.implicitly_wait(10) # seconds
   
    # ID/PASSを入力
    id = driver.find_element_by_id('user')
    id.send_keys(_email)
    password = driver.find_element_by_id('password')
    password.send_keys(_password)

    # ログインボタンをクリック
    login_button = driver.find_element_by_id("login")
    login_button.click()

    time.sleep(1.5)

    # サイト内の個人活動記録画面に遷移
    driver.get(trello_individual_url)
    time.sleep(1.5)

    #print(driver.page_source)


def HandClassScraping(_text):
    '''
    BeautifulSoupだとうまくスクレイピングできなかったので、
    必要なクラスだけ取ってくるように手実装している。
    Trelloの仕様が変わったら即死すると思われるので、
    あまり良くない実装
    '''
    print("*** HandClassScraping ***")
    start_pattern = re.compile(r'<div\sclass=\"js-list-actions\">') # 開いているページのコメント部分全体
    end_pattern = re.compile(r'<\/p><\/div><\/div>') # ここ変えたほうがいい、脆弱
    s = start_pattern.search(_text)
    e = end_pattern.search(_text, pos=s.start())
    #print(s.start())
    #print(e.end())
    useful_part = _text[s.start():e.end()]
    #print(useful_part)

    return useful_part
    

def TrelloScraping():
    surround_pattern = r'(trello_email\s*:\s*)'

    res = driver.page_source.encode('utf-8')
    #print(res)
    #print("*****************")
    my_soup = BeautifulSoup(res, 'lxml') #要素を抽出 html.parser
    #print("*****************")
    main_comment_html = HandClassScraping(res.decode('utf-8'))

    comment_soup = BeautifulSoup(main_comment_html, 'lxml')
    comment_log = comment_soup.find_all("div",{"class": "current-comment js-friendly-links js-open-card"})
    print(type(comment_log))
    #print(comment_log) # 一つの投稿に関する投稿者や投稿時間等のデータの集まりのリスト(のようなものby BeautifulSoup公式)
    #print(comment_log.)
    #print("******")

    #print(window_module.phenom mod-comment-type)
    #print(explains)

    for explain in comment_log:
        print (explain.text) 
    print("*** END ***")


if __name__=="__main__":
    try:
        loadProfile()
        TrelloLogin(plain_trello_email, plain_trello_pass)
        TrelloScraping()
    finally:
        driver.quit()
