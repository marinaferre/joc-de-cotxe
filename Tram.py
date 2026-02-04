import math

from visiodelmon.MonPunt import *
from visiodelmon.FinPunt import *

class Tram:   
    def __init__(self,punt_central_inicial_x,punt_central_inicial_y ,
                 punt_esq_inicial_x, punt_esq_inicial_y,
                   punt_dret_inicial_x,punt_dret_inicial_y,
                     direccio_x, direccio_y,
                       distancia):
        modul = math.sqrt(direccio_x**2 + direccio_y**2)
    
        self.punt_central_inicial_x=punt_central_inicial_x
        self.punt_central_inicial_y=punt_central_inicial_y
        self.punt_esq_inicial_x=punt_esq_inicial_x
        self.punt_esq_inicial_y=punt_esq_inicial_y
        self.punt_dret_inicial_x=punt_dret_inicial_x
        self.punt_dret_inicial_y=punt_dret_inicial_y
        self.dir_x=direccio_x/modul if modul >0 else 0
        self.dir_y=direccio_y/modul if modul >0 else 0
        self.distancia=distancia

        
    def punt_central_inicial(self) -> MonPunt:
        return MonPunt(self.punt_central_inicial_x,self.punt_central_inicial_y)
    
    def punt_esq_inicial(self) -> MonPunt:
        return MonPunt(self.punt_esq_inicial_x,self.punt_esq_inicial_y)
    
    def punt_dret_inicial(self) -> MonPunt:
        return MonPunt(self.punt_dret_inicial_x,self.punt_dret_inicial_y)

    def punt_final(self, mp : MonPunt) -> MonPunt:
            x=mp.x
            y=mp.y
            x_final= x + self.distancia * self.dir_x
            y_final= y + self.distancia * self.dir_y
            return MonPunt(x_final, y_final)
    
    def punt_central_final(self) -> MonPunt:
         return self.punt_final(self.punt_central_inicial())

    def punt_esq_final(self)-> MonPunt:
         return self.punt_final(self.punt_esq_inicial())
    
    def punt_dret_final(self)-> MonPunt:
        return self.punt_final(self.punt_dret_inicial())
    
    def __repr__(self):
        a=f'CARRETERA: la direcció és ({self.dir_x, self.dir_y})'
        b=f'\nla distància és {self.punt_central_inicial().distancia(self.punt_central_final())}'
        return a+b
    