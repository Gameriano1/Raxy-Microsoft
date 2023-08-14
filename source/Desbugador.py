import random
import json
import time

import requests
import requests as r
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import logging
import threading
import os

logging.getLogger('selenium').setLevel(logging.CRITICAL)
dtb = "https://contas2-b9481-default-rtdb.firebaseio.com/"


class login:
    def __init__(self, email, senha, canal):

        while True:
            try:
                self.token = r.get(dtb + "infos/.json", verify=False).json()["token"]
                break
            except:
                pass

        self.delay = 14

        self.email = email
        self.senha = senha

        self.canal = canal

    def bingantibug(self,
                    xpath, driverz):
        try:
            WebDriverWait(driverz, self.delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            raise Exception('A Pagina nao carregou a tempo')

    def logar(self):
        try:

            chrome_options = ChromeOptions()
            chrome_options.page_load_strategy = 'none'
            chrome_options.add_argument('--log-level=3')

            driver = webdriver.Firefox(service=ChromeService(GeckoDriverManager().install()), options=chrome_options)

            driver.get(
                'https://login.microsoftonline.com/common/oauth2/v2.0/authorize?scope=service%3A%3Aaccount.microsoft.com%3A%3AMBI_SSL%20openid%20profile%20offline_access&response_type=code&client_id=81feaced-5ddd-41e7-8bef-3e20a2689bb7&redirect_uri=https%3A%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin-oauth&client-request-id=34301fcd-b6f1-42f7-ad50-0b722e89170b&x-client-SKU=MSAL.Desktop&x-client-Ver=4.45.0.0&x-client-CPU=x64&x-client-OS=Windows%20Server%202019%20Datacenter&prompt=login&client_info=1&state=H4sIAAAAAAAEAAXBt4KCMAAA0H-5lQEQKRkcKKJEigQkhI16oUXUA4Svv_d-LKZEFEuUHGK_lIcduD3BZPNqoFJZuH3-Im1OJjmdMn5ZYcF_8ZXcreP62xc-cda113adtfrcmUEHOH7EmRCyd2QkedzIyjUKSsXwxkfwGjCOvvY0HQRxYVKid8ja_aoeB4VDvi5Q-9b09RuP8Xmv1ZfnNEaFuGc0R0gu3ymCx1ufC0W9vB5uUjkDgx5VxEXq4cZCxS6HtljbDbYpACRkeMnsVJ-uLMCXl8DdIWjAZ2NP5EKUmrauwdkHumhJ3UeifO0kMwzFTjbjYTaH7LsnBo94lvVz35bIJFZO7IiGLs22exLk--AljnRsMNCsJ6xVq3LVizRq5_1sTw-xLNbT6ecfwNfrVloBAAA&msaoauth2=true&lc=1046&ru=https%3A%2F%2Faccount.microsoft.com%2Faccount%2FAccount%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252F%26destrt%3Dhome.landing')
            driver.maximize_window()

            self.bingantibug('//*[@id="i0116"]', driver)
            driver.find_element('xpath', '//*[@id="i0116"]').send_keys(self.email)

            self.bingantibug('//*[@id="idSIButton9"]', driver)
            driver.find_element('xpath', '//*[@id="idSIButton9"]').click()

            self.bingantibug('//*[@id="i0118"]', driver)
            driver.find_element('xpath', '//*[@id="i0118"]').send_keys(self.senha)

            self.bingantibug('//*[@id="idSIButton9"]', driver)
            driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
            titulo = driver.title
            while titulo == "Continuar":
                titulo = driver.title

            numero = 7

            while not titulo.__contains__("Ajude-nos"):
                titulo = driver.title
                if titulo.lower().__contains__("suspensa"):
                    bloqueada = False
                    try:
                        texto = driver.find_element('xpath', '//*[@id="StartHeader"]').text
                        if texto.__contains__("bloqueada"):
                            bloqueada = True
                    except:
                        pass
                    if bloqueada:
                        print("conta bloqueada")
                        raise Exception()

            self.bingantibug('//*[@id="frmAddProof"]', driver)
            texto = driver.find_element('xpath', '//*[@id="iShowSkip"]').text
            if not texto.__contains__(str(numero)):
                print("conta ja usada")
                raise Exception()

            while True:
                try:
                    driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
                    time.sleep(1)
                    break
                except:
                    try:
                        driver.find_element('xpath', '//*[@id="iShowSkip"]').click()
                    except:
                        pass
            self.bingantibug('//*[@id="iCancel"]', driver)
            driver.find_element('xpath', '//*[@id="iCancel"]').click()

            while not driver.current_url.startswith('https://account.microsoft.com/'):
                continue

            driver.get("https://bing.com")
            self.bingantibug('//*[@id="sbi_b"]', driver)
            cookiesbing = driver.get_cookies()

            #######################
            # Criar Conta no Xbox #
            #######################


            self.delay = 20
            driver.get("https://support.xbox.com/pt-BR/forms/request-a-refund")
            while True:
                try:
                    driver.find_element('xpath', '//*[@id="FormSignInButton"]').click()
                    break
                except:
                    pass

            numero = random.randint(1, 4)
            self.bingantibug(f'//*[@id="create-account-gamertag-suggestion-{str(numero)}"]', driver)
            driver.find_element('xpath', f'//*[@id="create-account-gamertag-suggestion-{str(numero)}"]').click()

            verification = driver.find_element('xpath',
                                               '//*[@id="create-account-gamertag-input-indicator"]').get_attribute(
                "class")

            while verification == "spinner":
                verification = driver.find_element('xpath',
                                                   '//*[@id="create-account-gamertag-input-indicator"]').get_attribute(
                    "class")
                if verification == "failure":
                    numero = random.randint(1, 4)
                    self.bingantibug(f'//*[@id="create-account-gamertag-suggestion-{str(numero)}"]', driver)
                    driver.find_element('xpath', f'//*[@id="create-account-gamertag-suggestion-{str(numero)}"]').click()
                continue

            driver.find_element('xpath', '//*[@id="inline-continue-control"]').click()

            while not driver.current_url == "https://support.xbox.com/pt-BR/forms/request-a-refund":
                continue

            driver.minimize_window()
            print("Conta Desbugada")
            return [driver, cookiesbing]
        except Exception as e:
            try:
                threading.Thread(target=driver.quit, args=()).start()
            except:
                pass
            raise Exception(e)


    def manager(self, users):

        try:

            while True:
                try:
                    requests.delete(dtb + "Contas/" + users + "/.json", verify=False)
                    break
                except:
                    continue

            driver = self.logar()

            data = {"Current": f"{self.email};{self.senha}"}
            requests.post(f"{dtb}/Usuarios/Farmando/{os.getlogin()}/.json", data=json.dumps(data), verify=False)
            msg = f"""```{os.getlogin()}``` >>> {self.email}
                        {self.senha}"""
            mensagem = Discord(self.token, self.canal, msg)
            mensagem.enviar()

            return driver
        except:
            return False


class Discord:
    def __init__(self, token, canal, conta):
        self.token = token
        self.canal = canal
        self.conta = conta

    def enviar(self):
        py = {
            'content': self.conta
        }

        header = {
            'authorization': self.token
        }

        r.post("https://discord.com/api/v9/channels/" + self.canal + "/messages",
               data=py, headers=header, verify=False)


class contas:

    def gerar(self):
        while True:
            try:
                contas = requests.get(dtb + "Contas/.json", verify=False).json()
                break
            except:
                continue

        itens = []
        for i in contas:
            itens.append(i)

        item = random.choice(itens)
        itemjson = contas[item]
        conta = [itemjson[i] for i in itemjson][0].split(":")

        return [item, conta[0], conta[1]]


class Desbug:
    def __init__(self):
        self.canal = "1131646251302142102"

    def desbugar(self):

        while True:
            acc = contas()
            users = acc.gerar()

            Login = login(users[1], users[2], self.canal)

            result = Login.manager(users[0])
            if not result:
                continue

            return result
