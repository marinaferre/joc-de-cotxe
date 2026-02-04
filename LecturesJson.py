import math
import json

from Tram import *
from Cotxe import *

class LecturesJson:
    def trams_json(self,fitxer):
        f=open(fitxer,"r")
        dades=json.load(f)
        f.close()
        trams=[]

        centre_x_inici, centre_y_inici= dades['posicio_inicial'][0]['x'], dades['posicio_inicial'][0]['y']
        amplada= dades['posicio_inicial'][0]['amplada']
        dir_x_inici,dir_y_inici=dades['trams'][0]['direccio']['x'],dades['trams'][0]['direccio']['y']
        modul_inici = math.sqrt(dir_x_inici**2 + dir_y_inici**2)
        # contertim el vector (a,b) en (-b,a), el seu ortogonal cap a l'esquerra
        esq_x_inici= centre_x_inici -amplada/2 * dir_y_inici/modul_inici if modul_inici>0 else 0
        esq_y_inici= centre_y_inici +amplada/2 * dir_x_inici/modul_inici if modul_inici>0 else 0
        # contertim el vector (a,b) en (b,-a), el seu ortogonal cap a la dreta
        dret_x_inici= centre_x_inici +amplada/2 * dir_y_inici/modul_inici if modul_inici>0 else 0
        dret_y_inici= centre_y_inici -amplada/2 * dir_x_inici/modul_inici if modul_inici>0 else 0

        for t in dades['trams']:
            t1=Tram(centre_x_inici,centre_y_inici,
                    esq_x_inici,esq_y_inici,
                    dret_x_inici,dret_y_inici,
                    t['direccio']['x'],t['direccio']['y'],
                    t['distancia'])
            trams.append(t1)
            centre_x_inici, centre_y_inici = t1.punt_central_final()
            esq_x_inici,esq_y_inici = t1.punt_esq_final()
            dret_x_inici,dret_y_inici = t1.punt_dret_final()
        return trams

    def cotxes_json(self,fitxer):
        f=open(fitxer,"r")
        dades=json.load(f)
        f.close()
        cotxes=[]
        for c in dades['cotxes']:
            c1=Cotxe(dades['posicio_inicial'][0]['x'],dades['posicio_inicial'][0]['y'],c['amplada'], c['altura'],0,0)
            cotxes.append(c1) 
        return cotxes