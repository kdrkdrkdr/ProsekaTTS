import codecs
from pprint import pprint
from socket import socket
from time import sleep
import chromedriver_autoinstaller

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from subprocess import CREATE_NO_WINDOW
from pathlib import Path
from pySmartDL import SmartDL
from utils import GetDataURL, GetProsekaDataset

options = Options()
path = chromedriver_autoinstaller.install()
driver = Chrome()

g = GetDataURL(driver)
sp = g.character_stories()
pprint(sp)

p = GetProsekaDataset(driver)
p.get_data(sp)