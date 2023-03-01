import requests as r


def conquista(xuid, auth):

    payload = {
        "titles": [{"expiration": 600, "id": 2013672301, "state": "active", "sandbox": "RETAIL"}]
    }

    payload2 = {
        "action": "progressUpdate", "serviceConfigId": "00000000-0000-0000-0000-00007806336d", "titleId": 2013672301,
        "userId": xuid, "achievements": [{"id": 1, "percentComplete": 100}, {"id": 2, "percentComplete": 100}, {"id": 3, "percentComplete": 100}]}

    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'x-xbl-contract-version': '3',
        'Authorization': auth,
        'Cache-Control': 'no-cache'
    }

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

    response = r.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current", json=payload, headers=headers1, verify=False)
    if response.status_code != 200:
        response.raise_for_status()

    responsi = r.post(f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/00000000-0000-0000-0000-00007806336d/update?", json=payload2, headers=headers2, verify=False)
    if responsi.status_code == 200 or responsi.status_code == 304:
        print("Conquista conquistada com sucesso! 🤩")
        print("-------------------------------------")
    else:
        print(f"Algo deu errado, {responsi.status_code} ❌")



if __name__ == '__main__':
    conquista()
