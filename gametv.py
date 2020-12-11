
import re,os

from selenium import webdriver
from selenium.webdriver import ActionChains
import requests
import concurrent.futures

class gametv:

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
        #self.driver = webdriver.Chrome(executable_path=os.path.join(os.path.abspath(__file__+'/../..'),'executables','chromedriver.exe'))
        self.urls = {}

    def invoke_browser(self):
        self.driver.get("https://www.game.tv/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.availablegames = self.driver.find_element_by_class_name("available-games")

    def get_urls(self):
        action = ActionChains(self.driver)
        action.move_to_element(self.availablegames)
        action.perform()
        self.driver.implicitly_wait(5)
        game_items = self.driver.find_elements_by_class_name("games-item")
        for i in range (1, len(game_items)+1):
             game_name = self.driver.find_element_by_xpath("//*[@id='game_list']/ul/li["+str(i)+"]")
             link = game_name.find_element_by_tag_name('a')
             url = link.get_attribute('href')
             self.urls[url] = [game_name.text]

    def count(self,url):
        response = requests.get(url)
        code = response.status_code
        res = response.text
        # print(res)
        count = re.findall('count-tournaments">(.*)</span>', res)[0]
        data = self.urls[url]
        data.append(count)
        data.append(code)
        self.urls[url] = data


    def runner(self):
        self.invoke_browser()
        self.get_urls()
        print("Please Wait while the script is fetching data...")
        print("It would approximately take 1 minute to scrap all pages...")
        with concurrent.futures.ThreadPoolExecutor() as exact:
            exact.map(self.count,list(self.urls.keys()))
        print("S.No || Game Name        || URL       || Count     ||  status_code    ")
        for index,(url,game_and_count) in enumerate(self.urls.items()):
            print(f"{int(index) + 1}   || {game_and_count[0]}     || {url} || {game_and_count[1]}  || {game_and_count[2]}")


if __name__ == '__main__':
    game_tv = gametv()
    game_tv.runner()