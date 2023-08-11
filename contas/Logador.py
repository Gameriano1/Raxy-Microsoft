import os
import subprocess
import sys
import time
from winreg import *
import pyautogui
import pygetwindow as gw
import requests
import json

CONTAS = "contas.png"
EMALIS = "emalis.png"
PARAR_DE_ENTRAR = "parar_entrar.png"
CAMERA = "camera.png"
EMAILS_E_CONTAS = "emailsecontas.png"
MS_LOGO = "mslogo.png"
REMOVERBOTAO = "removerbotao.png"
SIMREMOVER = "yes.png"
ADICIONAR_CONTA = "adicionarconta.png"
SUCESS = "sucess.png"
OUTLOOK_COM = "outlookcom.png"
CONTINUARBUTAO = "continuarbotao.png"
EMAIL = "email.png"
CRIANDO = "criando.png"
PROXIMOBOTAO = "proximobotao.png"
SENHA = "senha.png"
ENTRARBOTAO = "entrarbotao.png"
PROXIMOUSARESSACONTA = "proximousaressaconta.png"
CONCLUIDOBOTAO = "concluidobotao.png"
AGUARDE = "aguarde.png"
GERENCIAR = "gerenciar.png"
INFOS = "suasinformacoes.png"

ROBUX = "robux.png"
OITENTAROBUX = "80robux.png"
OITENTAEOITO = "88robux.png"
ENDERECO = "endereco.png"
IGNORAR = "ignorar.png"
PRECISAMOS = "precisamos.png"
SELECIONARESTADO = "selecionarestado.png"
AGRIGENTO = "agrigento.png"
CEP = "cep.png"
SALVAR = "salvar.png"
COMPRAR = "comprar.png"
FECHAR = "fechar.png"
FECHARROBUX = "fecharrobux.png"
CLOSE = "close.png"
USEESSACONTA = "useessaconta.png"
AJUDENOS = "ajudenos.png"
PREMIUM = "premium.png"
PAGAR = "pagar.png"
SERVERREFUSED = "serverrefused.png"
CONTAS2 = "contas2.png"


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

def IsWin11():
    if sys.getwindowsversion().build >= 22000:
        return "11"
    else:
        return "10"


class AutoLogin:
    def __init__(self, logada):
        self.logada = logada.lower()

    def normal(self, dir="../source", **credenciais):

        email = credenciais["email"]
        senha = credenciais["senha"]

        windows = IsWin11()

        while True:

            try:

                os.system("start ms-settings:")
                while True:
                    try:
                        window = gw.getWindowsWithTitle("Configurações")[0]
                        window.activate()
                        break
                    except:
                        pass
                controller = AImg(dir, 0.9, "Configurações")

                controller.WaitUntil(CONTAS)

                if windows == "11":
                    controller.WaitUntil(INFOS)
                controller.WaitUntil(CAMERA, 15, True)
                parar = controller.Exists(PARAR_DE_ENTRAR)
                if parar:
                    print("parar entrar")
                    controller.WaitUntil(PARAR_DE_ENTRAR)
                    controller.WaitDisappear(PARAR_DE_ENTRAR)

                if windows == "11":
                    controller.WaitUntil(CONTAS2)

                controller.WaitUntil(EMAILS_E_CONTAS)
                controller.WaitUntil(EMALIS, 15, True)
                while True:
                    try:
                        controller.WaitUntil(MS_LOGO, 4)
                        time.sleep(0.5)
                        # ife = controller.WaitIf(15, REMOVERBOTAO, GERENCIAR)
                        try:
                            controller.WaitUntil(REMOVERBOTAO, timeout=3)
                        except:
                            controller.WaitUntil(ADICIONAR_CONTA)
                            controller.WaitUntil(OUTLOOK_COM)
                            controller.WaitUntil(CONTINUARBUTAO)
                            controller.WaitUntil(EMAIL)
                            pyautogui.write(email)
                            controller.WaitUntil(PROXIMOBOTAO)
                            controller.WaitUntil(SENHA)
                            pyautogui.write(senha)
                            controller.WaitUntil(ENTRARBOTAO)

                            valid = controller.WaitIf(10, AJUDENOS, USEESSACONTA)
                            if valid == "1 Valido":
                                controller.WaitUntil(IGNORAR)
                                controller.WaitDisappear(AJUDENOS)

                            valid = controller.WaitIf(15, PROXIMOUSARESSACONTA, PROXIMOBOTAO)
                            if valid == "1 Valido":
                                controller.WaitUntil(PROXIMOUSARESSACONTA)
                            elif valid == "2 Valido":
                                controller.WaitUntil(PROXIMOBOTAO)
                            try:
                                controller.WaitUntil("concluidoconfig.png", timeout=10)
                            except:
                                pass

                            if windows == "11":
                                controller.WaitUntil(CONTAS2)
                            controller.WaitUntil(INFOS)
                            controller.WaitUntil(CAMERA, 15, True)
                            parar = controller.Exists(PARAR_DE_ENTRAR)
                            if parar:
                                print("parar entrar")
                                controller.WaitUntil(PARAR_DE_ENTRAR)
                                controller.WaitDisappear(PARAR_DE_ENTRAR)
                            if windows == "11":
                                controller.WaitUntil(CONTAS2)
                            controller.WaitUntil(EMAILS_E_CONTAS)
                            controller.WaitUntil(EMALIS, 15, True)

                            def removeacc():
                                controller.WaitUntil(REMOVERBOTAO, timeout=3)
                                controller.WaitUntil(SIMREMOVER)

                            controller.MultipleElements(MS_LOGO, removeacc)
                            continue
                        controller.WaitUntil(SIMREMOVER)
                        if windows == "11":
                            controller.WaitUntil(CONTAS2)
                        controller.WaitUntil(INFOS)
                        controller.WaitUntil(CAMERA, 15, True)
                        if windows == "11":
                            controller.WaitUntil(CONTAS2)
                        controller.WaitUntil(EMAILS_E_CONTAS)
                        controller.WaitUntil(EMALIS, 15, True)
                        time.sleep(1)
                        try:
                            controller.WaitDisappear(MS_LOGO, timeout=5)
                        except:
                            pass
                        break
                    except:
                        break

                controller.WaitUntil(ADICIONAR_CONTA)
                controller.WaitUntil(OUTLOOK_COM)
                controller.WaitUntil(CONTINUARBUTAO)
                controller.WaitUntil(EMAIL)
                pyautogui.write(email)
                controller.WaitUntil(PROXIMOBOTAO)
                controller.WaitUntil(SENHA)
                pyautogui.write(senha)
                controller.WaitUntil(ENTRARBOTAO)

                valid = controller.WaitIf(10, AJUDENOS, USEESSACONTA)
                if valid == "1 Valido":
                    controller.WaitUntil(IGNORAR)
                    controller.WaitDisappear(AJUDENOS)

                valid = controller.WaitIf(15, PROXIMOUSARESSACONTA, PROXIMOBOTAO)
                if valid == "1 Valido":
                    controller.WaitUntil(PROXIMOUSARESSACONTA)
                elif valid == "2 Valido":
                    controller.WaitUntil(PROXIMOBOTAO)

                controller.WaitDisappear(AGUARDE)
                subprocess.run("taskkill /IM SystemSettings.exe /F", stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                break
            except:
                subprocess.run("taskkill /IM SystemSettings.exe /F", stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                continue

    def roblox(self, reembolso=False):

        dtb = "https://contas2-b9481-default-rtdb.firebaseio.com/"


        if not reembolso:
            dat = requests.get(f"{dtb}/Usuarios/Concluido/{os.getlogin()}/.json", verify=False).json()
        else:
            dat = requests.get(f"{dtb}/Usuarios/Reembolso/{os.getlogin()}/.json", verify=False).json()

        emails = []
        senhas = []

        datlist = list(dat.keys())
        for i in datlist:
            if not reembolso:
                datlist2 = list(dat[i].keys())
                for conta in datlist2:
                    acc = dat[i][conta]["Current"]
                    email, senha = str(acc).split(";")
                    emails.append(email)
                    senhas.append(senha)
            else:
                acc = dat[i]["Current"]
                email, senha = str(acc).split(";")
                emails.append(email)
                senhas.append(senha)


        for email, senha in zip(emails, senhas):

            while True:
                try:
                    print(email + ";" + senha)
                    os.system("start ms-settings:")
                    while True:
                        try:
                            window = gw.getWindowsWithTitle("Configurações")[0]
                            window.activate()
                            break
                        except:
                            pass
                    controller = AImg("../source/imgs", 0.9, "Configurações")

                    controller.WaitUntil(CONTAS)

                    controller.WaitUntil(CAMERA, 15, True)
                    parar = controller.Exists(PARAR_DE_ENTRAR)
                    print("parar entrar")
                    if parar:
                        controller.WaitUntil(PARAR_DE_ENTRAR)
                        controller.WaitDisappear(PARAR_DE_ENTRAR)
                        time.sleep(3)

                    controller.WaitUntil(EMAILS_E_CONTAS)
                    controller.WaitUntil(EMALIS, 15, True)
                    while True:
                        time.sleep(4)
                        existe = controller.Exists(MS_LOGO)
                        if existe:
                            controller.WaitUntil(MS_LOGO)
                            time.sleep(1)
                            controller.WaitUntil(REMOVERBOTAO)
                            controller.WaitUntil(SIMREMOVER)
                            controller.WaitUntil(INFOS)
                            controller.WaitUntil(CAMERA, 15, True)
                            controller.WaitUntil(EMAILS_E_CONTAS)
                            controller.WaitUntil(EMALIS, 15, True)
                            time.sleep(1.5)
                            controller.WaitDisappear(MS_LOGO)
                            break
                        else:
                            break
                    controller.WaitUntil(ADICIONAR_CONTA)
                    controller.WaitUntil(OUTLOOK_COM)
                    controller.WaitUntil(CONTINUARBUTAO)
                    controller.WaitUntil(EMAIL)
                    pyautogui.write(email)
                    controller.WaitUntil(PROXIMOBOTAO)
                    controller.WaitUntil(SENHA)
                    pyautogui.write(senha)
                    controller.WaitUntil(ENTRARBOTAO)
                    valid = controller.WaitIf(10, AJUDENOS, USEESSACONTA)
                    if valid == "1 Valido":
                        controller.WaitUntil(IGNORAR)
                        controller.WaitDisappear(AJUDENOS)

                    existe = controller.WaitIf(15, PROXIMOUSARESSACONTA, PROXIMOBOTAO)
                    if existe == "1 Valido":
                        controller.WaitUntil(PROXIMOUSARESSACONTA)
                    elif existe == "2 Valido":
                        controller.WaitUntil(PROXIMOBOTAO)

                    controller.WaitDisappear(AGUARDE)
                    subprocess.run("taskkill /IM SystemSettings.exe /F", stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)

                    try:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\Desktop\Roblox.lnk")
                    except:
                        os.startfile(fr"C:\Users\{str(os.getlogin())}\OneDrive\Área de Trabalho\Roblox.lnk")
                    time.sleep(4)
                    controller = AImg("../source/imgs", 0.9, "Roblox")
                    controller.WaitUntil(ROBUX)
                    oito = controller.WaitIf(15, OITENTAROBUX, OITENTAEOITO)
                    if oito == "1 Valido":
                        controller.WaitUntil(OITENTAROBUX)
                    else:
                        controller.WaitUntil(OITENTAEOITO)
                    controller.WaitUntil(SENHA)

                    pyautogui.write(senha)
                    controller.WaitUntil(ENTRARBOTAO)
                    valid = controller.WaitIf(15, ENDERECO, COMPRAR, PAGAR)
                    if valid == "1 Valido":
                        controller.WaitUntil(ENDERECO)
                        controller.WaitUntil(PRECISAMOS, 15, True)
                        for _ in range(2):
                            pyautogui.write("dover")
                            pyautogui.press("enter")
                            time.sleep(0.3)
                        pyautogui.press("enter")
                        pyautogui.write("d")
                        time.sleep(0.3)
                        pyautogui.press("enter")
                        pyautogui.press("tab")
                        pyautogui.write("19904")
                        pyautogui.press("enter")
                        time.sleep(3)
                        pyautogui.press("enter")
                    if valid == "1 Valido" or valid == "2 Valido":
                        while True:
                            valid = controller.WaitIf(15, COMPRAR, PAGAR)
                            if valid == "1 Valido":
                                controller.WaitUntil(COMPRAR)
                                fecha = controller.WaitIf(23, SERVERREFUSED, SUCESS)
                                if fecha == "1 Valido":
                                    valid = controller.WaitIf(15, FECHAR, CLOSE)
                                    if valid == "1 Valido":
                                        controller.WaitUntil(FECHAR)
                                    else:
                                        controller.WaitUntil(CLOSE)
                                    controller.WaitUntil(OITENTAROBUX)
                                    controller.WaitUntil(SENHA)

                                    controller.WaitUntil("fecch.png")
                                    valid = controller.WaitIf(15, FECHAR, CLOSE)
                                    if valid == "1 Valido":
                                        controller.WaitUntil(FECHAR)
                                    else:
                                        controller.WaitUntil(CLOSE)
                                    if oito == "1 Valido":
                                        controller.WaitUntil(OITENTAROBUX)
                                    else:
                                        controller.WaitUntil(OITENTAEOITO)
                                    controller.WaitUntil(SENHA)
                                    pyautogui.write(senha)
                                    controller.WaitUntil(ENTRARBOTAO)
                                    controller.WaitUntil(PREMIUM, 15, True)
                                else:
                                    valid = controller.WaitIf(15, FECHAR, CLOSE)
                                    if valid == "1 Valido":
                                        controller.WaitUntil(FECHAR)
                                    else:
                                        controller.WaitUntil(CLOSE)
                                controller.WaitUntil(OITENTAROBUX)
                                controller.WaitUntil(SENHA)
                                controller.WaitUntil(SENHA)
                                pyautogui.write(senha)
                                controller.WaitUntil(ENTRARBOTAO)
                                controller.WaitUntil(PREMIUM, 15, True)
                            else:
                                break

                    window = gw.getWindowsWithTitle('Roblox')[0]
                    window.close()

                    if not reembolso:

                        for data_key, inner_dict in dat.items():
                            for inner_key, inner_value in inner_dict.items():
                                current_value = inner_value.get('Current')
                                if current_value == str(email + ';' + senha):
                                    requests.delete(
                                        f"{dtb}Usuarios/Concluido/{os.getlogin()}/{data_key}/{inner_key}/.json",
                                        verify=False)

                        data = {"Current": str(email + ';' + senha)}

                        requests.post(f"{dtb}/Usuarios/Reembolsar/{os.getlogin()}/.json", data=json.dumps(data),
                                      verify=False)
                    else:
                        dat = requests.get(f"{dtb}/Usuarios/Reembolso/{os.getlogin()}/.json",verify=False).json()

                        for data_key, inner_dict in dat.items():
                            for inner_key, inner_value in inner_dict.items():
                                if inner_value == str(email + ';' + senha):
                                    requests.delete(f"{dtb}Usuarios/Reembolso/{os.getlogin()}/{data_key}/.json", verify=False)
                    break
                except:
                    try:
                        window = gw.getWindowsWithTitle('Roblox')[0]
                        window.close()
                    except:
                        pass
                    subprocess.run("taskkill /IM SystemSettings.exe /F", stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    continue

    def loginAPI(self, dir="../source/imgs", **credenciais):
        if self.logada == "n":
            return self.roblox()
        elif self.logada == "r":
            return self.roblox(reembolso=True)
        elif self.logada == "s":
            if not credenciais:
                return self.normal(dir)
            else:
                return self.normal(dir, email=credenciais["email"], senha=credenciais["senha"])
        else:
            raise Exception("digite um valor valido!")


if __name__ == '__main__':
    sys.path.append("..")
    from source import AImg

    controller = AImg("../source/imgs", 0.9, "Roblox")

    gerarcmd()

    logada = input("usar para roblox? R para reembolso N para normal\n")

    logar = AutoLogin(logada)
    if logada.lower() != "s":
        key = OpenKey(HKEY_CURRENT_USER, r'Control Panel\International\Geo', 0, KEY_ALL_ACCESS)
        SetValueEx(key, "Name", 0, REG_SZ, "US")
        SetValueEx(key, "Nation", 0, REG_SZ, "244")
        logar.loginAPI()
    else:
        logar.loginAPI()
else:
    from source import AImg
