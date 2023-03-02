import glob
from bots.abs import ABS
from threading import Thread
from colorama import Fore
import threading
from bots.taskxbox import RewardsRun
from bots.xboxa import conquista

def processrewards():
    mscv = []
    authe = []
    cu = []
    threads = []

    my_files = glob.glob('rewards\*.txt')
    if not len(my_files):
        raise Exception("Arquivos Faltando")
    for s in my_files:
        with open(s, "r") as f:
            x = f.readlines()
            for o in x:
                if o.__contains__("Authorization: "):
                    h = o.strip()
                    h = h.replace("Authorization: ", "")
                    authe.append(h)
                if o.__contains__("MS-CV: "):
                    j = o.strip()
                    j = j.replace("MS-CV: ", "")
                    mscv.append(j)
                if o.__contains__("Cookie: "):
                    y = o.strip()
                    y = y.replace("Cookie: ", "")
                    cu.append(y)
    for v, i, u in zip(authe, mscv, cu):
        t = threading.Thread(target=RewardsRun, args=(v, i, u))
        threads.append(t)
        t.start()
    for t in threads:

        t.join()

def xboxrun():
    xuids = []
    aut = []
    threads = []

    my_files = glob.glob('xbox\*.txt')
    if not len(my_files):
        raise Exception("Arquivos Faltando")

    for s in my_files:
        with open(s, "r") as f:
            x = f.readlines()
            for o in x:
                if o.__contains__("Authorization: ") or o.__contains__("authorization: "):
                    z = o.strip()
                    z = z.replace("Authorization: ", "")
                    z = z.replace("authorization: ", "")
                    aut.append(z)
                if o.__contains__("users"):
                    b = o.strip()
                    b = b.replace("HTTP/1.1", "")
                    xuid = str(''.join(i for i in b if i.isdigit()))
                    xuids.append(xuid)
    for x, i in zip(xuids,aut):
        t = threading.Thread(target=conquista, args=(x,i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def bing():
    my_files = glob.glob('bing\*.txt')
    if not len(my_files):
        raise Exception("Arquivos Faltando")
    for s in my_files:
        with open(s, "r") as f:
            x = f.readlines()
            for o in x:
                if o.__contains__("Cookie: "):
                    h = o.strip()
                    h = h.replace("Cookie: ", "")
                    ABS(h)

def main():
    fazer = str(
        input("Fazer as tasks / conquista? S/N (OU T SÓ PARA AS TASKS / OU X PARA SÓ CONQUISTA / OU B SÓ PARA ABS)\n"))
    if fazer.lower() == "s":
        print(Fore.BLUE + "----------TASKS DO REWARDS-----------")
        xboxthread = Thread(target=processrewards)
        rewardsthread = Thread(target=xboxrun)
        rewardsthread.start()
        rewardsthread.join()
        xboxthread.start()
        xboxthread.join()
        print(Fore.GREEN + "Finalizado ✅")

    elif fazer.lower() == "t":
        print(Fore.BLUE + "----------TASKS DO REWARDS-----------")
        processrewards()
        print(Fore.GREEN + "Finalizado ✅")
    elif fazer.lower() == "x":
        print(Fore.MAGENTA + "-----------TASKS DO XBOX------------")
        xboxrun()
    elif fazer.lower() == "b":
        print(Fore.YELLOW + "-----------TASKS DO BING------------")
        bing()
        print(Fore.GREEN + "Finalizado ✅")
if __name__ == '__main__':
    main()
