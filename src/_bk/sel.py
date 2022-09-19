#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver # ex. pip install selenium==4.0.0a7
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by      import By
from selenium.webdriver.support.ui     import Select
import re
import sys
import time
import urllib.parse

conf = {
    "selenium" : {
        "browser_driver": "./chromedriver",
#        "browser_driver": "/usr/local/bin/chromedriver",
        "browser_options" : [
#            "--headless",
            "--enable-logging=False",
            "--ignore-certificate-errors",
            "--disable-extensions",
            "--disable-print-preview",
            "--download.default_directory=/tmp"
        ],
        "implicitly_wait": 10 }
}

search_url = "https://www.google.co.jp/search"
search_str = urllib.parse.quote("戸建て住宅 間取り図面")
search_params = [
    "q="  + search_str,
    "tbm=isch",
    "hl=ja",
    "sclient=img",
    "ei=7yL2Ypn2MtuM1e8PutqksA0",
    "tbs=itp:clipart",
    "sa=X"]
re_compile = re.compile("\?imgurl=(.[^&]+)")
# 収集する最大url数.
# google検索での最大件数がこの程度でしたので
max_url_size = 5


def main():
    browser = get_browser()

    req_url = search_url +"?" + "&".join(search_params)
    print( req_url )
    browser.get( req_url )
    time.sleep(3)
    
    img_urls = []
    while len(img_urls) <= max_url_size:
        print( len(img_urls), file=sys.stderr )
        img_urls = extract_img_urls( browser, img_urls )
        
    for img_url in img_urls:
        print( img_url )
        

def extract_img_urls( browser, img_urls ):
    a_elms = browser.find_elements(by=By.CSS_SELECTOR,
                                   value="a.wXeWr")
    i = len( img_urls )
    while i < len( a_elms ):
        a_elm = a_elms[i]
        
        try:
            # clickすることで、auto pagerize します
            a_elm.click()
            href_url =  a_elm.get_attribute("href")
        except Exception as e:
            i += 1
            time.sleep( 1 )
            continue
        
        re_result = re_compile.search( href_url )
        
        if not re_result:
            i += 1
            continue
        
        img_url = re_result.group(1)
        img_url = urllib.parse.unquote( img_url )
        img_urls.append( img_url )
        
        i += 1
        time.sleep( 1 )
        
    return img_urls

# selenium を使用する場合、browser(driver)を返します
def get_browser():
    selenium_conf = conf["selenium"]
    browser_service = \
        Service( executable_path=selenium_conf["browser_driver"] )

    browser_opts = Options()
    for tmp_opt in selenium_conf["browser_options"]:
        browser_opts.add_argument( tmp_opt )

    browser = webdriver.Edge(service = browser_service,
                             options = browser_opts )
    # 要素が見つかるまで、最大 ?秒 待つ
    browser.implicitly_wait( selenium_conf["implicitly_wait"] )

    # 以下は、headless modeでもdownloadする為のもの。
    # refer to https://qiita.com/memakura/items/f80d2e2c59514cfc14c9
    browser.command_executor._commands["send_command"] = (
        "POST",
        '/session/$sessionId/chromium/send_command' )
    params = {'cmd': 'Page.setDownloadBehavior',
              'params': {'behavior': 'allow',
                         'downloadPath': '/tmp' } }
    browser.execute("send_command", params=params)

    return browser



if __name__ == '__main__':
    main()
    