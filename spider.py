from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from urllib.parse import unquote
import pymysql
import time
import re


class spider:
    pageNum = 0
    def __init__(self):
        self.data_list = []
        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            self.wait = WebDriverWait(self.driver, 50)
        except WebDriverException:
            errorMsg = """
            Cannot found chrome.exe or ChromeDriver in ~\\AppData\\Local\\Google\\Chrome\\Application\\ 
            Please download chrome and the ChromeDriver in https://chromedriver.storage.googleapis.com/index.html?path=108.0.5359.71/
            """
            raise WebDriverException(f'[Runtime error]{time.asctime()} : {errorMsg}') from None
        # except TypeError as e:
        #     raise TypeError(f"[Runtime error]{time.asctime()}: Found a TypeEorror: {e}")
        
    def __del__(self):
        try:
            self.driver.quit()
            del self.data_list
            del self.driver
            del self.wait
        except Exception as e:
            raise Exception(f'{e}') from None
    
    def set_wait_Time(self, wait_time : int) -> None:
        """设置界面最长等待时间
        
        Args:
            wait_time (int): 等待时间
        """
        self.wait = WebDriverWait(self.driver, wait_time)
    
    def search(self, keywords : str, zone_code : str) -> None:
        """
        Args:
            keywords (string): 商品关键词
        """
        self.driver.get('https://www.amazon.com/')
        self.change_address(zone_code)
        inputtag = self.driver.find_element(By.ID,'twotabsearchtextbox')
        inputtag.send_keys(keywords)
        inputtag.send_keys(Keys.ENTER)

    def change_address(self, postal : str) -> None:
        """
        Args:
            postal (string): 地址代号
        """
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

    def get_data(self) -> list:
        """获取商品信息

        Returns:
            data_list: 商品信息列表
        """
        for i in range(self.pageNum):
            time.sleep(20)
            #先定位到页面中每个商品的div 然后从中获取该商品各个维度的信息
            # parent_elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")))
            parent_elements = self.driver.find_elements(By.CSS_SELECTOR, ".a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")
            
            List = []
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
                    rating_number = parent_element.find_element(By.XPATH, '//span[@class="a-size-base s-underline-text"]').text
                except NoSuchElementException:
                    rating_number = 0
                # 处理url
                try:
                    link_element = parent_element.find_element(By.CSS_SELECTOR, ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                    link = link_element.get_attribute("href")
                    link = unquote(link)    # 替换url中的转义字符
                    pattern = r"\/[A-Za-z0-9-]+\/dp\/[A-Za-z0-9]+\/"
                    product_path = re.search(pattern, link)
                    base_url = "https://www.amazon.com"
                    link = base_url + product_path.group(0)
                except NoSuchElementException:
                    link = "NO DATA"
                except AttributeError:
                    print(link)
                    link = "NO DATA"
                List = [title, price, link, rating, rating_number]
                self.data_list.append(List)
                List = []

                
            forward = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")))[0]
            if forward.is_enabled():
                forward.click()
        print(f"data_list: {self.data_list}")
        
        return self.data_list
        
    def commit_data(self, data_lists : list) -> None:
        #To be re refactored
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='123456',
                                    database='test',
                                    port=3306)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        # 检查是否有结果返回
        result = cursor.fetchone()
        if result:
            print("连接成功")
        else:
            print("连接失败")
        sql = "INSERT INTO amazon_data VALUES (%s, %s, %s, %s, %s)"
        default_values = ["NO DATA", "NO DATA", "NO DATA", "NO DATA", "0"]
        for data_list in data_lists:
            # 对列表中可能的缺失补充默认值
            new_list = [default_values[i] if i is None else i for i in data_list]
            print(new_list)
            cursor.execute(sql, new_list)

        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':
    key:str = "bear glasses"
    zone_code:str = "20001"
    
    crawler = spider()
    crawler.pageNum = 1
    crawler.search(key, zone_code)
    crawler.get_data()
    # crawler.commit_data(crawler.data_list)
