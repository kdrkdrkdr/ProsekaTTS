import os
from pprint import pprint
from pySmartDL import SmartDL
from time import sleep
from selenium.common import exceptions
from pprint import pprint
import chromedriver_autoinstaller

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from pySmartDL import SmartDL





class GetDataURL:
    def __init__(self, driver) -> None:
        self.driver = driver

    
    def get_all_data(self):
        lst = []
        # lst.extend(self.character_stories())
        # lst.extend(self.card_stories())
        # lst.extend(self.area_talk())
        # lst.extend(self.unit_story())
        # lst.extend(self.special_story())
        # lst.extend(self.event_story())
        return lst
        

    def character_stories(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/charaStory')
        sleep(5)
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for i in container:
            if character in i.text:
                url = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                url_lst.append(url)
        pprint(url_lst)
        return url_lst


    def card_stories(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/cardStory')
        sleep(10)
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for i in container:
            if character in i.text:
                i.click()
                break
        
        con = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in con]:
            self.driver.get(j)
            sleep(5)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        pprint(url_lst)
        return url_lst


    def area_talk(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/areaTalk/5') # MapTalk에서 에어리어 '교실 세카이'
        sleep(5)
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for i in container:
            for j in i.find_elements(By.TAG_NAME, 'img'):
                if char_code in j.get_attribute('src'):
                    url_lst.append(i.find_elements(By.TAG_NAME, 'a')[-1].get_attribute('href'))
                    break
        pprint(url_lst)
        return url_lst
        

    def unit_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/unitStory/light_sound') # Leo/need 스토리
        sleep(5)
        
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(5)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        pprint(url_lst)
        return url_lst
        

    def special_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/specialStory')
        sleep(5)

        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(5)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        pprint(url_lst)
        return url_lst


    def event_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/eventStory')
        sleep(10)

        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(10)
            try:
                c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
                url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
            except exceptions.StaleElementReferenceException:
                print("StaleElementReferenceException")

        pprint(url_lst)
        return url_lst




class GetProsekaDataset:
    def __init__(self, driver) -> None:
        if not os.path.isdir(f'./tts_dataset/{name}/'): os.mkdir(f'./tts_dataset/{name}/')
        if not os.path.isdir(f'./tts_dataset/{name}/mp3s/'): os.mkdir(f'./tts_dataset/{name}/mp3s/')
        if not os.path.isdir(f'./tts_dataset/{name}/wavs/'): os.mkdir(f'./tts_dataset/{name}/wavs/')

        self.metadata = open(f'./tts_dataset/{name}/metadata.txt', 'a', encoding='utf-8')
        self.driver = driver


    def get_data(self, talk_urls):
        for tu in talk_urls:
            self.driver.get(tu)
            sleep(10)
            containers = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            for i in containers:
                if self.is_character(i):
                    try:
                        transcript = i.find_element(By.TAG_NAME, 'p').text.strip()
                        mp3Link = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        fname = mp3Link.split('/')[-1]
                        print(f'{transcript}\n{mp3Link}')
                        self.download_mp3(mp3Link)
                        print('\n')
                        self.metadata.writelines(f'../tts_dataset/{name}/wavs/{fname}|{transcript}\n')
                    except exceptions.NoSuchElementException:
                        print("요소가 없습니다!")

                    

        
    def is_character(self, element):
        try:
            if element.text.strip().startswith(character):
                return True
            else:
                return False
        except:
            return False


    def download_mp3(self, mp3Url):
        while True:
            try:
                obj = SmartDL(mp3Url, f'./tts_dataset/{name}/mp3s/')
                obj.start()
                path = obj.get_dest()
                break
            except:
                print("1초 후 다시 요청")
                sleep(1)




if __name__ == '__main__':
    name = 'hoshino_ichika' # tenma_saki
    character = '一歌' # 咲希
    char_code = 'chr_ts_1.' # chr_ts_2.

    options = Options()
    path = chromedriver_autoinstaller.install()
    driver = Chrome()


    g = GetDataURL(driver)
    data = g.event_story()

    p = GetProsekaDataset(driver)
    p.get_data(data)