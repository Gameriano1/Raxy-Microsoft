import requests
import urllib3
import time
from sys import stdout
import threading
import os


class Xbox:
    def ativar(self, xuid: str, auth, ide):

        urllib3.disable_warnings()

        payload = {
            "titles": [{"expiration": 600, "id": ide, "state": "active", "sandbox": "RETAIL"}]
        }

        headers = {
            'Accept-Encoding': 'gzip, deflate',
            'x-xbl-contract-version': '3',
            'Authorization': auth,
            'Cache-Control': 'no-cache'
        }
        while True:
            try:
                response = requests.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                                        json=payload,
                                        headers=headers, verify=False)
                break
            except:
                continue
        if response.status_code != 200:
            p = 16
            while response.status_code != 200:
                stdout.write(
                    "\r" + "Um Erro foi Encontrado, Esperando " + str(p) + " segundos e tentando executar novamente")
                stdout.flush()
                time.sleep(p)
                while True:
                    try:
                        response = requests.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                                                 json=payload,
                                                 headers=headers, verify=False)
                        break
                    except:
                        continue

    def conquistar(self, xuid, auth, ide, scid, idi):

        urllib3.disable_warnings()

        payloadconquistar = {
            "action": "progressUpdate", "serviceConfigId": scid, "titleId": ide,
            "userId": xuid, "achievements": [{"id": idi, "percentComplete": 100}]}

        headersconquistar = {
            'Accept-Encoding': 'gzip, deflate',
            'x-xbl-contract-version': '2',
            'Cache-Control': 'no-cache',
            'User-Agent': 'XboxServicesAPI/2021.04.20210610.3 c',
            'accept': 'application/json',
            'accept-language': 'en-GB',
            'Content-Type': 'text/plain; charset=utf-8',
            'Authorization': auth,
            'Host': 'achievements.xboxlive.com',
            'Connection': None,
        }
        while True:
            try:
                responsi = requests.post(
                    f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                    json=payloadconquistar, headers=headersconquistar, verify=False)
                break
            except:
                continue
        if responsi.status_code == 200 or responsi.status_code == 304:
            pass
        elif responsi.status_code == 429:
            while responsi.status_code == 429:
                stdout.write(
                    "\r" + "Um Erro foi Encontrado, Esperando " + "5" + " segundos e tentando executar novamente")
                stdout.flush()
                time.sleep(5)
                while True:
                    try:
                        responsi = requests.post(
                            f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                            json=payloadconquistar, headers=headersconquistar, verify=False)
                        break
                    except:
                        continue
        else:
            pass

    def conquista(self, xuid, auth, authrewards):

        urllib3.disable_warnings()

        headersconquista = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': 'IT',
            'X-Rewards-Language': 'it-IT',
            'Authorization': authrewards,
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        ids = [1870475503, 2030093255]
        scids = ["00000000-0000-0000-0000-00006f7d30ef", "00000000-0000-0000-0000-00007900c3c7"]

        t1s = []
        for gameid, scid in zip(ids, scids):
            t = threading.Thread(target=self.ativar, args=(xuid, auth, gameid))
            t1s.append(t)

        for t1 in t1s:
            t1.start()
            t1.join()

        conquista = ["", ""]
        for gameid, scid in zip(ids, scids):
            while conquista[0] != "pcchild4_playe":
                for i in range(1, 21):
                    status = requests.get("https://prod.rewardsplatform.microsoft.com/dapi/me?channel=xboxapp&options=6", headers=headersconquista, verify=False).json()
                    itens = [tasks for tasks in status['response']["counters"] if tasks.__contains__("RewardsOnboarding")]
                    conquista = [tasks.replace("ENUS_xboxapp_punchcard_RewardsOnboarding_", "") for tasks in itens if tasks.__contains__("ENUS_xboxapp_punchcard_RewardsOnboarding_")]
                    conquista.sort()
                    t = threading.Thread(target=self.conquistar, args=(xuid, auth, gameid, scid, i))
                    t.start()
                    t.join()
                    if not len(conquista):
                        conquista = ["",""]
                    else:
                        if conquista[0] == "pcchild4_playe":
                            return True
                    if i >= 10:
                        break
                break
        return False

def checkpesquisa(authenticate, pais):
    headersfarm = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': "IT",
            'X-Rewards-Language': 'it-IT',
            'Authorization': f'{authenticate}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
    }

    while True:
        try:
            status = requests.get("https://prod.rewardsplatform.microsoft.com/dapi/me?channel=xboxapp&options=6",
                                headers=headersfarm, verify=False).json()
            itens = [tasks for tasks in status['response']["counters"] if tasks.__contains__("RewardsOnboarding")]
            taskspais = [tasks.replace(f"{pais}_xboxapp_punchcard_RewardsOnboarding_", "") for tasks in itens if tasks.__contains__(pais)]

            pesquisa = [quanto for quanto in taskspais if quanto.__contains__("pcchild2_searche")]
            try:
                vixe = status['response']["counters"][f"{pais}" + "_xboxapp_punchcard_RewardsOnboarding_" + pesquisa[0]]
            except:
                vixe = "0"
        except:
            continue
        return status['response']['balance'], str(vixe).split(";")[0]

class Farm:
    def TaskXbox(self, o, authenticate, country, mscv, cookies, getpoints=False):

        if authenticate is None:
            raise Exception('Coloque um authenticate valido')

        if getpoints:
            headersfarm = {
                'Cache-Control': 'no-cache',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'MS-CV': mscv,
                'Authorization': authenticate,
                'Connection': 'Keep-Alive',
                'Host': 'prod.rewardsplatform.microsoft.com',
            }
        else:
            headersfarm = {
                'Cache-Control': 'no-cache',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
                'X-Rewards-Country': country[-2:],
                'X-Rewards-Language': 'it-IT',
                'MS-CV': mscv,
                'Authorization': f'{authenticate}',
                'Connection': 'Keep-Alive',
                'Host': 'prod.rewardsplatform.microsoft.com',
            }

        cookie = {
            'Cookie': cookies
        }

        urllib3.disable_warnings()

        if getpoints:
            payloadfarm = {
                "id": "", "type": 101, "amount": 1, "country": f"{country[-2:]}",
                "attributes": {"offerid": "ENUS_readarticle3_30points"}
            }
        else:
            payloadfarm = {
                "id": "", "timestamp": "", "type": 80, "amount": 1, "country": f"{country[-2:]}", "retry_in_background": 'true',
                "attributes": {"offerid": f"{country}{o}"}
            }

        while True:
            try:
                tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payloadfarm,
                               headers=headersfarm, cookies=cookie, verify=False)
                break
            except:
                continue
        while tentar.status_code != 200:
            stdout.write(f"\rOcorreu um Erro 💀 , pais: {country[-2:]}")
            while True:
                try:
                    tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities',
                                   json=payloadfarm,
                                   headers=headersfarm, cookies=cookie, verify=False)
                    break
                except:
                    continue
            if tentar.status_code == 200:
                stdout.write("\rErro Resolvido 🔥")


    def RewardsRun(self, auths, mscv, cook, countries):

        headersfarm = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': "IT",
            'X-Rewards-Language': 'it-IT',
            'MS-CV': mscv,
            'Authorization': f'{auths}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        cookie = {
            'Cookie': cook
        }

        urllib3.disable_warnings()

        while True:
            threads = []
            taskscompletar = ["pcchild1_dset", "pcchild3_shope", "pcchild5_gpquest", "pcchild6_redeem", "pcchild7_app"]
            while True:
                try:
                    status = requests.get("https://prod.rewardsplatform.microsoft.com/dapi/me?channel=xboxapp&options=6", headers=headersfarm, cookies=cookie, verify=False).json()
                    break
                except:
                    continue
            itens = [tasks for tasks in status['response']["counters"] if tasks.__contains__("RewardsOnboarding")]
            taskspais = [tasks.replace(f"{countries}_xboxapp_punchcard_RewardsOnboarding_", "") for tasks in itens if tasks.__contains__(countries)]
            try:
                taskspais.remove("pcparent")
                taskspais.remove("pcchild2_searche")
            except:
                pass
            elementos_exclusivos = list(set(taskscompletar) - set(taskspais))
            if not len(elementos_exclusivos):
                break
            for o in elementos_exclusivos:
                o = "_xboxapp_punchcard_RewardsOnboarding_" + o
                t = threading.Thread(target=self.TaskXbox, args=(o, auths, countries, mscv, cook))
                threads.append(t)
                t.start()
            o = "_Welcome_Tour_XboxApp_Offer"
            t = threading.Thread(target=self.TaskXbox,args=(o, auths, countries, mscv, cook))
            threads.append(t)
            t.start()
            for t in threads:
                t.join()

    def getpoints(self, auths, mscv, cook, countries):
        t = threading.Thread(target=self.TaskXbox, args=(None, auths, countries, mscv, cook, True))
        t.start()
        t.join()


    def singletask(self, task, auth, mscv, cookie):
        o = "_xboxapp_punchcard_RewardsOnboarding_" + task

        headersfarm = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': "IT",
            'X-Rewards-Language': 'it-IT',
            'MS-CV': mscv,
            'Authorization': f'{auth}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        cookies = {
            'Cookie': cookie
        }

        urllib3.disable_warnings()

        payloadfarm = {
            "id": "", "timestamp": "", "type": 80, "amount": 1, "country": f"IT", "retry_in_background": 'true',
            "attributes": {"offerid": f"ITIT{o}"}
        }

        tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payloadfarm,
                               headers=headersfarm, cookies=cookies, verify=False)
        while tentar.status_code != 200:
            stdout.write(f"\rOcorreu um Erro 💀 , pais: IT")
            tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities',
                                   json=payloadfarm,
                                   headers=headersfarm, cookies=cookies, verify=False)
            if tentar.status_code == 200:
                stdout.write("\rErro Resolvido 🔥")

    def singlexbox(self, task, auth, mscv, cookie):
        if task == "pcchild1":
            o = "_xboxapp_" + task + "_xboxactivity_achievementpc_MayTopFive2023"
        else:
            o = "_xboxapp_" + task + "_urlreward_achievementpc_MayTopFive2023"

        headersfarm = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': "IT",
            'X-Rewards-Language': 'it-IT',
            'MS-CV': mscv,
            'Authorization': f'{auth}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        cookies = {
            'Cookie': cookie
        }
        urllib3.disable_warnings()

        payloadfarm = {
            "id": "", "timestamp": "", "type": 80, "amount": 1, "country": f"IT", "retry_in_background": 'true',
            "attributes": {"offerid": f"ENUS{o}"}
        }

        tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payloadfarm,
                               headers=headersfarm, cookies=cookies, verify=False)
        while tentar.status_code != 200:
            stdout.write(f"\rOcorreu um Erro 💀 , pais: IT")
            tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities',
                                   json=payloadfarm,
                                   headers=headersfarm, cookies=cookies, verify=False)
            if tentar.status_code == 200:
                stdout.write("\rErro Resolvido 🔥")

if __name__ == '__main__':
    paises = ['ESES', 'ENUS', 'JAJP', 'PTBR', 'ITIT', 'FRFR', 'NLNL', 'DEDE', 'ENGB', 'ESMX']

    farm = Farm()

    print("Paises disponiveis:")
    for i in paises:
        print(i)
    pais = input("Selecione o pais para pegar a task\n>>> ")

    if not pais.upper() in paises: raise Exception("Digite um valor valido!")

    with open(f"C:/Farm/rewards/{os.getlogin()}.txt", "r") as file:
        lines = file.readlines()
        authorization = [linha for linha in lines if linha.__contains__("Authorization: ")][
            0].strip().replace("Authorization: ", "")

        ms = [linha for linha in lines if linha.__contains__("MS-CV: ")][0].strip().replace("MS-CV: ", "")

        cookie = [linha for linha in lines if linha.__contains__("Cookie: ")][0].strip().replace("Cookie: ", "")

        farm.getpoints(authorization, ms, cookie, pais.upper())

