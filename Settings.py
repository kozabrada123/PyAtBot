import undetected_chromedriver as webdriver


#General required settings

Token = ****
Username = ****
Password =  ****

#Discord settings
prefix = "at."
description = ""


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

#Headless
#woptions.add_argument("--headless")
#woptions.add_argument("--disable-gpu")