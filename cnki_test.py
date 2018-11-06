# -*- coding: utf-8 -*-
#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import FirefoxOptions
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", type = str, default = '互联网', help = 'please input search content')
parser.add_argument("-p", "--pages", type = int, default = '10', help = 'please input number of page')
args = parser.parse_args()

firefox_options = FirefoxOptions()
#firefox_options.set_headless()
browser=webdriver.Firefox(options = firefox_options)
browser.get("http://www.cnki.net")

for name in [args.search]:
    input1=browser.find_element_by_id("txt_SearchText")
    input1.clear()
    input1.send_keys(name)
    input1.send_keys(Keys.ENTER)
    time.sleep(5)
    browser.switch_to_frame("iframeResult")
    num = 1
    for page in range(args.pages):
        titles = browser.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td/table/tbody/tr')[1:21]
        now_handle = browser.current_window_handle
        for title in titles:
            item = {}
            item["index"] = num
            item["paper_name"] = " 题目:" + title.find_element_by_xpath('./td[2]').text
#            item["author"] = " 作者:" + title.find_element_by_xpath('./td[3]').text
#            item["source"] = " 期刊:" + title.find_element_by_xpath('./td[4]/a').text
            item["time"] = " 发表时间:" + title.find_element_by_xpath('./td[5]').text[:4]
            try:
                target = title.find_element_by_xpath("./td[2]/a")
                browser.execute_script("arguments[0].scrollIntoView();", target)
                title.find_element_by_xpath('./td[2]/a').click()
                time.sleep(2)
                browser.switch_to_window(browser.window_handles[-1])
                ##judge if exists foud
                if browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[4]/div[1]/p[3]').text != "" and browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[4]/div[1]/p[3]').text[:3] != "DOI":
                    item["keyword"] = browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[4]/div[1]/p[3]').text
                else:
                    item["keyword"] = browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[4]/div[1]/p[2]').text
                browser.close()
                num += 1
            except:
                try:
                    item["keyword"] = browser.find_element_by_xpath('/html/body/div[5]/div[3]/div[3]/div[1]/p[2]').text
                    num += 1
                except:
                    print("some errors occur")
                    browser.close()
                    browser.switch_to_window(now_handle)
                    continue
                else:
                    print("no error")
                    browser.close()
                    browser.switch_to_window(now_handle)
            else:
                browser.switch_to_window(now_handle)
                print("no error")
            print(item)
            with open('title_author_keywords.csv','a') as f:
                f_write = csv.writer(f)
                f_write.writerow((item["index"],item["paper_name"],item["time"],item["keyword"]))
            browser.switch_to_window(now_handle)
        time.sleep(2)
        print(page)
        if page == 0:
            browser.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[9]').click()
        else:
            browser.find_element_by_xpath('/html/body/form/table/tbody/tr[3]/td/table/tbody/tr/td/div/a[11]').click()
        time.sleep(2)
        browser.switch_to_window(browser.window_handles[-1])
