import os
import requests

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


if __name__ == '__main__':
    if not os.path.exists("accs"):
        os.makedirs("accs")

    gerarcmd()

    dtb = "https://contas2-b9481-default-rtdb.firebaseio.com/"

    acao = input("Digite D para deletar todas as contas salvas em farmando,C para deletar conta especifica, O para deletar outro ou qualquer outra tecla para puxar as contas\n>>> ")
    print("\n")

    if acao.lower() == "d":
        req = requests.delete(f"{dtb}Usuarios/Farmando/{os.getlogin()}/.json", verify=False)
        print("Operação Feita")

    elif acao.lower() == "o":
        metodo = input("Primeiro fale o que quer deletar (Concluido, Reembolsar ,Reembolso)\n>>> ")
        if metodo.lower() == "reembolso":
            req = requests.delete(f"{dtb}Usuarios/Reembolso/{os.getlogin()}/.json", verify=False)
            print("Operação Feita")
        elif metodo.lower() == "reembolsar":
            req = requests.delete(f"{dtb}Usuarios/Reembolsar/{os.getlogin()}/.json", verify=False)
            print("Operação Feita")
        elif metodo.lower() == "concluido":
            req = requests.delete(f"{dtb}Usuarios/Concluido/{os.getlogin()}/.json", verify=False)
            print("Operação Feita")
        else:
            raise Exception("Digite um valor valido!")


    elif acao.lower() == "c":
        metodo = input("Primeiro fale o que quer deletar (Concluido, Reembolsar ,Reembolso)\n>>> ")
        conta = input("Agora Fale a Conta que quer deletar email;senha\n>>> ")

        if metodo.lower() == "reembolso":
            dat = requests.get(f"{dtb}/Usuarios/Reembolso/{os.getlogin()}/.json", verify=False).json()

            for data_key, inner_dict in dat.items():
                for inner_key, inner_value in inner_dict.items():
                    if inner_value == conta:
                        requests.delete(f"{dtb}Usuarios/Reembolso/{os.getlogin()}/{data_key}/.json", verify=False)
        elif metodo.lower() == "reembolsar":
            dat = requests.get(f"{dtb}/Usuarios/Reembolsar/{os.getlogin()}/.json", verify=False).json()

            for data_key, inner_dict in dat.items():
                for inner_key, inner_value in inner_dict.items():
                    if inner_value == conta:
                        requests.delete(f"{dtb}Usuarios/Reembolsar/{os.getlogin()}/{data_key}/.json", verify=False)

        elif metodo.lower() == "Concluido":

            dat = requests.get(f"{dtb}/Usuarios/Concluido/{os.getlogin()}/.json", verify=False).json()

            for data_key, inner_dict in dat.items():
                for inner_key, inner_value in inner_dict.items():
                    current_value = inner_value.get('Current')
                    if current_value == conta:
                        requests.delete(f"{dtb}Usuarios/Concluido/{os.getlogin()}/{data_key}/{inner_key}/.json",
                                        verify=False)
        else:
            raise Exception("Digite um Valor Valido!")
        print("Operação Feita")
    else:
        acoes = ["Farmando", "Concluido", "Reembolsar", "Reembolso"]

        for act in acoes:
            try:
                req = requests.get(f"{dtb}Usuarios/{act}/{os.getlogin()}/.json", verify=False).json()
                if req is not None:
                    nome_arquivo = f"accs/{os.getlogin()}{act}.txt"

                    with open(nome_arquivo, 'a') as arquivo:
                        for inner_dict in req.values():
                            for inner_value in inner_dict.values():
                                try:
                                    current_value = inner_value.get('Current')
                                    arquivo.write(current_value + '\n')
                                except:
                                    arquivo.write(inner_value + '\n')
                                    pass

                    print("Valores salvos em", nome_arquivo)
            except:
                pass