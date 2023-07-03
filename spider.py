from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote
import time
import csv
import re

class spider:
    pass    
    
def search(keywords, self):
    self.driver.get('https://www.amazon.com/')
    change_address('20001', self)
    inputtag = self.driver.find_element(By.ID,'twotabsearchtextbox')
    inputtag.send_keys(keywords)
    inputtag.send_keys(Keys.ENTER)

def change_address(postal, self):
    while True:
        try:
            self.driver.find_element(By.ID,'glow-ingress-line1').click()
            # driver.find_element(By.ID,'nav-global-location-slot').click()
            time.sleep(2)
        except Exception as e:
            self.driver.refresh()
            time.sleep(10)
            continue
        try:
            self.driver.find_element(By.ID,"GLUXChangePostalCodeLink").click()
            time.sleep(2)
        except:
            pass
        try:
            self.driver.find_element(By.ID,'GLUXZipUpdateInput').send_keys(postal)
            time.sleep(1)
            break
        except Exception as NoSuchElementException:
            try:
                self.driver.find_element(By.ID,'GLUXZipUpdateInput_0').send_keys(postal.split('-')[0])
                time.sleep(1)
                self.driver.find_element(By.ID,'GLUXZipUpdateInput_1').send_keys(postal.split('-')[1])
                time.sleep(1)
                break
            except Exception as NoSuchElementException:
                self.driver.refresh()
                time.sleep(10)
                continue
    self.driver.find_element(By.ID,'GLUXZipUpdate').click()
    time.sleep(1)
    self.driver.refresh()
    time.sleep(3)

def review(self):
    for i in range(self.pageNum):
    
        #先定位到页面中每个商品的div 然后从中获取该商品各个维度的信息
        parent_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")))
        # parent_elements = driver.find_elements(By.CSS_SELECTOR, ".a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")

        for parent_element in parent_elements:
            try:
                title = parent_element.find_element(By.CSS_SELECTOR, ".a-size-base-plus.a-color-base.a-text-normal").text
            except NoSuchElementException:
                title = "NO DATA"
            try:
                rating = parent_element.find_element(By.CLASS_NAME, "a-icon-alt").get_attribute("innerHTML")
            except NoSuchElementException:
                rating = "NO DATA"
            try:
                price = parent_element.find_element(By.CSS_SELECTOR, ".a-offscreen").get_attribute("innerHTML")
            except NoSuchElementException:
                price = "NO DATA"
            try:
                rating_number = parent_element.find_element(By.CSS_SELECTOR, ".a-size-base.s-underline-text").text
            except NoSuchElementException:
                rating_number = "NO DATA"
            # 处理url
            try:
                url_element = parent_element.find_element(By.CSS_SELECTOR, ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                url = url_element.get_attribute("href")
                url = unquote(url)
                pattern = r"\/[A-Za-z0-9-]+\/dp\/[A-Za-z0-9]+\/"
                product_path = re.search(pattern, url)
                base_url = "https://www.amazon.com"
                url = base_url + product_path.group(0)
            except NoSuchElementException:
                url = "NO DATA"
            except AttributeError:
                print(url)
            List = []
            List = [title, price, rating, rating_number, url]
            self.all_list.append(List)
            print(List)
        
        # forward = self.driver.find_element(By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
        forward = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")))[0]
        if forward.is_enabled():
            forward.click()
        
    headers = ["标题", "价格", "评分", "评价数", "链接"]
    with open('amazon.csv', 'a', newline='', encoding='utf-8') as file:
        f_csv = csv.writer(file)
        f_csv.writerow(headers)
        f_csv.writerows(self.all_list)
        
if __name__ == '__main__':
    obj = spider()
    obj.pageNum = 7
    # chrome 驱动程序路径
    path = r"path\to\your\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.binary_location = r"path\to\your\chrome.exe"
    obj.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    obj.wait = WebDriverWait(obj.driver, 20)
    obj.all_list = []

    search('Bear glasses', obj)
    review(obj)
    obj.driver.quit()
