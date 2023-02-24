import undetected_chromedriver as webdriver
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))
USERNAME = str(os.getenv('USERNAME'))
PASSWORD = str(os.getenv('PASSWORD'))
GUILDID = int(os.getenv('GUILDID'))

#Webdriver options
woptions = webdriver.ChromeOptions()
#woptions.add_argument('--disable-blink-features=AutomationControlled')
#woptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#                     "AppleWebKit/537.36 (KHTML, like Gecko) "
#                     "Chrome/87.0.4280.88 Safari/537.36")
#woptions.add_experimental_option("excludeSwitches", ["enable-automation"])
#woptions.add_experimental_option('useAutomationExtension', False)
woptions.add_argument("--headless")
woptions.add_argument('--disable-gpu')
woptions.add_argument('--no-sandbox')
woptions.add_argument("--disable-dev-shm-usage")
woptions.add_argument("--blink-settings=imagesEnabled=false")