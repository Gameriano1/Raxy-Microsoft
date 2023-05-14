import requests
import urllib3
import time
from sys import stdout
import threading


class Xbox:
    def ativar(xuid: str, auth, ide):
        payload = {
            "titles": [{"expiration": 600, "id": ide, "state": "active", "sandbox": "RETAIL"}]
        }

        headers1 = {
            'Accept-Encoding': 'gzip, deflate',
            'x-xbl-contract-version': '3',
            'Authorization': auth,
            'Cache-Control': 'no-cache'
        }

        response = requests.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                                 json=payload,
                                 headers=headers1, verify=False)
        if response.status_code != 200:
            p = 16
            while response.status_code != 200:
                stdout.write(
                    "\r" + "Um Erro foi Encontrado, Esperando " + str(p) + " segundos e tentando executar novamente")
                stdout.flush()
                time.sleep(p)
                response = requests.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                                         json=payload,
                                         headers=headers1, verify=False)

    def conquistar(xuid, auth, ide, scid):

        payload2 = {
            "action": "progressUpdate", "serviceConfigId": scid, "titleId": ide,
            "userId": xuid, "achievements": [{"id": 1, "percentComplete": 100}, {"id": 2, "percentComplete": 100},
                                             {"id": 3, "percentComplete": 100}, {"id": 4, "percentComplete": 100}]}

        headers2 = {
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

        responsi = requests.post(
            f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
            json=payload2, headers=headers2, verify=False)
        if responsi.status_code == 200 or responsi.status_code == 304:
            pass
        elif responsi.status_code == 429:
            while responsi.status_code == 429:
                stdout.write(
                    "\r" + "Um Erro foi Encontrado, Esperando " + "30" + " segundos e tentando executar novamente")
                stdout.flush()
                time.sleep(30)
                responsi = requests.post(
                    f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                    json=payload2, headers=headers2, verify=False)
        else:
            pass

    def conquista(xuid, auth):
        ids = [629270283, 1870475503]
        scids = ["0b0a0100-e8bd-4d11-a41c-80aa2581e70b", "00000000-0000-0000-0000-00006f7d30ef"]

        t1s = []
        for gameid, scid in zip(ids, scids):
            t = threading.Thread(target=Xbox.ativar, args=(xuid, auth, gameid))
            t1s.append(t)

        t2s = []
        for gameid, scid in zip(ids, scids):
            t = threading.Thread(target=Xbox.conquistar, args=(xuid, auth, gameid, scid))
            t2s.append(t)

        for t1 in t1s:
            t1.start()
            t1.join()
        for t2 in t2s:
            t2.start()
            t2.join()


class Farm:
    def TaskXbox(o, authenticate, countries, cc, j, cookies):

        urllib3.disable_warnings()

        if authenticate is None:
            raise Exception('Coloque um authenticate valido')

        payload = {
            "id": "", "timestamp": "", "type": 80, "amount": 1, "country": f"{cc}", "retry_in_background": 'true',
            "attributes": {"offerid": f"{countries}{o}"}
        }

        headers = {
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate',
            'X-Rewards-AppId': 'RewardsAppOnXbox v1.1.1.0',
            'X-Rewards-Country': f'{cc}',
            'X-Rewards-Language': 'pt-BR',
            'MS-CV': j,
            'Authorization': f'{authenticate}',
            'Connection': 'Keep-Alive',
            'Host': 'prod.rewardsplatform.microsoft.com',
        }

        cu = {
            'Cookie': cookies
        }

        tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payload,
                               headers=headers, cookies=cu, verify=False)
        while tentar.status_code != 200:
            stdout.write(f"\rOcorreu um Erro 💀 , pais: {cc}")
            tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payload,
                                   headers=headers, cookies=cu, verify=False)
            if tentar.status_code == 200:
                stdout.write("\rErro Resolvido 🔥")

    def RewardsRun(auths, je, ye):
        threads = []
        offers = ["_Welcome_Tour_XboxApp_Offer", "_xboxapp_punchcard_RewardsOnboarding_pcparent",
                  "_xboxapp_punchcard_RewardsOnboarding_pcchild1_dset",
                  "_xboxapp_punchcard_RewardsOnboarding_pcchild3_shope",
                  "_xboxapp_punchcard_RewardsOnboarding_pcchild5_gpquest",
                  "_xboxapp_punchcard_RewardsOnboarding_pcchild6_redeem",
                  "_xboxapp_punchcard_RewardsOnboarding_pcchild7_app", ]
        countries = ['ITIT', 'ENNZ', 'PTBR']
        cc = ['IT', 'NZ', 'BR']
        for c, ccc in zip(countries, cc):
            for o in offers:
                t = threading.Thread(target=Farm.TaskXbox, args=(o, auths, c, ccc, je, ye))
                threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
