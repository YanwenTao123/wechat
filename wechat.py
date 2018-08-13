import time
import re
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
from os import path
from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
from config import *


# PLATFROM = PLATFROM
# DEVICE_NAME = DEVICE_NAME
# APP_PACKAGE = APP_PACKAGE
# APP_ACTIVITY = APP_ACTIVITY
# DRIVER_SERVER = 'http://localhost:4723/wd/hub'
# TIMEOUT = 300
# MONGO_DB = 'moments'
# MONGO_COLLECTION = 'moments'
# MONGO_COLLECTION_OWN = 'own'
# FLICK_START_X = 300
# FLICK_START_Y = 300
# FLICK_DISTANCE = 700


class Moments():
    """朋友圈动态"""
    def __init__(self):
        self.desired_caps = {
            "platformName": PLATFROM,
            "deviceName": DEVICE_NAME,
            "appPackage": APP_PACKAGE,
            "appActivity": APP_ACTIVITY
            }
        self.driver = webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        self.wait = WebDriverWait(self.driver,TIMEOUT)
        self.msg = {}
        self.client = pymongo.MongoClient(host=HOST,port=PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def login(self):
        stoage_ =  self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.android.packageinstaller:id/permission_allow_button')))[0].click()
        phone_ =  self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.android.packageinstaller:id/permission_allow_button')))[0].click()
        login = self.wait.until(EC.presence_of_all_elements_located((By.ID,"com.tencent.mm:id/d75")))[0].click()
        qqform = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/c1t')))[0].click()
        phone = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/hz')))[0].set_text(WEIXIN)
        password = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/hz')))[1].set_text(PASSWORD)
        denglu = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/c1u')))[0].click()
        time.sleep(10)
        self.driver.back()
        TouchAction(self.driver).tap(x=936, y=1669).perform()
        time.sleep(30)
        TouchAction(self.driver).tap(x=680, y=1697).perform()
        time.sleep(1)
        TouchAction(self.driver).tap(x=567, y=346).perform()
        time.sleep(0.5)

    def crawl(self):
        time.sleep(3)
        while True:
            d = {}
            self.driver.swipe(FLICK_START_X,FLICK_START_Y+FLICK_DISTANCE,FLICK_START_X,FLICK_START_Y)
            time.sleep(3)
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/dkc')))
            print(items)
            for item in items:
                try:
                    if item.find_element_by_id('com.tencent.mm:id/as6'):
                        nickname = item.find_element_by_id('com.tencent.mm:id/as6').get_attribute("text")
                        d['nickname'] = nickname
                    else:
                        d['nickname'] = 'NA'
                except:
                    d['nickname'] = 'NA'
                try:
                    if item.find_element_by_id('com.tencent.mm:id/ib'):
                        text = item.find_element_by_id('com.tencent.mm:id/dkf').get_attribute("text")
                        d['text'] = text
                    else:
                        d['text'] = 'NA'
                except:
                    d['text'] = 'NA'
                    pass
                if  d['text'] == 'NA' and  d['nickname'] == 'NA':
                    pass
                else:
                    try:
                        self.collection.insert(d)
                    except Exception as e:
                        print(e)

class Own():
    """自己的动态"""
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "FRD_AL10",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI"
            }
        self.driver = webdriver.Remote(DRIVER_SERVER,self.desired_caps)
        self.wait = WebDriverWait(self.driver,TIMEOUT)
        self.msg = {}
        self.client = pymongo.MongoClient(host=HOST,port=PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION_OWN]

    def login(self):
        stoage_ =  self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.android.packageinstaller:id/permission_allow_button')))[0].click()
        phone_ =  self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.android.packageinstaller:id/permission_allow_button')))[0].click()
        login = self.wait.until(EC.presence_of_all_elements_located((By.ID,"com.tencent.mm:id/d75")))[0].click()
        qqform = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/c1t')))[0].click()
        phone = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/hz')))[0].set_text(WEIXIN)
        password = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/hz')))[1].set_text(PASSWORD)
        denglu = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/c1u')))[0].click()
        time.sleep(10)
        self.driver.back()
        TouchAction(self.driver).tap(x=936, y=1669).perform()
        time.sleep(30)
        TouchAction(self.driver).tap(x=680, y=1697).perform()
        time.sleep(1)
        TouchAction(self.driver).tap(x=567, y=346).perform()
        time.sleep(1)
        TouchAction(self.driver).tap(x=877, y=925).perform()
        print("2222222")

    def crawl(self):
        time.sleep(3)
        while True:
            d = {}
            self.driver.swipe(FLICK_START_X,FLICK_START_Y+FLICK_DISTANCE,FLICK_START_X,FLICK_START_Y)
            time.sleep(3)
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID,'com.tencent.mm:id/dem')))
            print(items)
            for item in items:
                try:
                    if item.find_element_by_id('com.tencent.mm:id/dgh'):
                        day = item.find_element_by_id('com.tencent.mm:id/dgh').get_attribute("text")
                        d['day'] = day
                    else:
                        d['day'] = 'NA'
                except:
                    d['day'] = 'NA'
                try:
                    if item.find_element_by_id('com.tencent.mm:id/dgi'):
                        month = item.find_element_by_id('com.tencent.mm:id/dgi').get_attribute("text")
                        d['month'] = month
                    else:
                        d['month'] = 'NA'
                except:
                    d['month'] = 'NA'
                try:
                    if item.find_element_by_id('com.tencent.mm:id/ib'):
                        text = item.find_element_by_id('com.tencent.mm:id/ib').get_attribute("text")
                        d['text'] = text
                    else:
                        d['text'] = 'NA'
                except:
                    d['text'] = 'NA'
                try:
                    if item.find_element_by_id('com.tencent.mm:id/cm'):
                        address = item.find_element_by_id('com.tencent.mm:id/cm').get_attribute("text")
                        d['address'] = address
                    else:
                        d['address'] = 'NA'
                except:
                    d['address'] = 'NA'
                print(d)
                if  d['text'] == 'NA' and  d['day'] == 'NA' and d['month'] == 'NA':
                    pass
                else:
                    try:
                        self.collection.insert(d)
                    except Exception as e:
                        print(e)

class Dataviews():
    """数据可视化"""
    def __init__(self):
        self.client = pymongo.MongoClient(host=HOST, port=PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]
        self.collection_own= self.db[MONGO_COLLECTION_OWN]

    def get_img(self):
        """朋友圈情绪词云"""
        text = ''
        result = self.collection.find({}, {"text": 1, "_id": 0})
        for i in result:
            text += i["text"]
        with open('text.txt', 'w', encoding='utf8') as fp:
            fp.write(text)
        mulu = path.dirname(__file__)
        text = open('text.txt','r',encoding='utf8').read()
        lst = re.findall('\[([\s\S]*?)\]',text)
        lst_str = ' '.join(lst)
        print(lst_str)
        # 通过jieba处理文本
        # seg_list = jieba.cut(text, cut_all=True)
        # seg_split = " ".join(seg_list)
        # print(seg_split)
        wordcloud_mask = np.array(Image.open(path.join(mulu, 'lou.jpg')))
        font = path.join(mulu, 'simhei.ttf')
        wc = WordCloud(font_path=font,background_color="white", max_words=2000, mask=wordcloud_mask)
        wc.generate(lst_str)
        wc.to_file(path.join(mulu, "pengyouquan_emj.jpg"))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def get_name(self):
        """朋友圈好友出镜率"""
        mulu = path.dirname(__file__)
        name_list = self.collection.find({},{"nickname":1,"_id":0})
        with open('text.txt','w',encoding='utf8') as fp:
            for i in name_list:
                if i["nickname"] != 'NA':
                    fp.write(i['nickname']+" ")
        with open('text.txt','r',encoding='utf8') as fp:
            lst_str = fp.read()
        print(lst_str)
        word_mask = np.array(Image.open(path.join(mulu, 'lou.jpg')))
        font = path.join(mulu, 'simhei.ttf')
        wc = WordCloud(font_path=font, background_color="white", max_words=2000, mask=word_mask)
        wc.generate(lst_str)
        wc.to_file(path.join(mulu, "friend_name.jpg"))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis("off")
        plt.show()




if __name__ == "__main__":
    # 朋友圈动态
    # pengyouquan = Moments()
    # pengyouquan.login()
    # pengyouquan.crawl()
    # 自己动态
    # own = Own()
    # own.login()
    # own.crawl()
    # 词云展示
    views = Dataviews()
    views.get_img()
    # views.get_name()






