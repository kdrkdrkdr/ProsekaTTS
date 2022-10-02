from pprint import pprint
from pySmartDL import SmartDL
from time import sleep
from selenium.webdriver.common.by import By

name = 'hoshino_ichika'
character = '一歌'
char_code = 'chr_ts_1.'

class GetDataURL:
    def __init__(self, driver) -> None:
        self.driver = driver
        

    def character_stories(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/charaStory')
        sleep(5)
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for i in container:
            if character in i.text:
                url = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                url_lst.append(url)
        return url_lst


    def card_stories(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/cardStory')
        sleep(5)
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for i in container:
            if character in i.text:
                i.click()
                break
        
        con = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in con]:
            self.driver.get(j)
            sleep(3)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
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
        return url_lst
        

    def unit_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/unitStory/light_sound') # Leo/need 스토리
        sleep(5)
        
        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(3)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        return url_lst
        

    def event_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/eventStory')
        sleep(5)

        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(3)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        return url_lst
        

    def special_story(self):
        url_lst = []
        self.driver.get('https://sekai.best/storyreader/specialStory')
        sleep(5)

        container = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
        for j in [i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in container]:
            self.driver.get(j)
            sleep(3)
            c = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            url_lst.extend([i.find_element(By.TAG_NAME, 'a').get_attribute('href') for i in c])
        return url_lst
        
        


class GetProsekaDataset:
    def __init__(self, driver) -> None:
        name = 'tenma_saki'
        character = '咲希'
        self.metadata = open(f'metadata_{name}.txt', 'w', encoding='utf-8')
        self.driver = driver


    def get_data(self):
        talk_urls = self.get_talk_urls()
        for tu in talk_urls:
            self.driver.get(tu)
            sleep(10)
            containers = self.driver.find_elements(By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div')
            for i in containers:
                if self.is_character(i):
                    transcript = i.find_element(By.TAG_NAME, 'p').text.strip()
                    mp3Link = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    fname = mp3Link.split('/')[-1]
                    self.download_mp3(mp3Link)
                    self.metadata.writelines(f'{fname}|{transcript}\n')

        
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
                obj = SmartDL(mp3Url, 'wavs\\')
                obj.start()
                path = obj.get_dest()
                break
            except:
                print("1초 후 다시 요청")
                sleep(1)


    
    