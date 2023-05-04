import requests
import urllib3
from sys import stdout
import threading

def TaskXbox(o, authenticate,countries, cc, j, cookies):

    urllib3.disable_warnings()

    if authenticate == None:
        raise Exception('Coloque um authenticate valido')

    payload = {
            "id":"","timestamp":"","type":80,"amount":1,"country":f"{cc}","retry_in_background":'true',"attributes":{"offerid":f"{countries}{o}"}
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

    tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities',json=payload, headers=headers,cookies=cu, verify=False)
    while tentar.status_code != 200:
        stdout.write(f"\rOcorreu um Erro 💀 , pais: {cc}")
        tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payload,headers=headers, cookies=cu, verify=False)
        if tentar.status_code == 200:
            stdout.write("\rErro Resolvido 🔥")


def RewardsRun(auths, je, ye):
    threads = []
    offers = ["_Welcome_Tour_XboxApp_Offer", "_xboxapp_punchcard_RewardsOnboarding_pcparent",
              "_xboxapp_punchcard_RewardsOnboarding_pcchild1_dset",
              "_xboxapp_punchcard_RewardsOnboarding_pcchild3_shope",
              "_xboxapp_punchcard_RewardsOnboarding_pcchild5_gpquest",
              "_xboxapp_punchcard_RewardsOnboarding_pcchild6_redeem",
              "_xboxapp_punchcard_RewardsOnboarding_pcchild7_app",]
    for i in range(1, 6):
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_Overwatch2S4")
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_CODMW2S3")
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_APIHeritageMonth2023")
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_MilitaryUSOMonth2023")
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_RedfallBiteBackLaunch")
        offers.append(f"_xboxapp_pcchild{i}_urlreward_adhocpc_StarWarsMay4th")
    countries = ['ENUS', 'ENNZ']
    cc = ['US', 'NZ']
    for c, ccc in zip(countries, cc):
        for o in offers:
            t = threading.Thread(target=TaskXbox, args=(o, auths, c, ccc, je, ye))
            threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
