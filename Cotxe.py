# Aquí només hi ha la classe de Cotxe
import math
from visiodelmon.MonPunt import *

class Cotxe:

    def __init__(self,x,y,ampl,altu,direccio_x, direccio_y):
        modul = math.sqrt(direccio_x**2 + direccio_y**2)
        self.ampl = ampl
        self.altu = altu
        self.direccio_x=direccio_x / modul if modul>0 else 0
        self.direccio_y=direccio_y / modul if modul>0 else 0

        # x_centre, y_centre és el centre del cotxe
        self.x_centre=x
        self.y_centre=y

        self.v = 0             # Velocitat inicial
        self.v_max = 50.0     # Velocitat màxima
        self.acceleracio = 2.0 
        self.friccio = 0.99    
        self.frenada = 4.0     # la frenada és més forta que l'acceleració

    def mou(self, temps_frame_segons):
        # km/h * 1/3600 * 1000/1 = m/s
        # km/h = 3.6 m/s
        # m/s = km/h / 3.6
        
        metres_per_segon = self.v / 3.6
        
        # Distància = Velocitat (m/s) * Temps (s)
        distancia_metres = metres_per_segon * temps_frame_segons
        
        self.x_centre += distancia_metres * self.direccio_x
        self.y_centre += distancia_metres * self.direccio_y
        
        self.x = self.x_centre - (self.altu/2 * self.direccio_x)
        self.y = self.y_centre - (self.altu/2 * self.direccio_y)

        return MonPunt(self.x_centre, self.y_centre)
    
    
    def gira(self, angle_radians):
        #Angle positiu -> Gira a l'esquerra (antihorari)
        #Angle negatiu -> Gira a la dreta (horari)

        # x' = x cos(theta) - y sin(theta)
        # y' = x sin(theta) + y cos(theta)

        nou_dx = self.direccio_x * math.cos(angle_radians) - self.direccio_y * math.sin(angle_radians)
        nou_dy = self.direccio_x * math.sin(angle_radians) + self.direccio_y * math.cos(angle_radians)
        
        # Normalitzem
        modul = math.sqrt(nou_dx**2 + nou_dy**2)
        if modul > 0:
            self.direccio_x = nou_dx / modul
            self.direccio_y = nou_dy / modul

    def pinta(self, w, vm):
        # Vector Endavant (ux, uy)
        ux = self.direccio_x
        uy = self.direccio_y
        
        # Vector  perpendicular (px, py) 
        px = -self.direccio_y
        py = self.direccio_x
        
        # Centre del cotxe 
        cx = self.x_centre
        cy = self.y_centre

        # Li donem: quant "endavant" i quant "de costat" volem anar des del centre
        def get_pos(endavant, costat):
            mx = cx + (ux * endavant) + (px * costat)
            my = cy + (uy * endavant) + (py * costat)
            p = vm.monAfinestraXY(mx, my)
            return p.x, p.y

        
        meitat_altura = self.altu / 2  # Longitud (mig cotxe)
        meitat_ample = self.ampl / 2 # Amplada (mig cotxe)
        
        # Rodes Davanteres
        w.create_line(get_pos(meitat_altura*0.6, - meitat_ample *1.2), get_pos(meitat_altura*0.6, -meitat_ample*0.6), width=4, fill="black") # Esq
        w.create_line(get_pos(meitat_altura*0.6, meitat_ample*1.2), get_pos(meitat_altura*0.6, meitat_ample*0.6), width=4, fill="black")  # Dreta
        # Rodes Darreres
        w.create_line(get_pos(-meitat_altura*0.6, -meitat_ample*1.2), get_pos(-meitat_altura*0.6, -meitat_ample*0.6), width=4, fill="black")
        w.create_line(get_pos(-meitat_altura*0.6, meitat_ample*1.2), get_pos(-meitat_altura*0.6, meitat_ample*0.6), width=4, fill="black")

        # El cotxe roig
        w.create_polygon(
            get_pos(-meitat_altura, -meitat_ample), # Darrere esq
            get_pos(meitat_altura, -meitat_ample),  # Davant esq
            get_pos(meitat_altura, meitat_ample),   # Davant dret
            get_pos(-meitat_altura, meitat_ample),  # Darrere dret
            fill="#D32F2F", outline="black", width=1 # Vermell esportiu
        )

        # Parabrisa (Blau cel) - Un trapezi al davant
        w.create_polygon(
            get_pos(meitat_altura*0.1, -meitat_ample*0.8), # Base sostre
            get_pos(meitat_altura*0.4, -meitat_ample*0.7), # Capó
            get_pos(meitat_altura*0.4, meitat_ample*0.7), 
            get_pos(meitat_altura*0.1, meitat_ample*0.8), 
            fill="#81D4FA" # Blau clar
        )
        
        # Vidre Darrere (Blau fosc)
        w.create_polygon(
            get_pos(-meitat_altura*0.4, -meitat_ample*0.8), 
            get_pos(-meitat_altura*0.1, -meitat_ample*0.8),
            get_pos(-meitat_altura*0.1, meitat_ample*0.8), 
            get_pos(-meitat_altura*0.4, meitat_ample*0.8),
            fill="#4FC3F7"
        )
    
        # llums grogues davant
        w.create_line(get_pos(meitat_altura, -meitat_ample*0.7), get_pos(meitat_altura, -meitat_ample*0.3), width=3, fill="yellow")
        w.create_line(get_pos(meitat_altura, meitat_ample*0.7), get_pos(meitat_altura, meitat_ample*0.3), width=3, fill="yellow")
        
        # Llums roges detràs
        w.create_line(get_pos(-meitat_altura, -meitat_ample*0.7), get_pos(-meitat_altura, -meitat_ample*0.3), width=3, fill="#FF5252")
        w.create_line(get_pos(-meitat_altura, meitat_ample*0.7), get_pos(-meitat_altura, meitat_ample*0.3), width=3, fill="#FF5252")

    def centre(self):
        return MonPunt(self.x_centre, self.y_centre)
    
    def distancia_cotxe(self, punt_inicial: MonPunt):
        return self.centre().distancia(punt_inicial)