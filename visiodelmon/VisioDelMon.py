#aquí només hi ha la classe de VisioDelMon

#visiodelmon és la carpeta
from visiodelmon.MonPunt import *
from visiodelmon.FinPunt import *
import math

# puc definir tranquilament les mides de pantalla que jo vulga
# ja que dins de visiodelmon quan busquem l'escala farem
# 1000/24 (amplada finestra / amplada mon) 
# i això dona 41.6 píxels per metre ja sigui en horitz o vertical
# per tant, si la pantalla fa 1000x600
# veurem a baix 24 metres i a dalt 14.4 metres
#             14.4= 24/1000 * 600
# amplada_mon/amplada_finestra * altura_finestra

class VisioDelMon:
    def __init__(self, amplada_mon, altura_mon, amplada_finestra, altura_finestra):
        self.MA = MonPunt(0, 0)
        self.MB = MonPunt(amplada_mon, 0)
        self.MC = MonPunt(amplada_mon, altura_mon)
        self.MD = MonPunt(0, altura_mon)

        self.FA = FinPunt(0, 0)
        self.FB = FinPunt(amplada_finestra, 0)
        self.FC = FinPunt(amplada_finestra, altura_finestra)
        self.FD = FinPunt(0,  altura_finestra)

        
        self.amplada_mon=amplada_mon
        self.altura_mon = altura_mon
        self.amplada_finestra=amplada_finestra
        self.altura_finestra=altura_finestra

        # Calculem l'escala inicial (píxels per metre)
        # Amplada pantalla (pixels) / Amplada món (metres)
        self.pixels_per_metre = amplada_finestra / amplada_mon
        
        # Variables de la càmera (posició i direcció)
        self.cam_x = 0
        self.cam_y = 0 # Per defecte al punt (0,0)
        self.v_x = 0
        self.v_y = 1 # Per defecte mirant amunt (0,1)
        self.w_x = 1
        self.w_y = 0 # Per defecte mirant a la dreta (1,0)

        self.centre_finestra_x = (self.FC.x + self.FA.x) / 2
        self.centre_finestra_y = (self.FC.y + self.FA.y) / 2

    # on és el cotxe i cap a on mira
    def centraFinestra(self, x_cotxe, y_cotxe, dir_x, dir_y):
        self.cam_x = x_cotxe
        self.cam_y = y_cotxe

        modul = math.sqrt(dir_x**2 + dir_y**2)
        if modul > 0:
            self.v_x = dir_x / modul
            self.v_y = dir_y / modul
        else:
            self.v_x = 0
            self.v_y = 1
        
        self.w_x = self.v_y
        self.w_y = -self.v_x

    def monAfinestra(self, Mp: MonPunt) -> FinPunt:
        #Vector des del cotxe fins al punt que volem pintar
        u_x = Mp.x - self.cam_x
        u_y = Mp.y - self.cam_y

        # u*v
        # Distància "endavant" (sobre la direcció del cotxe)
        dist_endavant = u_x * self.v_x + u_y * self.v_y
        
        # u*w
        # Distància "dreta" (sobre la perpendicular del cotxe)
        dist_dreta = u_x * self.w_x + u_y * self.w_y

        # Coordenada X pantalla: Centre + distància dreta * escala
        fx = self.centre_finestra_x + (dist_dreta * self.pixels_per_metre)
        
        # Coordenada Y pantalla: Centre - distància endavant * escala
        # (Restem perquè a la pantalla la Y creix cap avall)
        fy = self.centre_finestra_y - (dist_endavant * self.pixels_per_metre)

        return FinPunt(int(fx), int(fy))

    def monAfinestraXY(self, x: float, y: float) -> FinPunt:      
        return self.monAfinestra(MonPunt(x, y))