import requests
import urllib3
import threading

def TaskXbox(authenticate,countries, cc, j, cookies):

    urllib3.disable_warnings()

    offers =["_Welcome_Tour_XboxApp_Offer","_xboxapp_punchcard_RewardsOnboarding_pcparent","_xboxapp_punchcard_RewardsOnboarding_pcchild1_dset","_xboxapp_punchcard_RewardsOnboarding_pcchild3_shope","_xboxapp_punchcard_RewardsOnboarding_pcchild5_gpquest","_xboxapp_punchcard_RewardsOnboarding_pcchild6_redeem","_xboxapp_punchcard_RewardsOnboarding_pcchild7_app"]

    if authenticate == None:
        raise Exception('Coloque um authenticate valido')

    for o in offers:

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
            print(f"Ocorreu um Erro 💀 , pais: {cc}, task: {o}")
            tentar = requests.post('https://prod.rewardsplatform.microsoft.com/dapi/me/activities', json=payload,headers=headers, cookies=cu, verify=False)
            if tentar.status_code == 200:
                print("Erro Resolvido 🔥")


def RewardsRun(auths, je, ye):
    print("Fazendo as Tasks do aplicativo... 🙃")
    threads = []
    countries = ['ENUS', 'PTBR', 'ENNZ']
    cc = ['US', 'BR', 'NZ']
    for c, ccc in zip(countries, cc):
        t = threading.Thread(target=TaskXbox, args=(auths, c, ccc, je, ye))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print("Tasks Completas! 😁")
    print("-------------------------------------")

if __name__ == "__main__":
    RewardsRun()