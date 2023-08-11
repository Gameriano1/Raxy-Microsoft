import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import requests
import threading
import json

dtb = "https://contas2-b9481-default-rtdb.firebaseio.com/"


def gerarcmd():
    if os.path.isfile("AccountManager.cmd"):
        return
    else:
        comando = input("Deseja criar um cmd para fazer atalho? (S/N)\n>> ")
        if comando.lower() == "s":
            with open("AccountManager.cmd", "w") as autobote:
                autobote.write(fr"""@echo off
echo Escolha o arquivo Python que deseja executar:
echo [1] Logador.py
echo [2] Reembolsador.py
echo [3] ContasNuvem.py

CHOICE /C 123 /N /M "Digite o número correspondente ao arquivo Python que deseja executar: "

if errorlevel 3 (
    "C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python311\python.exe" ContasNuvem.py
) else if errorlevel 2 (
    "C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python311\python.exe" Reembolsador.py
) else if errorlevel 1 (
    "C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python311\python.exe" Logador.py
)""")
                autobote.write("\npause")
                exit()


def create_threads(resgate):

    dat = requests.get(f"{dtb}/Usuarios/Reembolsar/{os.getlogin()}/.json", verify=False).json()

    emails = []
    senhas = []

    datlist = list(dat.keys())
    for conta in datlist:
        acc = dat[conta]["Current"]
        email, senha = str(acc).split(";")
        emails.append(email)
        senhas.append(senha)

    pares_email_senha = list(zip(emails, senhas))

    threads = []
    for i in range(0, len(pares_email_senha), 5):
        batch = pares_email_senha[i:i + 5]

        for email, senha in batch:
            thread = threading.Thread(target=resgate.open_google, args=(email, senha))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()


class Resgatar:
    def __init__(self):
        self.delay = 25

    def bingantibug(self, xpath, driverz):
        try:
            WebDriverWait(driverz, self.delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            raise Exception('A Pagina nao carregou a tempo')

    def open_google(self, username, password):

        print("Começando a Reembolsar, conta: " + username)

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(
            "https://login.live.com/oauth20_authorize.srf?redirect_uri=https://sisu.xboxlive.com/connect/oauth/XboxLive&response_type=code&state=LAAAAAEB2bjvHIVgmBsrG6e2oqVgvTfTdB8F9ZEEehVouBG0stnR_HHNwo5xMGVmMDkyZThlNTA1NDg3Njg2OTNkZWM1MmM2ODM4OGMzIDhaYS83QXdTNlVhZGFKK2hFUHpmNGcuMA&client_id=000000004420578E&scope=XboxLive.Signin&lw=1&fl=dob,easi2&xsup=1&uaid=522b8b7ac7504a2f8796ef81425717a4&nopa=2")

        self.bingantibug("//input[@id='i0116']", driver)
        driver.find_element("xpath", "//input[@id='i0116']").send_keys(username)

        time.sleep(2)
        self.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element("xpath", '//*[@id="idSIButton9"]').click()

        self.bingantibug('//*[@id="i0118"]', driver)
        driver.find_element('xpath', '//*[@id="i0118"]').send_keys(password)

        self.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element("xpath", '//*[@id="idSIButton9"]').click()
        try:
            driver.find_element("xpath", '//*[@id="idSIButton9"]').click()
        except:
            pass

        driver.get("https://support.xbox.com/pt-BR/help/subscriptions-billing/buy-games-apps/refund-orders")

        self.bingantibug('//*[@id="RefundAuthCard_SignInButton"]', driver)
        driver.find_element('xpath', '//*[@id="RefundAuthCard_SignInButton"]').click()

        while True:
            try:
                driver.find_element('xpath', '//*[@id="RequestRefundButtonBottom"]').get_attribute('type')
                break
            except:
                pass

        self.bingantibug('//*[@id="BodyContent"]/div/section/div[2]/div[1]/div/div[6]/section/div/div/div/div[2]/div[2]/div[1]/div[2]/span[2]/span', driver)
        productid = driver.find_element('xpath', '//*[@id="BodyContent"]/div/section/div[2]/div[1]/div/div[6]/section/div/div/div/div[2]/div[2]/div[1]/div[2]/span[2]/span').text

        driver.get("https://support.xbox.com/pt-BR/forms/request-a-refund")

        self.bingantibug('//*[@id="TextField0"]', driver)
        driver.find_element('xpath', '//*[@id="TextField0"]').send_keys('premium 88 roblox')

        self.bingantibug('//*[@id="TextField5"]', driver)
        driver.find_element('xpath', '//*[@id="TextField5"]').send_keys(str(productid))

        self.bingantibug("//*[contains(text(), 'Selecione uma opção')]", driver)
        opts = driver.find_element('xpath', "//*[contains(text(), 'Selecione uma opção')]").get_attribute('id')
        driver.find_element('xpath', "//*[contains(text(), 'Selecione uma opção')]").click()

        itens = ["0", "2", "3"]

        num = random.choice(itens)

        self.bingantibug(f'//*[@id="{opts}{num}"]', driver)
        driver.find_element(f'xpath', f'//*[@id="{opts}{num}"]').click()

        motivo = random.randint(0, 2) if num == "3" else random.randint(0, 3)

        self.bingantibug("//*[contains(text(), 'Selecione uma opção')]", driver)
        opts = driver.find_element('xpath', "//*[contains(text(), 'Selecione uma opção')]").get_attribute("id")
        driver.find_element('xpath', "//*[contains(text(), 'Selecione uma opção')]").click()

        self.bingantibug(f'//*[@id="{opts}{motivo}"]', driver)
        driver.find_element('xpath', f'//*[@id="{opts}{motivo}"]').click()

        self.bingantibug('//*[@id="BodyContent"]/div/div[2]/div/div/div/div[3]/button', driver)
        driver.find_element('xpath', '//*[@id="BodyContent"]/div/div[2]/div/div/div/div[3]/button').click()

        self.bingantibug('//*[@id="BodyContent"]/div/div[2]/div/div/h1', driver)

        dat = requests.get(f"{dtb}/Usuarios/Reembolsar/{os.getlogin()}/.json", verify=False).json()

        for data_key, inner_dict in dat.items():
            for inner_key, inner_value in inner_dict.items():
                if inner_value == str(username + ';' + password):
                    requests.delete(f"{dtb}Usuarios/Reembolsar/{os.getlogin()}/{data_key}/.json", verify=False)

        data = {"Current": str(username + ';' + password)}

        requests.post(f"{dtb}/Usuarios/Reembolso/{os.getlogin()}/.json", data=json.dumps(data), verify=False)

        print("Conta " + username + " Reembolsada com Sucesso")
        driver.close()


if __name__ == '__main__':

    gerarcmd()

    resgate = Resgatar()
    create_threads(resgate)
