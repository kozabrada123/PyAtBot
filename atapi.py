import datetime

import undetected_chromedriver as webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Settings

import colorama

from mcstatus import MinecraftServer

driver = webdriver.Chrome(options=Settings.woptions)


def connect_account():
    driver.get("https://aternos.org/go/")

    print_out("Logging in..", colorama.Fore.YELLOW)

    wait = WebDriverWait(driver, 20)
    wait.until(EC.element_to_be_clickable((By.ID, "user"))).click()

    usernamelement = driver.find_element(By.ID, "user")
    usernamelement.send_keys(Settings.Username)

    wait.until(EC.element_to_be_clickable((By.ID, "password"))).click()

    passelement = driver.find_element(By.ID, "password")
    passelement.send_keys(Settings.Password)

    wait.until(EC.element_to_be_clickable((By.ID, "login"))).click()

    print_out("Logged in.", colorama.Fore.CYAN)

    driver.implicitly_wait(2)

    try:
        wait.until(EC.element_to_be_clickable((By.ID, "accept-choices"))).click()
        print_out("Accepted cookies..", colorama.Fore.CYAN)
    except:
        print_out("Skipped cookies..", colorama.Fore.CYAN)

    driver.implicitly_wait(2)

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
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-red"))).click()

    while get_status() == "Waiting in queue":
        # while in queue, check for the confirm button and try click it
        try:
            wait = WebDriverWait(driver, 5)
            element = wait.until(EC.element_to_be_clickable((By.ID, 'confirm'))).click()
        except:
            pass

    print_out("Started the server!", colorama.Fore.GREEN)


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


def refreshBrowser():
    driver.refresh()


def get_players():
    try:
        server = MinecraftServer.lookup(get_ip())
        status = server.status()
        names = []
        for a in status.players.sample:
            names.append(a.name)
        return names
    except:
        return []


def get_number_of_players():
    return len(get_players())


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

def get_ip():
    ip = _find_on_page(classname="ip", xpath='//*[@id="ip"]')

    #If first method failed
    if ip == "ERR":
         #Try the other Address div
         ip = _find_on_page(classname="server-ip", xpath="/html/body/div[2]/main/section/div[3]/div[1]")

    #If any method worked, it returns the ip
    #If none works it ERR anyway
    return ip


def get_software():
    return _find_on_page(id="software", xpath='//*[@id="software"]')


def get_version():
    return _find_on_page(id="version", xpath='//*[@id="version"]')


def get_tps():
    tps = _find_on_page(classname="js-tps", errval=0)
    return tps



def get_server_info():
    return get_ip(), get_status(), get_number_of_players(), \
           get_software(), get_version(), get_tps()


def print_out(out, color):
    print("")
    print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "]" + color, out, colorama.Style.RESET_ALL)