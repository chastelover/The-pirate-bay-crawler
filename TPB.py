from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from multiprocessing.dummy import Pool
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from config import *
import time
import re
import json
import pymongo

#path = PATH
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
isexplicit = ISEXPLICIT
mode = MODE
recent_url = RECENT_URL


def choose_one_format(browser,format):
    if (format == 'all'):
        button = browser.find_element_by_name('all')
        ActionChains(browser).move_to_element(button).click(button).perform()
    if (format == 'audio'):
        button = browser.find_element_by_name('audio')
    if (format == 'video'):
        button = browser.find_element_by_name('video')
    if (format == 'apps'):
        button = browser.find_element_by_name('apps')
    if (format == 'games'):
        button = browser.find_element_by_name('games')
    if (format == 'porn'):
        button = browser.find_element_by_name('porn')
    if (format == 'other'):
        button = browser.find_element_by_name('other')
    ActionChains(browser).move_to_element(button).click(button).perform()


def get_search_result(url,format,content):

    try:
        if(isexplicit):
            browser = webdriver.Chrome()
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        browser.get(url)
        input = browser.find_element_by_css_selector("input[name='q'][type='search']")
        input.send_keys(content)
        choose_one_format(browser, format)
        button = browser.find_element_by_name('search')
        ActionChains(browser).move_to_element(button).click(button).perform()
        wait = WebDriverWait(browser, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))
        time.sleep(1)
        return browser.page_source
    except TimeoutError:
        print("timeout")


def get_recent_torrents_url(url):
    try:
        if (isexplicit):
            browser = webdriver.Chrome()
        else:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        browser.get(url)
        button = browser.find_element_by_xpath("/html/body[@id='home']/header/nav/section[2]/a[2]")
        ActionChains(browser).move_to_element(button).click(button).perform()
        wait = WebDriverWait(browser, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'row')))
        time.sleep(1)
        #return browser.page_source
        return browser.current_url
        #new_url = browser.current_url+ ':' +str(offset)
    except TimeoutError:
        print("timeout")


def turn_page(url):
    #new_url = url + ':' +str(offset)
    if (isexplicit):
        browser = webdriver.Chrome()
    else:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    browser.get(url)
    return browser.page_source


def find_items(source):
    pattern = re.compile(r'.*?id="st">\n.*?item-title">.*?>(.*?)</a>.*?item-uploaded">(.*?)</span>'
                         + r'.*?"item-icons".*?href="(.*?)".*?item-size">(\d+.\d+)\S\w+\S(\w+).*?', re.S)
    items = re.findall(pattern, source)
    for item in items:
        yield{
            'title':item[0],
            'uploadtime':item[1],
            'magnet':item[2],
            'size':item[3]+item[4]
        }

    """
    for magnet in magnets:
        onlymagnet = magnet
        #print(onlymagnet)
        with open('./magnetlink/magnetname.txt','a')as f:
            f.write(onlymagnet+'\n')
    """


def write_to_file(content):
    filename = FILENAME
    with open('./magnetlink/' + filename ,'a',encoding='utf-8')as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')


def save_to_mongo(content):
    if db[MONGO_TABLE].insert(content):
        #print(('存储成功'))
        return True
    return False


def main(offset):
    url = URL
    format = FORMAT
    content = CONTENT
    if(mode == 'search'):
        source = get_search_result(url,format,content)
    if(mode == 'recent'):
        new_url = recent_url + ':' + str(offset)
        source = turn_page(new_url)
    for item in find_items(source):
        #print(item)
        #write_to_file(item)
        save_to_mongo(item)


if __name__ == '__main__':
    if(mode=='recent'):
        pool = Pool()
        pool.map(main,[i for i in range(3)])
    if(mode == 'search'):
        main(0)


"""
if __name__ == '__main__':
    if(mode == 'recent'):
        for i in  range(6):
            main(offset=i)
    if(mode == 'search'):
        main()
"""