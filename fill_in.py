# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
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
driver.set_window_size(width=150,height=400)
plain_trello_email = ""
plain_trello_pass = ""
# 個人の方じゃないと、<comment-box-input js-text>がない
trello_individual_comment_url = 'https://trello.com/c/7uDgTT3s/51-%E5%B2%A1%E9%87%8E'
#trello_individual_comment_url = 'https://trello.com/c/aIBEyEDk/21-bot%E3%83%86%E3%82%B9%E3%83%88'
trello_login_url = 'https://trello.com/login?returnUrl=%2Fb%2FlSPupn89%2Frobocup2018-montr%25C3%25A9al-canada'
trello_api_url = 'https://trello.com/app-key'
trello_token_url = ['https://trello.com/1/authorize?key=<','>&name=&expiration=never&response_type=token&scope=read,write']
latest_time_stamp = None
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


def loadTimeStamp():
    '''Load latest time stamp and set variable'''
    global latest_time_stamp
    pattern = r'(LatestTimeStamp\s*:\s*)' # 雛形に合わせてデータを取ってくる
    with open('./internal_data.txt') as f:
        for line in f: 
            phrase = re.match(pattern, line)
            if phrase != None:
                time_string = line[phrase.end():-1] # 2018.1.1.0.0
                string_list = time_string.split('.')
                num_list = [int(s) for s in string_list]
                #print(num_list)
                latest_time_stamp = datetime.date(*num_list) # リストを展開して渡す
                print("latest time stamp :",latest_time_stamp)
# [END LoadFunction]


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
    driver.get(trello_individual_comment_url)
    time.sleep(1.5)

    #print(driver.page_source)
# [END LoginFunction]


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
    

def getTrelloScraping():
    surround_pattern = r'(trello_email\s*:\s*)'

    res = driver.page_source.encode('utf-8')
    my_soup = BeautifulSoup(res, 'lxml') #要素を抽出 html.parser
    main_comment_html = HandClassScraping(res.decode('utf-8')) # <div class="js-list-actions">が閉じられるまでのコードを返す

    comment_soup = BeautifulSoup(main_comment_html, 'lxml')
    # マークダウンのためにhtmlのタグとかついたテキストを持ってくる方法
    #exprains = comment_soup.find_all("div",{"class": "current-comment js-friendly-links js-open-card"})
    # ユーザがTrelloに書いたテキストをそのまま使う方法
    exprains = comment_soup.find_all("textarea",{"class": "comment-box-input js-text"})

    #print("exprains :",type(exprains)) # <class 'bs4.element.ResultSet'>
    #print(exprains) # 一つの投稿に関する投稿者や投稿時間等のデータの集まりのリスト(のようなものby BeautifulSoup公式)
    #print("******")

    modify_list = []
    for explain in exprains: # explain : <class 'bs4.element.Tag'>
        # タグを外す
        #print("contents:",type(explain.contents)) # list
        #print("contents:",type(explain.contents[0])) # tag
        #print(explain.contents[0]) # same to str(explain.contents[0])
        string = ''.join(map(str,explain.contents))
        #print(string)
        modify_list.append(string)
        
        #print("*** END ***")
    #print("*** END ***")
    return modify_list
# [END ScrapingFunction]


def isCheckTimeStamp(_date):
    '''
    receive <class 'datatime'>
    コメントに入っている日付情報を見て、更新するべき情報かどうかを確認する
    '''
    if type(_date) == None: # コメントに時刻の記入が無いとき
        return False

    try:
        if latest_time_stamp < _date: # 新しい投稿であるとき
            return True
        else: # 古い投稿であるとき
            return False
    except:
        return False


def isCheckAddress(_str):
    '''
    receive <class 'str'>
    '''
    if _str == None:
        return False
    else:
        return True


class Comment:
    """News infomation class"""
    date_patterns = [\
            re.compile(r'([0-1]?[0-9])(?:/|-|\.)([0-3]?[0-9])'),\
            re.compile(r'([0-1]?[0-9])月([0-3]?[0-9])日?'),\
    ]
    # 4/01 ???
    time_patterns = [\
            re.compile(r'([0-2]?[0-9]):([0-5]?[0-9]) ?(?:~|-) ?([0-2]?[0-9]):([0-5]?[0-9])'),\
    ]
    address_patterns = [\
            re.compile(r'(?:to|To|TO):([a-zA-Z]+)'),\
    ]
    university_pattern = [\
            re.compile(r'(U|u)niv?')
    ]
    private_pattern = [\
            re.compile(r'(P|p)rivate')
    ]
    day_of_the_week_pattern = [\
            re.compile(r' [月火水木金土日]'),\
            re.compile(r'\([月火水木金土日]\)')
    ]

    def __init__(self, _html_string):
        ''' 変数初期化して、引数のテキストから整形とか情報の抽出とかする関数の呼び出す '''
        self.plain_html_text = _html_string
        self.address = 'university' # デフォルトで大学行き
        self.timestamp = None
        self.body_text = None
        self.activity_time = datetime.timedelta()

        self.ExtractInfosFromPlainText()
        self.MarkdownTextToPlainText()


    def ExtractInfosFromPlainText(self):
        '''
        引数のhtmlテキストからタイムスタンプ等の情報を抽出する
        separate to body_text,timestamp,address
        '''
        text = self.plain_html_text # <str>

        # TIME STAMP
        for pattern in self.date_patterns: # re pattern
            obj = pattern.search(text)
            if obj == None:
                pass
                #return -1 # or, raise ERR
            else:
                #print(obj.groups())
                month,day = obj.groups() # taple
                # set timestamp
                year = datetime.date.today().year # int
                self.timestamp = datetime.date(year=year,month=int(month),day=int(day))
        print("time stamp    : ",self.timestamp)

        # ACTIVITY TIME
        for pattern in self.time_patterns: # re pattern
            obj_list = pattern.findall(text)
            for obj in obj_list:
                s_h,s_m,e_h,e_m = obj
                s_time = datetime.timedelta(hours=int(s_h),minutes=int(s_m))
                e_time = datetime.timedelta(hours=int(e_h),minutes=int(e_m))
                self.activity_time += e_time - s_time
        print("activity time : ",self.activity_time)

        # ADDRESS
        for pattern in self.address_patterns: # re pattern
            obj = pattern.search(text)
            if obj == None:
                pass
            else:
                # obj.group example   "to:univ" -> ('univ',)
                #print(obj.groups()) 
                string, = obj.groups() # for catch univ # taple string to plane string
                for p in self.university_pattern + self.private_pattern: # re pattern
                    if p.search(string) != None:
                        self.address = 'university'
                    elif p.search(string) != None:
                        self.address = 'private'
                    #elif :
        print("address       : ",self.address)


    def MarkdownTextToPlainText(self):
        ''' Markdownで書かれたものを活動記録に記入する文に変える '''
        text = self.plain_html_text # <str>
        #modify = re.sub(r"(@[a-zA-Z0-9_]*:)+","",modify)

        # 正規表現のパターンにマッチングする文字列を取り除く
        pattern_markdown = [\
                # 強調 \w \^wを使うか?
                #re.compile(r'\*+(.| )+\*+'),\
                # 顔文字消し
                re.compile(r':(.)+:'),\
                # 見出し消し
                re.compile(r'#+ '),\
                ]
        pattern_sum = \
                self.date_patterns + \
                self.time_patterns + \
                self.address_patterns + \
                self.university_pattern + \
                self.private_pattern + \
                self.day_of_the_week_pattern
        for p in pattern_sum:
            text = re.sub(p,'',text)
        for p in pattern_markdown:
            # 複数のグループに対してそれぞれ本文だけを残して置換する?
            # text = text.replace("*", "") でよくね？
            text = re.sub(p,'', text)

        # 非正規表現のパターンを消してく
        text = text.replace("<br/>", "\n")
        text = text.replace("*", "")

        self.body_text = text
        print(self.body_text)


if __name__=="__main__":
    try:
        loadProfile()
        loadTimeStamp()
        # ココで学校ログイン、だめなら
        #SchoolLogin()
        TrelloLogin(plain_trello_email, plain_trello_pass)
        # ここでエラーでるならsys.exit、タイムスタンプの更新はしないことに注意
        comment_info_list = getTrelloScraping()

        # Create modify data from plain text
        comment_class_list = []
        for s in comment_info_list:
            print('-'*50)
            #print(s) # strっぽいもの
            j = Comment(s)
            comment_class_list.append(j)

        for c in comment_class_list:
            if isCheckAddress(c.address) == True:
                if isCheckTimeStamp(c.timestamp) == True:
                    pass
                    #SendTo
                    # ココらへんで送信する 学校接続エラーのときはタイムスタンプを更新しない
    finally:
        driver.quit()
        #latest_time_stamp = 
