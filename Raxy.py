import asyncio
import datetime
import json
import os
import random
import string
import subprocess
import sys
import threading
import re
import time
from concurrent.futures import ThreadPoolExecutor
from winreg import *
import glob

import aiohttp
import pygetwindow as gw
import pytz
import requests
import urllib3
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

from smsactivate.api import SMSActivateAPI
from contas import Logador
from source import *
from TempMail import TempMail

import logging

version = 1.28

logging.getLogger('selenium').setLevel(logging.CRITICAL)


def configs():
    with open("source/configs.json", "r") as json_file:
        data_dict = json.load(json_file)
    return data_dict

class AutoFarm:
    def __init__(self):
        key = OpenKey(HKEY_CURRENT_USER, r'Control Panel\International\Geo', 0, KEY_ALL_ACCESS)
        SetValueEx(key, "Name", 0, REG_SZ, "BR")
        SetValueEx(key, "Nation", 0, REG_SZ, "32")

        self.email = None
        self.senha = None
        self.primeiralinha = None
        self.ismain = None
        self.quantidade = None

        self.authrewards = None

    def gerarcmd(self):
        if os.path.isfile("autobote.cmd"):
            return
        else:
            comando = input("Deseja criar um cmd para fazer atalho? (S/N)\n>> ")
            if comando.lower() == "s":
                with open("autobote.cmd", "w") as autobote:
                    autobote.write("@echo off\n")
                    autobote.write(
                        fr'"C:\Users\{os.getlogin()}\AppData\Local\Programs\Python\Python311\python.exe" AutoBot.py' + "\n")
                    autobote.write("pause")
                    exit()

    def getacc(self, delete=False):
        if not delete:
            req = requests.get(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False).json()

            accs = list(req.keys())[0]
            conta = req[accs]["Current"]

            self.email, self.senha = str(conta).split(";")
        else:
            accs = list(requests.get(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False).json().keys())[0]
            requests.delete(f"{dtb}Usuarios/Farmando/{os.getlogin()}/{accs}.json", verify=False)

            data = {"Current": str(self.email + ';' + self.senha)}

            dia = self.get_data_hora_brasilia()

            requests.post(f"{dtb}/Usuarios/Concluido/{os.getlogin()}/{dia}/.json", data=json.dumps(data), verify=False)

    def logar(self):
        print("Logando contas no windows")
        logador = Logador.AutoLogin("s")
        logador.loginAPI(dir="source/imgs", email=self.email, senha=self.senha)
        print("Contas logadas no windows\n\n")

    def fiddler(self, method="open"):
        if method == "open":
            while True:
                try:
                    print("Abrindo o Fiddler")
                    try:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\Desktop\Fiddler Classic.lnk")
                    except:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\OneDrive\Área de Trabalho\Fiddler Classic.lnk")

                    while True:
                        try:
                            window = gw.getWindowsWithTitle("Fiddler")[0]
                            window.restore()
                            window.activate()
                            break
                        except:
                            pass

                    controller = AImg("source/imgs", 0.8, "Fiddler")

                    valid = controller.WaitIf(15, "simfiddler.png", "fiddlercapturing.png")
                    if valid == "1 Valido":
                        controller.WaitUntil("simfiddler.png")

                    while True:
                        try:
                            controller.WaitUntil("fiddlercapturing.png", 15, True)
                            window = gw.getWindowsWithTitle("Fiddler")[0]
                            window.minimize()
                            print("Fiddler aberto\n\n")
                            return
                        except:
                            pass
                except:
                    try:
                        window = gw.getWindowsWithTitle('Progress Telerik Fiddler Classic')[0]
                        window.close()
                    except:
                        pass
                    continue

        elif method.lower() == "close":
            try:
                window = gw.getWindowsWithTitle('Progress Telerik Fiddler Classic')[0]
                window.close()
                print("Fiddler fechado\n\n")
            except:
                pass

    def rewardscriar(self):

        if not os.path.exists(f"C:/Farm/rewards/{os.getlogin()}criar.txt"):
            raise Exception("Arquivos Faltando")
        with open(f"C:/Farm/rewards/{os.getlogin()}criar.txt", "r") as file:
            lines = file.readlines()
            authorization = self.authrewards = [linha for linha in lines if linha.__contains__("Authorization: ")][
                0].strip().replace("Authorization: ", "")

            ms = [linha for linha in lines if linha.__contains__("MS-CV: ")][0].strip().replace("MS-CV: ", "")

        headersfarm = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': "IT",
            'X-Rewards-Language': 'it-IT',
            'MS-CV': ms,
            'Authorization': f'{authorization}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        payload = {"puid": "",
                   "risk_context": {"ui_language": "pt-BR", "device_type": "Unknown(Windows.Desktop) 10.0.19045.3086",
                                    "device_id": ""},
                   "attributes": {"country": "BR", "creative": "MY00OF", "program": "XBOXAPPJOIN", "publisher": "Xbox"}}

        response = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me', headers=headersfarm,
                                 json=payload, verify=False)
        response.raise_for_status()

    def rewards(self):
        print("Logando no rewards")

        while True:
            try:

                while True:
                    try:
                        window = gw.getWindowsWithTitle("Microsoft Rewards")[0]
                        window.activate()
                        break
                    except:
                        pass
                    try:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\Desktop\Microsoft Rewards.lnk")
                    except:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\OneDrive\Área de Trabalho\Microsoft Rewards.lnk")

                while True:
                    try:
                        controller = AImg("source/imgs", 0.8, "Microsoft Rewards")
                        break
                    except:
                        pass

                valid = controller.WaitIf(10, "experimente.png", "detalhamento.png", "localizacao.png",
                                          "boasvindas.png", "conheca.png")
                if valid == "1 Valido":
                    while not os.path.exists(f"C:/Farm/rewards/{os.getlogin()}criar.txt"):
                        continue
                    self.rewardscriar()
                    subprocess.run("taskkill /IM Microsoft.Rewards.Xbox.exe /F", stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    continue

                elif valid == "2 Valido":
                    controller.WaitUntil("detalhamento.png", 15, True)
                    while not os.path.exists(f"C:\\Farm\\rewards/{os.getlogin()}.txt"):
                        continue

                elif valid == "3 Valido" or valid == "4 Valido":
                    subprocess.run("taskkill /IM Microsoft.Rewards.Xbox.exe /F", stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    continue
                else:
                    controller.WaitUntil("conheca.png")
                    controller.WaitUntil("detalhamento.png", 15, True)
                    while not os.path.exists(f"C:\\Farm\\rewards/{os.getlogin()}.txt"):
                        continue
                subprocess.run("taskkill /IM Microsoft.Rewards.Xbox.exe /F", stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                print("Rewards logado\n\n")
                return True
            except:
                subprocess.run("taskkill /IM Microsoft.Rewards.Xbox.exe /F", stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                continue

    def xbox(self):
        print("Logando no xbox")

        while True:
            try:

                while True:
                    try:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\Desktop\Xbox.lnk")
                    except:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\OneDrive\Área de Trabalho\Xbox.lnk")
                    try:
                        window = gw.getWindowsWithTitle("Xbox")[0]
                        window.activate()
                        break
                    except:
                        pass

                controller = AImg("source/imgs", 0.8, "Xbox")

                controller.WaitUntil("xboxg.png", 10, True)
                time.sleep(2)
                try:
                    controller.WaitUntil("entrar.png", timeout=2)
                except:
                    print("A conta já esta logada no xbox\n\n")
                    while not os.path.exists(f"C:\\Farm\\xbox/{os.getlogin()}xbox.txt"):
                        continue
                else:
                    controller.WaitUntil("entrarxbox.png")
                    controller.WaitDisappear("configs.png")
                    ife = controller.WaitIf(15, "xbox.png", "entrar2.png")
                    if ife == "1 Valido" or ife == "2 Valido":
                        if ife == "2 Valido":
                            controller.WaitUntil("entrar2.png")
                        controller.WaitUntil("xbox.png", 15, True)
                        time.sleep(2)
                        controller.WaitUntil("vamosjogar.png")
                        valido = controller.WaitIf(15, "tentarnovamente.png", "gamepass.png")
                        if valido == "1 Valido":
                            controller.WaitUntil("tentarnovamente.png")
                            controller.WaitUntil("gamepass.png", 15, True)
                            try:
                                controller.WaitUntil("entrar.png", 4, False)
                                subprocess.run("taskkill /IM XboxPcApp.exe /F", stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL)
                                subprocess.run("taskkill /IM XboxApp.exe /F", stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL)
                                continue
                            except:
                                pass
                            while not os.path.exists(f"C:\\Farm\\xbox/{os.getlogin()}xbox.txt"):
                                continue
                        else:
                            try:
                                time.sleep(2)
                                controller.WaitUntil("entrar.png", 2, False)
                                subprocess.run("taskkill /IM XboxPcApp.exe /F", stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL)
                                subprocess.run("taskkill /IM XboxApp.exe /F", stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL)
                                continue
                            except:
                                pass
                            while not os.path.exists(f"C:\\Farm\\xbox/{os.getlogin()}xbox.txt"):
                                continue
                        print("Xbox logado\n\n")
                subprocess.run("taskkill /IM XboxPcApp.exe /F", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run("taskkill /IM XboxApp.exe /F", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return
            except:
                subprocess.run("taskkill /IM XboxPcApp.exe /F", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                subprocess.run("taskkill /IM XboxApp.exe /F", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)
                continue

    def processrewards(self):

        threads = []

        if not os.path.exists(f"C:/Farm/rewards/{os.getlogin()}.txt"):
            raise Exception("Arquivos Faltando")
        while True:
            try:
                with open(f"C:/Farm/rewards/{os.getlogin()}.txt", "r") as file:
                    lines = file.readlines()
                    authorization = self.authrewards = [linha for linha in lines if linha.__contains__("Authorization: ")][
                        0].strip().replace("Authorization: ", "")

                    ms = [linha for linha in lines if linha.__contains__("MS-CV: ")][0].strip().replace("MS-CV: ", "")

                    cookie = [linha for linha in lines if linha.__contains__("Cookie: ")][0].strip().replace("Cookie: ", "")
                    if not authorization:
                        continue

                for country in countries:
                    t = threading.Thread(target=farm.RewardsRun, args=(authorization, ms, cookie, country))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
                break
            except:
                pass

    def farmxbox(self):

        if not os.path.exists(f"C:/Farm/xbox/{os.getlogin()}xbox.txt"):
            raise Exception("Arquivos Faltando")

        while True:
            try:
                with open(f"C:/Farm/rewards/{os.getlogin()}.txt", "r") as file:
                    lines = file.readlines()
                    authorizationrewards = self.authrewards = \
                    [linha for linha in lines if linha.__contains__("Authorization: ")][
                        0].strip().replace("Authorization: ", "")
                    if not authorizationrewards:
                        continue

                with open(f"C:/Farm/xbox/{os.getlogin()}xbox.txt", "r") as file:
                    lines = file.readlines()
                    authorization = [linha for linha in lines if linha.lower().__contains__("authorization: ")][0][15:].strip()

                    xuide = [linha.strip() for linha in lines if linha.__contains__("users")][0].replace("HTTP/1.1", "")
                    xuide = str(''.join(i for i in xuide if i.isdigit()))
                    if not authorizationrewards:
                        continue
                break
            except:
                pass

        resultado: bool = xbox.conquista(xuide, authorization, authorizationrewards)
        return resultado

    def get_data_hora_brasilia(self):
        fuso_brasilia = pytz.timezone('America/Sao_Paulo')

        data_hora_brasilia = datetime.datetime.now(fuso_brasilia)

        dia = data_hora_brasilia.day
        mes = data_hora_brasilia.month
        ano = data_hora_brasilia.year

        data_hora_string = f"{dia:02d}-{mes:02d}-{ano}"

        return data_hora_string


class Login:
    def __init__(self):
        self.delay = 9
        self.cookiesbing = None

        self.chrome_options = ChromeOptions()
        self.chrome_options.add_argument('--log-level=3')

        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36")

    def bingantibug(self,
                    xpath, driverz, sumir=False):
        try:
            if not sumir:
                WebDriverWait(driverz, self.delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                WebDriverWait(driverz, self.delay).until(EC.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            raise Exception('A Pagina nao carregou a tempo')

    def logarsite(self, username, senha):

        print("Começando a Logar no Site")

        try:
            driver = webdriver.Firefox(service=ChromeService(GeckoDriverManager().install()), options=self.chrome_options)
        except:
            driver = webdriver.Firefox(options=self.chrome_options)
        try:
            driver.get(
                'https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%26sig%3d387A7E8F86D465B53DD36C1487C06411&wp=MBI_SSL&lc=1046&CSRFToken=68214017-1e42-4484-bc17-b8a7323b9b91&aadredir=1')
            driver.maximize_window()
            self.bingantibug('//*[@id="i0116"]', driver)
            driver.find_element('xpath', '//*[@id="i0116"]').send_keys(username)

            self.bingantibug('//*[@id="idSIButton9"]', driver)
            driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
            time.sleep(2)

            self.bingantibug('//*[@id="i0118"]', driver)
            driver.find_element('xpath', '//*[@id="i0118"]').send_keys(senha)

            self.bingantibug('//*[@id="idSIButton9"]', driver)
            driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
            titulo = driver.title
            while titulo == "Continuar":
                titulo = driver.title

            time.sleep(1.5)
            titulo = driver.current_url
            if titulo.__contains__("bing"):
                pass
            else:
                self.bingantibug('//*[@id="idSIButton9"]', driver)
                driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
            driver.get("https://bing.com/")
            self.bingantibug('//*[@id="sbi_b"]', driver)
            self.cookiesbing = driver.get_cookies()

            driver.quit()
            print("Site logado\n\n")
            return
        except:
            try:
                driver.close()
            except:
                pass


    def checkpesquisa(self, pais):
        tries = 0
        while True:
            try:
                with open(f"C:\\Farm\\rewards/{os.getlogin()}.txt", "r") as v:
                    x = v.readlines()
                    authorization = [linha for linha in x if linha.__contains__("Authorization: ")]
                    authorization = authorization[0].strip()
                    authorization = authorization.replace("Authorization: ", "")
                saldo, pesquisa = checkpesquisa(authorization, pais)
                return int(saldo), int(pesquisa)
            except Exception as e:
                if tries > 6:
                    raise Exception("Bugamos tentando ver a quantidade de pontos na conta, motivo: " + str(e))
                tries += 1
                continue

    async def pesquisa(self, country, pontos, quantidade=125):

        quantidade1, pesquisadas1 = self.checkpesquisa(country)
        if quantidade1 >= pontos:
            return

        while True:

            try:

                connector = aiohttp.TCPConnector(limit=0)

                async with aiohttp.ClientSession(connector=connector) as session:
                    for i in range(quantidade):
                        tasks = []
                        task = asyncio.create_task(self.pesquisareq(session, f"-{country[2:]}-rotate"))
                        tasks.append(task)
                        if i < 40:
                            task = asyncio.create_task(self.pesquisareq(session, f"-{country[2:]}-rotate",
                                                                      useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"))
                            tasks.append(task)
                    await asyncio.gather(*tasks)
            except:
                pass

            quantidade2, pesquisadas2 = self.checkpesquisa(country)
            sys.stdout.write(
                "\rA Quantidade de Pontos ainda é: " + str(quantidade2) + " " + f"Quantidade App: {pesquisadas2}/50")
            sys.stdout.flush()
            if int(pesquisadas1) == int(pesquisadas2):
                if int(pesquisadas2) < 50:
                    continue
            if int(quantidade2) < pontos:
                continue
            print("\nPesquisa Completa! \n\n")
            return

    async def pesquisareq(self, session, pais,
                          useragent="Mozilla/5.0 (Linux; Android 8.0.1; Samsung A33 Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36"):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": useragent,
            "sec-ch-ua-full-version-list": '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.134", "Google Chrome";v="114.0.5735.134"',
            "Upgrade-Insecure-Requests": "1"
        }

        cookies_requests = {}

        for cookie in self.cookiesbing:
            name = cookie['name']
            value = cookie['value']
            cookies_requests[name] = value

        palavra_aleatoria = ''.join(random.choices(string.ascii_lowercase, k=15))

        try:
            if not isproxy:
                async with session.get(f"https://www.bing.com/search?q={palavra_aleatoria}", headers=headers,
                                       cookies=cookies_requests,
                                       timeout=12):
                    pass
            else:
                proxy = config['proxy']

                proxydetails = [proxy['proxy_address'], proxy['proxy_port'], proxy['proxy_username'], proxy['proxy_password']]
                if pais != "-BR-rotate":
                    async with session.get(f"https://www.bing.com/search?q={palavra_aleatoria}", headers=headers,
                                           cookies=cookies_requests,
                                           proxy=f"http://{proxydetails[2]}{pais}:{proxydetails[3]}@{proxydetails[0]}:{proxydetails[1]}/",
                                           timeout=6):
                        pass
                else:
                    async with session.get(f"https://www.bing.com/search?q={palavra_aleatoria}", headers=headers,
                                           cookies=cookies_requests,
                                           timeout=6):
                        pass
        except:
            pass

    def desbugar(self):
        while requests.get(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False).json() is None:
            print("Desbugando contas")

            desbugador = Desbug()
            drivermail = desbugador.desbugar()
            return drivermail

    def resgatar(self, drivermail, inb, tmp, senha ,addnum=True):
        try:
            drivermail = drivermail[0]

            print("começando a resgatar")
            drivermail.maximize_window()
            while True:
                try:
                    while True:
                        try:
                            greenid = drivermail.find_element('name', 'greenId').get_attribute("value")
                            break
                        except:
                            pass

                    vertoken = drivermail.find_element('name', '__RequestVerificationToken').get_attribute("value")

                    reqid = drivermail.find_element('name', 'challenge.RequestId').get_attribute("value")
                    cookies = drivermail.get_cookies()
                    cookies_requests = {cookie['name']: cookie['value'] for cookie in cookies}

                    url = "https://rewards.bing.com/redeem/checkout/verify?form=dash_2"
                    payload = {
                        "productId": "000400000259",
                        "provider": "csv",
                        "challenge.RequestId": str(reqid),
                        "challenge.TrackingId": "",
                        "challenge.ChallengeMessageTemplate": "D",
                        "challenge.State": "CreateChallenge",
                        "expectedGreenId": str(greenid),
                        "challenge.SendingType": "SMS",
                        "__RequestVerificationToken": str(vertoken)
                    }

                    headers = {
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                    }

                    proxy = config['proxy']

                    proxydetails = [proxy['proxy_address'], proxy['proxy_port'], proxy['proxy_username'],
                                    proxy['proxy_password']]
                    proxy = {
                        "http": f"http://{proxydetails[2]}-US-rotate:{proxydetails[3]}@{proxydetails[0]}:{proxydetails[1]}/",
                        "https": f"http://{proxydetails[2]}-US-rotate:{proxydetails[3]}@{proxydetails[0]}:{proxydetails[1]}/"
                    }

                    break
                except:
                    pass

            try:
                drivermail.get('https://account.live.com/names/manage')
                while not drivermail.current_url.lower().__contains__("proof"):
                    if drivermail.current_url.lower().startswith('https://account.live.com/names/manage'):
                        break
                    try:
                        drivermail.find_element('xpath', '//*[@id="i0118"]').send_keys(senha)
                        drivermail.find_element('xpath', '//*[@id="idSIButton9"]').click()
                    except:
                        pass
                while True:
                    need = False
                    try:
                        if drivermail.current_url.lower().startswith('https://account.live.com/names/manage'):
                            break
                        try:
                            drivermail.find_element('xpath', '//*[@id="idDiv_SAOTCS_Proofs"]/div/div').is_enabled()
                            need = True
                            break
                        except:
                            pass
                        if need:
                            break

                        self.bingantibug('//*[@id="EmailAddress"]', drivermail)
                        drivermail.find_element('xpath', '//*[@id="EmailAddress"]').send_keys(inb.address)
                        self.bingantibug('//*[@id="iNext"]', drivermail)
                        drivermail.find_element('xpath', '//*[@id="iNext"]').click()
                        time.sleep(2)

                        while True:
                            emails = TempMail.getEmails(tmp, inbox=inb)
                            if not len(emails):
                                continue
                            mensagem = emails[0].body
                            break

                        linhas = str(mensagem).splitlines()
                        otp = [i for i in linhas if i.__contains__('Código de segurança:')]

                        ott = otp[0][21:]

                        self.bingantibug('//*[@id="iOttText"]', drivermail)
                        drivermail.find_element('xpath', '//*[@id="iOttText"]').send_keys(ott)
                        drivermail.find_element('xpath', '//*[@id="iNext"]').click()
                        break
                    except:
                        drivermail.get('https://account.live.com/names/Manage')

                while not drivermail.current_url.lower().startswith('https://account.live.com/names/manage'):
                    try:
                        if drivermail.current_url.lower().startswith('https://account.live.com/names/manage'):
                            break
                        self.bingantibug('//*[@id="idDiv_SAOTCS_Proofs"]/div/div', drivermail)
                        drivermail.find_element('xpath', '//*[@id="idDiv_SAOTCS_Proofs"]/div/div').click()
                        self.bingantibug('//*[@id="idTxtBx_SAOTCS_ProofConfirmation"]', drivermail)
                        drivermail.find_element('xpath', '//*[@id="idTxtBx_SAOTCS_ProofConfirmation"]').send_keys(inb.address)
                        drivermail.find_element('xpath', '//*[@id="idSubmit_SAOTCS_SendCode"]').click()

                        while True:
                            emails = TempMail.getEmails(tmp, inbox=inb)
                            if not len(emails):
                                continue
                            mensagem = emails[0].body
                            break

                        linhas = str(mensagem).splitlines()
                        otp = [i for i in linhas if i.__contains__('Código de segurança:')]

                        ott = otp[0][21:]

                        self.bingantibug('//*[@id="idTxtBx_SAOTCC_OTC"]', drivermail)
                        drivermail.find_element('xpath', '//*[@id="idTxtBx_SAOTCC_OTC"]').send_keys(ott)
                        drivermail.find_element('xpath', '//*[@id="idChkBx_SAOTCC_TD"]').click()
                        drivermail.find_element('xpath', '//*[@id="idSubmit_SAOTCC_Continue"]').click()
                    except:
                        drivermail.get('https://account.live.com/names/manage')
            except:
                pass

            if addnum:

                sa = SMSActivateAPI(smsauth)

                dado = str(config['numbers'][os.getlogin()])
                if not dado:
                    print(f"Coloque um numero para o seu usuario, nome do usuario = {os.getlogin()}")
                    while not dado:
                        dado = str(config['numbers'][os.getlogin()])

                for item in sa.getRentList()['values'].values():
                    if item['phone'] == dado:
                        numeroid = item['id']

                try:
                    if sa.getRentStatus(id=numeroid)["message"] == "STATUS_WAIT_CODE":
                        quantidade = 0
                except:
                    try:
                        quantidade = sa.getRentStatus(id=numeroid)["quantity"]
                    except:
                        return False

                smsplus = int(quantidade) + 1

                self.bingantibug('//*[@id="idAddPhoneAliasLink"]', drivermail)
                drivermail.find_element('xpath', '//*[@id="idAddPhoneAliasLink"]').click()
                self.bingantibug('//*[@id="DisplayPhoneCountryISO"]', drivermail)
                drivermail.find_element('xpath', '//*[@id="DisplayPhoneCountryISO"]').click()

                self.bingantibug('//*[@id="DisplayPhoneCountryISO"]/option[4]', drivermail)
                drivermail.find_element('xpath', '//*[@id="DisplayPhoneCountryISO"]/option[4]').click()

                while True:
                    try:
                        drivermail.find_element('xpath', '//*[@id="DisplayPhoneNumber"]').send_keys(str(dado[2:]))
                        break
                    except:
                        try:
                            drivermail.get('https://account.live.com/names/manage')
                            self.bingantibug('//*[@id="idAddPhoneAliasLink"]', drivermail)
                            drivermail.find_element('xpath', '//*[@id="idAddPhoneAliasLink"]').click()
                            self.bingantibug('//*[@id="DisplayPhoneCountryISO"]', drivermail)
                            drivermail.find_element('xpath', '//*[@id="DisplayPhoneCountryISO"]').click()

                            self.bingantibug('//*[@id="DisplayPhoneCountryISO"]/option[4]', drivermail)
                            drivermail.find_element('xpath', '//*[@id="DisplayPhoneCountryISO"]/option[4]').click()
                        except:
                            pass

                drivermail.find_element('xpath', '//*[@id="iBtn_action"]').click()

                while not int(quantidade) == smsplus:
                    try:
                        quantidade = sa.getRentStatus(id=numeroid)["quantity"]
                    except:
                        quantidade = "0"

                smsinteiro = sa.getRentStatus(id=numeroid)['values']["0"]['text']
                sms = re.findall(r'\d+', smsinteiro)[0]

                self.bingantibug('//*[@id="iOttText"]', drivermail)
                drivermail.find_element('xpath', '//*[@id="iOttText"]').send_keys(sms)
                drivermail.find_element('xpath', '//*[@id="iBtn_action"]').click()

                while not drivermail.current_url.__contains__("Manage"):
                    continue

                quantidade, _ = self.checkpesquisa("PTBR")
                while quantidade >= 2900:
                    try:
                        if isproxy:
                            response = requests.post(url, data=payload, headers=headers, cookies=cookies_requests,
                                                     proxies=proxy, verify=False)
                        else:
                            response = requests.post(url, data=payload, headers=headers, cookies=cookies_requests, verify=False)
                        if response.status_code == 200:
                            print("Resgatado com sucesso!")
                        else:
                            print("Ocorreu um erro ao resgatar:", response.status_code)
                    except:
                        pass
                    quantidade, _ = self.checkpesquisa("PTBR")

                drivermail.find_element('xpath', '//*[@id="idRemoveAssocPhone"]').click()
                self.bingantibug('//*[@id="iBtn_action"]', drivermail)
                drivermail.find_element('xpath', '//*[@id="iBtn_action"]').click()

                while not drivermail.current_url.__contains__("uaid"):
                    continue

                return True
        except:
            return False

    def get_location(self, pais):
        ip_address = requests.get('https://www.trackip.net/ip?json', verify=False).json()
        ip_address = ip_address["IP"]
        response = requests.get(f"https://api.findip.net/{ip_address}/?token=f3038d016cbc4511b927e2f792342c38",
                                verify=False).json()
        if response["country"]["iso_code"].upper() == pais.upper():
            return
        print("Ligue a vpn da " + pais + ".......")
        while True:
            try:
                ip_address = requests.get('https://www.trackip.net/ip?json', verify=False).json()
                ip_address = ip_address["IP"]
                response = requests.get(f"https://api.findip.net/{ip_address}/?token=f3038d016cbc4511b927e2f792342c38",
                                        verify=False).json()
                if response["country"]["iso_code"].upper() == pais.upper():
                    return
            except:
                pass


urllib3.disable_warnings()
config = configs()

quantidade = config['configurations']['quantidade']
dtb = config['configurations']['database']
countries = config['countries']

isproxy = config['proxy']['proxy_enabled']
smsauth = config['configurations']['smsauth']

def Run():

    if int(quantidade) < 1: raise Exception("Digite uma quantidade de contas a ser feitas valida!")

    for _ in range(int(quantidade)):

        autofarm = AutoFarm()
        login = Login()

        # autofarm.gerarcmd()
        print("------------------ Começando ------------------")

        if not isproxy:
            login.get_location("BR")

        drivermail = login.desbugar()

        autofarm.getacc()

        dirs = ["C:\\Farm\\rewards", "C:\\Farm\\xbox"]

        for diretorio in dirs:
            padrao_arquivos = os.path.join(diretorio, f"*{os.getlogin()}*")
            arquivos = glob.glob(padrao_arquivos)

            for arquivo in arquivos:
                os.remove(arquivo)

        autofarm.fiddler()
        autofarm.logar()

        restart = False
        while not os.path.exists(f"C:/Farm/rewards/{os.getlogin()}.txt"):
            result = autofarm.rewards()
            if result:
                break
            else:
                requests.delete(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False)
                print("Varias contas logadas, refazendo")
                restart = True
                break
        if restart:
            continue

        while not os.path.exists(f"C:/Farm/xbox/{os.getlogin()}xbox.txt"):
            autofarm.xbox()
        autofarm.fiddler("close")

        with ThreadPoolExecutor() as executor:
            print("Fazendo tasks do aplicativo/logando no site")
            xboxthread = executor.submit(autofarm.farmxbox)

            results = [xboxthread.result()]

            if results[0] is False:
                requests.delete(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False)
                print("Conquista Da conta bugou, refazendo")
                continue
            else:
                print("Tasks do app Feitas\n\n")
            rewardsthread = executor.submit(autofarm.processrewards)
            rewardsthread.result()

        drivermail[0].maximize_window()
        drivermail[0].get("https://rewards.bing.com/redeem/checkout?productId=000409000021")
        while True:
            try:
                drivermail[0].find_element('name', 'greenId').get_attribute("value")
                break
            except:
                pass
        drivermail[0].minimize_window()

        with open(f"C:/Farm/rewards/{os.getlogin()}.txt", "r") as file:
            lines = file.readlines()
            authorization = [linha for linha in lines if linha.__contains__("Authorization: ")][
                0].strip().replace("Authorization: ", "")

            ms = [linha for linha in lines if linha.__contains__("MS-CV: ")][0].strip().replace("MS-CV: ", "")

            cookie = [linha for linha in lines if linha.__contains__("Cookie: ")][0].strip().replace("Cookie: ", "")
            for country in countries:
                farm.getpoints(authorization, ms, cookie, country)

        print("Fazendo Pesquisas")

        pontos_por_pais = {
            "PTBR": 250,
            "ENUS": 500,
            "JAJP": 400
        }
        pontos_padrao = 250
        pontos = 30

        login.cookiesbing = drivermail[1]

        for country in countries:
            pontos += pontos_por_pais.get(country, pontos_padrao)
            if not isproxy:
                login.get_location(country[2:])

            print(f"Pontos necessarios: {pontos}, Pais:{country[2:]}")

            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(login.pesquisa(country, pontos))
            except:
                pass

        print("Pesquisa Feita!\n\n")

        tmp = TempMail()
        inb = TempMail.generateInbox(tmp)
        if not isproxy:
            login.get_location("US")

        while not login.resgatar(drivermail, inb=inb, tmp=tmp, senha=autofarm.senha):
            continue

        print("Conta feita!")
        drivermail[0].close()
        autofarm.getacc(True)

        for diretorio in dirs:
            padrao_arquivos = os.path.join(diretorio, f"*{os.getlogin()}*")
            arquivos = glob.glob(padrao_arquivos)

            for arquivo in arquivos:
                os.remove(arquivo)

        print("!!!!!!!!!!!!!!!!!!FINALIZADO!!!!!!!!!!!!!!!!!!!\n\n")