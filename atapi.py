import datetime

import undetected_chromedriver as webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Settings

import colorama

from mcstatus import JavaServer

driver = webdriver.Chrome(options=Settings.woptions)


def connect_account():
    driver.get("https://aternos.org/go/")

    print_out("Logging in..", colorama.Fore.YELLOW)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, "user"))).click()

    usernamelement = driver.find_element(By.ID, "user")
    usernamelement.send_keys(Settings.USERNAME)

    wait.until(EC.element_to_be_clickable((By.ID, "password"))).click()

    passelement = driver.find_element(By.ID, "password")
    passelement.send_keys(Settings.PASSWORD)

    wait.until(EC.element_to_be_clickable((By.ID, "login"))).click()

    print_out("Logged in.", colorama.Fore.CYAN)

    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.css-1litn2c'))).click()
        print_out("Accepted cookies..", colorama.Fore.CYAN)
    except:
        print_out("Skipped cookies..", colorama.Fore.CYAN)

    #serverelement = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "server-body"))).click()
    #/html/body/div[1]/main/section/div[1]/div[2]/div/div[1]

    #Using xpath so that if it has multiple servers it clicks the first one


    try:
        serverelement = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "server-body"))).click()
    except:
        serverelement = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/section/div[1]/div[2]/div/div[1]"))).click()


    print_out("Serving for " + get_ip(), colorama.Fore.GREEN)


def start_server():
    print_out("Starting the server..", colorama.Fore.YELLOW)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, "start"))).click()
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-red"))).click()

    while get_status() == "Waiting in queue":
        # while in queue, check for the confirm button and try click it
        try:
            wait = WebDriverWait(driver, 5)
            wait.until(EC.element_to_be_clickable((By.ID, 'confirm'))).click()
        except:
            pass

    print_out("Started the server!", colorama.Fore.GREEN)


def refresh_browser():
    driver.refresh()


def get_players():
    try:
        server = JavaServer.lookup(get_ip())
        status = server.status()
        names = []
        for a in status.players.sample:
            names.append(a.name)
        return names
    except:
        return []

def get_players_num():
    num = _find_on_page(classname="js-players", xpath='/html/body/div[2]/main/section/div[3]/div[4]/div[3]/div[1]/div[1]/div[2]/div[2]')

    num = num.split("/")[0]
    num = int(num)

    return num

def get_time_left():
    wait = WebDriverWait(driver, 15)
    time_left = 'Unknown'

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "server-status-label-left")))
        time_left = driver.find_element(By.CLASS_NAME, "server-status-label-left").text

    except:
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section/div[3]/div[2]/div[1]/div/span[1]")))
        time_left = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/div[3]/div[2]/div[1]/div/span[1]").text

    return time_left

def get_status():
    wait = WebDriverWait(driver, 15)
    status = ''

    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "statuslabel-label")))
        status = driver.find_element(By.CLASS_NAME, "statuslabel-label").text

    except:

        #Also try xpath and hope it works
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/section/div[3]/div[3]/div[1]/div/span[2]/span")))
        status = driver.find_element(By.XPATH, "/html/body/div[2]/main/section/div[3]/div[3]/div[1]/div/span[2]/span").text


    if status == '':
        status = "ERR.STS"
    return status

def get_ip():
    ip = _find_on_page(classname="server-ip", xpath='/html/body/div[2]/main/section/div[3]/div[1]')

    if ip == "ERR":
         ip = _find_on_page(xpath='//*[@id="ip"]')

    ip = ip.replace("Connect", "");
    ip = ip.replace("\n", "");

    return ip

def get_software():
    return _find_on_page(id="software", xpath='//*[@id="software"]')

def get_version():
    return _find_on_page(id="version", xpath='//*[@id="version"]')

def get_tps():
    tps = _find_on_page(classname="js-tps", xpath='//*[@id="read-our-tos"]/main/section/div[3]/div[4]/div[3]/div[1]/div[3]/div[2]/div[2]', errval=0)
    return int(tps)

def get_ram():
    ram = _find_on_page(classname="js-ram", xpath='//*[@id="read-our-tos"]/main/section/div[3]/div[4]/div[3]/div[1]/div[2]/div[2]/div[2]', errval=0)
    return ram

def get_server_info():
    return get_ip(), get_status(), get_players_num(), \
           get_software(), get_version(), get_tps()


def print_out(out, color):
    print("")
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + color, out, colorama.Style.RESET_ALL)

def _find_on_page(id=None, classname=None, xpath=None, errval=None):
    wait = WebDriverWait(driver, 20)
    elementtext = ""

    if classname != None:
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, classname)))
            elementtext = driver.find_element(By.CLASS_NAME, classname).text
        except:pass

    if id != None:
        try:
            wait.until(EC.presence_of_element_located((By.ID, id)))
            elementtext = driver.find_element(By.ID, id).text
        except:
            pass



    if elementtext == "" and xpath != None:
        try:
            # Also try xpath and hope it works
            wait.until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            elementtext = driver.find_element(By.XPATH, xpath).text
        except:pass

    if elementtext == "":
        if errval == None:
            elementtext = "ERR"

        elif errval != None:
            elementtext = errval

    return elementtext