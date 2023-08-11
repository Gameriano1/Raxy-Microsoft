import time

import cv2
import pydirectinput
from mss import mss
import numpy as np
import pygetwindow as gw

class AImg:
    bbox = None
    def __init__(self, localimg, vvar, appname=None):
        self.VVAR = vvar
        self.READSCR = None
        self.LOCALIMG = localimg

        self.APPNAME = appname

    def analyzer(self, imagem, source, multiple=False):
        readimg = cv2.imread(self.LOCALIMG + '/' + imagem, cv2.COLOR_BGRA2GRAY)

        tela_cinza = cv2.cvtColor(source, cv2.COLOR_BGRA2GRAY)
        imagem_cinza = cv2.cvtColor(readimg, cv2.COLOR_BGRA2GRAY)

        result = cv2.matchTemplate(tela_cinza, imagem_cinza, cv2.TM_CCOEFF_NORMED)

        if not multiple:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= self.VVAR:
                ocorrencias_encontradas = []

                W = imagem_cinza.shape[1]
                H = imagem_cinza.shape[0]
                x = max_loc[0]
                y = max_loc[1]

                ocorrencias_encontradas.append((x, y ,W, H))
                return ocorrencias_encontradas
            else:
                return None
        else:

            resultado = cv2.matchTemplate(tela_cinza, imagem_cinza, cv2.TM_CCOEFF_NORMED)

            locais = np.where(resultado >= self.VVAR)

            if locais[0].size == 0 or locais[1].size == 0:
                return None

            ocorrencias_encontradas = []
            for (x, y) in zip(*locais[::-1]):
                W, H = imagem_cinza.shape[1], imagem_cinza.shape[0]
                ocorrencias_encontradas.append((x, y, W, H))

            return ocorrencias_encontradas

    def clicar(self, x, y, W, H):
        X = x + int(W / 2) + AImg.bbox[0]
        Y = y + int(H / 2) + AImg.bbox[1]

        pydirectinput.click(X, Y)

    def printar(self):
        app_window = gw.getWindowsWithTitle(self.APPNAME)[0]
        left, top, width, height = app_window.left, app_window.top, app_window.width, app_window.height

        AImg.bbox = (left, top, left + width, top + height)

        with mss() as sct:
            capture_options = {
                "top": top,
                "left": left,
                "width": width,
                "height": height,
            }
            screenshot = sct.grab(capture_options)
            screenshot_np = np.array(screenshot)

            screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2BGR)
            return screenshot_cv

    def WaitUntil(self, source, timeout=15, *click):
        i = 0
        screen = self.printar()
        element = self.analyzer(source, screen)
        while element is None:
            screen = self.printar()
            element = self.analyzer(source, screen)
            if element:
                break
            else:
                time.sleep(1)
                i += 1
            if i > timeout:
                raise Exception("Timeout Quebrou")
        if not click:
            x, y, W, H = element[0]
            self.clicar(x, y, W, H)

    def MultipleElements(self, source, func, timeout=15):
        i = 0
        screen = self.printar()
        element = self.analyzer(source, screen, True)
        while element is None:
            screen = self.printar()
            element = self.analyzer(source, screen, True)
            if element:
                break
            else:
                time.sleep(1)
                i += 1
            if i > timeout:
                raise Exception("Timeout Quebrou")
        for ocorrencia in element:
            x, y, W, H = ocorrencia
            self.clicar(x, y, W, H)
            try:
                func()
            except Exception as e:
                raise Exception(e)

    def WaitDisappear(self, source, timeout=15):
        i=0
        screen = self.printar()
        elemento = self.analyzer(source, screen)
        while elemento:
            screen = self.printar()
            elemento = self.analyzer(source, screen)
            if not elemento:
                break
            else:
                time.sleep(1)
                i += 1
            if i > timeout:
                raise Exception("Timeout Quebrou")

    def WaitIf(self, timeout=15, *sources):
        i = 0
        element = False
        while not element:
            for num, source in enumerate(sources, start=1):
                screen = self.printar()
                element = self.analyzer(source, screen)
                if element:
                    return f"{num} Valido"
                else:
                    time.sleep(1)
                    i += 1
                if i > timeout:
                    raise Exception("Timeout Quebrou")

    def Exists(self, source):
        screen = self.printar()
        elemento = self.analyzer(source, screen)
        if elemento:
            return True
        else:
            return False


if __name__ == '__main__':
    aiai = AImg("imgs", 0.9)

    aiai.WaitUntil("sarvo.png")


