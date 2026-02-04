from visiodelmon.MonPunt import *
from visiodelmon.FinPunt import *
from visiodelmon.VisioDelMon import *
from Cotxe import *
from Tram import *
import time

class CentrarCarretera:
    def __init__(self, w, carreteres, vm, altura_pantalla_mon):
        self.w = w
        self.carreteres = carreteres
        self.vm = vm

        self.altura_pantalla_mon=altura_pantalla_mon
        
        self.comptador=0
        self.comptador2=0
        
        self.inici = carreteres[0].punt_central_inicial()
        
        self.generar_punts_inicials()

        self.temps_inici_tram = time.time() # Guardem l'hora actual com a punt de partida


    def generar_punts_inicials(self):
        self.punts_inicial = []
        self.estat_monedes = []
        
        for c in self.carreteres:
            p4 = c.punt_central_inicial()
            self.punts_inicial.append(p4)
            self.estat_monedes.append("activada")

        self.punts_inicial.append(self.carreteres[-1].punt_central_final())
        self.estat_monedes.append("activada")

        # la primera moneda la desactivo:
        self.estat_monedes[0]="desactivada"
        
    def saber_si_cotxe_dins_recta(self,cotxe,p1,p2,paraula):
        x,y= cotxe.centre()

        a, b, c = p1.recta(p2) 

        # a*x + b*y +c =0 és la recta entre p1 i p2
        
        valor_cotxe = a*x + b*y + c
        if paraula=="inici":
            p_interior = self.carreteres[self.comptador].punt_central_inicial()

        if paraula=="final":
            p_interior = self.carreteres[self.comptador].punt_central_final()  
        
        valor_interior = a*p_interior.x + b*p_interior.y + c

        return valor_cotxe, valor_interior
        
    def saber_tram_actual(self,cotxe,d):
        p1 = self.carreteres[self.comptador].punt_esq_final()
        p3 = self.carreteres[self.comptador].punt_dret_final()

        valor_cotxe_final, valor_interior_final= self.saber_si_cotxe_dins_recta(cotxe,p1,p3,"inici")

        # Si multipliquem dos números i dona negatiu, vol dir que tenen signes diferents.
        # Això vol dir que el cotxe i l'inici estan a costats oposats de la meta.
        p0 = self.carreteres[self.comptador].punt_esq_inicial()
        p2 = self.carreteres[self.comptador].punt_dret_inicial()

        valor_cotxe_inicial, valor_interior_inicial= self.saber_si_cotxe_dins_recta(cotxe,p0,p2, "final")

        if valor_cotxe_final * valor_interior_final <= 0:
            # hem superat un tram
            self.comptador = self.comptador + 1
            #print(f"TRAM {self.comptador} SUPERAT!\n {self.carreteres[self.comptador]}")
            if self.saber_si_cotxe_fora(cotxe)==0:
                # si el cotxe està dins la carretera
                if self.estat_monedes[self.comptador]=="activada":
                    # si la moneda està activada
                    ara = time.time()
                    temps_tardat = ara - self.temps_inici_tram
                    
                    # Reiniciem el rellotge pel següent tram immediatament
                    self.temps_inici_tram = ara

                    # Evitem dividir per 0
                    if temps_tardat < 0.1: 
                        temps_tardat = 0.1
                    
                    # com més ràpid anem més punts obtenim
                    bonus = int(500 / temps_tardat)
                    d.dibuixar_bonus(bonus)
                    self.estat_monedes[self.comptador]="desactivada"

                    self.puntuacio = self.puntuacio+bonus
                    self.vida=self.vida+5
        

        if self.comptador>0:
            if valor_cotxe_inicial * valor_interior_inicial <= 0:
                self.comptador = self.comptador - 1
                #print(f"HEM TORNAT ENRERE\n TRAM {self.comptador} \n {self.carreteres[self.comptador]}")
            
    def saber_si_cotxe_fora(self,cotxe):
        p0 = self.carreteres[self.comptador].punt_esq_inicial()
        p1 = self.carreteres[self.comptador].punt_esq_final()

        valor_cotxe_e, valor_interior_e= self.saber_si_cotxe_dins_recta(cotxe,p0,p1,"inici")

        p2 = self.carreteres[self.comptador].punt_dret_inicial()
        p3 = self.carreteres[self.comptador].punt_dret_final()

        valor_cotxe_d, valor_interior_d= self.saber_si_cotxe_dins_recta(cotxe,p2,p3,"inici")

        if valor_cotxe_e * valor_interior_e <= 0 or valor_cotxe_d * valor_interior_d <= 0:
            self.vida=self.vida-2
            return 1
            #EL COTXE HA SORTIT DE LA CARRETERA
        else:
            return 0
        
 
    def actualitza(self, cotxe,PUNTUACIO,d, VIDA):
        self.puntuacio=PUNTUACIO
        self.vida=VIDA

        self.saber_tram_actual(cotxe,d)
        self.saber_si_cotxe_fora(cotxe)
        punt_final_mon = self.punts_inicial[-1]
        distancia_al_final = cotxe.distancia_cotxe(punt_final_mon)

        if(distancia_al_final<self.altura_pantalla_mon):
            self.mes_carreteres()
            self.comptador2=self.comptador2+1

        
# això és per fer la carretera ifinita
    def mes_carreteres(self):
        t1=self.carreteres[-1]
        centre_x_inici, centre_y_inici = t1.punt_central_final()
        esq_x_inici,esq_y_inici = t1.punt_esq_final()
        dret_x_inici,dret_y_inici = t1.punt_dret_final()
        tram_nou=Tram(centre_x_inici,centre_y_inici,
                esq_x_inici,esq_y_inici,
                dret_x_inici,dret_y_inici,
                     self.carreteres[self.comptador2].dir_x, self.carreteres[self.comptador2].dir_y,
                       self.carreteres[self.comptador2].distancia)
        self.carreteres.append(tram_nou)
        self.punts_inicial.append(tram_nou.punt_central_final())
        self.estat_monedes.append("activada")

        
    def pinta(self,d):
        i=0
        # Recorrem TOTS els trams per pintar-los
        for c in self.carreteres:
            # Calculem punts del tram actual
            p0 = c.punt_esq_inicial()
            p1 = c.punt_esq_final()
            p2 = c.punt_dret_inicial()
            p3 = c.punt_dret_final()
            p4 = c.punt_central_inicial()
            p5 = c.punt_central_final()

            self.w.create_polygon(
                self.vm.monAfinestra(p0).x, self.vm.monAfinestra(p0).y,   # 1. Cantonada Esquerra Aprop
                self.vm.monAfinestra(p1).x, self.vm.monAfinestra(p1).y,   # 2. Cantonada Esquerra Lluny
                self.vm.monAfinestra(p3).x, self.vm.monAfinestra(p3).y,   # 3. Cantonada Dreta Lluny (Ull! és el p3)
                self.vm.monAfinestra(p2).x, self.vm.monAfinestra(p2).y,   # 4. Cantonada Dreta Aprop (Ull! és el p2)
                fill="#cf9e4a", # Color GRIS FOSC (Asfalt)
                outline=""      # Sense línia negra al voltant del quadrat
            )

            # Pintem vores laterals
            self.w.create_line(self.vm.monAfinestra(p0).x, self.vm.monAfinestra(p0).y,
                               self.vm.monAfinestra(p1).x, self.vm.monAfinestra(p1).y,
                               fill="white", width=3)
            self.w.create_line(self.vm.monAfinestra(p2).x, self.vm.monAfinestra(p2).y,
                               self.vm.monAfinestra(p3).x, self.vm.monAfinestra(p3).y,
                                 fill="white", width=3)

            
            # Pintem línia central
            self.w.create_line(self.vm.monAfinestra(p4).x, self.vm.monAfinestra(p4).y,
                               self.vm.monAfinestra(p5).x, self.vm.monAfinestra(p5).y,
                               fill="white", width=3, dash=(20, 50))
            
            if self.estat_monedes[i] == "activada":
                d.dibuixa_moneda_carretera(p4)

            i=i+1
            