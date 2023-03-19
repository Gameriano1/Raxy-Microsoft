import requests as r
import threading
import time
from sys import stdout

def ativar(xuid,auth,ide):
    payload = {
        "titles": [{"expiration": 600, "id": ide, "state": "active", "sandbox": "RETAIL"}]
    }

    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'x-xbl-contract-version': '3',
        'Authorization': auth,
        'Cache-Control': 'no-cache'
    }

    response = r.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current", json=payload,
                      headers=headers1, verify=False)
    if response.status_code != 200:
        p = 16
        while response.status_code != 200:
            stdout.write(
                "\r" + "Um Erro foi Encontrado, Esperando " + str(p) + " segundos e tentando executar novamente")
            stdout.flush()
            time.sleep(p)
            response = r.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                              json=payload,
                              headers=headers1, verify=False)



def conquistar(xuid ,auth ,ide ,scid ,v):

    payload2 = {
        "action": "progressUpdate", "serviceConfigId": scid, "titleId": ide,
        "userId": xuid, "achievements": [{"id": v, "percentComplete": 100}]}

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

    responsi = r.post(f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                      json=payload2, headers=headers2, verify=False)
    if responsi.status_code == 200 or responsi.status_code == 304:
        pass
    elif responsi.status_code == 429:
        while responsi.status_code == 429:
            stdout.write(
                "\r" + "Um Erro foi Encontrado, Esperando " + "30" + " segundos e tentando executar novamente")
            stdout.flush()
            time.sleep(30)
            responsi = r.post(
                f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                json=payload2, headers=headers2, verify=False)
    else:
        pass

def conquista(xuid, auth):
    ids = 2013672301
    scid = "00000000-0000-0000-0000-00007806336d"
    threads1 = []
    threads2 = []
    t = threading.Thread(target=ativar, args=(xuid, auth, ids))
    threads2.append(t)
    t.start()

    for t in threads2:
        t.join()

    for v in range(1,25):
        t = threading.Thread(target=conquistar, args=(xuid, auth, ids, scid, v))
        threads1.append(t)
        t.start()

    for t in threads1:
        t.join()


if __name__ == '__main__':
    conquista()
