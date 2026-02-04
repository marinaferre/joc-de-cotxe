
import time
import random

class Dibuixos:
    def __init__(self, w,vm, cotxe):
        self.w=w
        self.vm=vm
        self.cotxe=cotxe
        self.puntuacio_anterior=0

        self.text_bonus = ""    
        self.temps_bonus = 0  # duració del bonus

        self.posicio_gespa_random = []
        quantitat_gespa = 300 

        for i in range(quantitat_gespa):
            # Triem una posició a l'atzar dins de la pantalla
            gx = random.randint(0, vm.amplada_finestra)
            gy = random.randint(0, vm.altura_finestra)
            
            # Mida random entre 2 i 5 píxels
            mida = random.randint(2, 5)
            
            self.posicio_gespa_random.append((gx, gy, mida))

    def pintar_gespa(self):
        for g in self.posicio_gespa_random:
            gx, gy, mida = g 
            
            # Dibuixem una "V"
            self.w.create_line(gx, gy, gx + 2, gy - mida, fill="#0c5202", width=1)
            self.w.create_line(gx + 2, gy - mida, gx + 4, gy, fill="#0c5202", width=1)

    def dibuixa_velocitat(self):
        x_base = 20
        y_base = 20
        
        velocitat = int(self.cotxe.v)

        self.w.create_text(x_base, y_base, text=f"{velocitat} km/h", 
                    font=("Impact", 24), fill="#A0A0A0", anchor="nw")

        barra_amplada = 200
        barra_altura = 15
        y_barra = y_base + 40 
        
        v_max = self.cotxe.v_max
            
        percentatge = self.cotxe.v / v_max
        
        if percentatge > 1: 
            percentatge = 1
        
        color_barra = "#00FF00"
        
        if percentatge > 0.9:
            color_barra = "#FF0000"
            
        # Fons de la barra
        self.w.create_rectangle(x_base, y_barra, x_base + barra_amplada, y_barra + barra_altura,
                                fill="#333333", outline="white", width=2)
                        
        # Interior de la barra
        if percentatge > 0:
            amplada_actual = barra_amplada * percentatge
            self.w.create_rectangle(x_base, y_barra, x_base + amplada_actual, y_barra + barra_altura,
                                    fill=color_barra, outline="")


    def dibuixa_puntuacio(self, puntuacio, temps_inici): 

            x_base = 820  
            y_base = 20
            amplada_caixa = 150
            altura_caixa = 60

            # la caixa
            self.w.create_rectangle(x_base, y_base, x_base + amplada_caixa, y_base + altura_caixa, 
                                    fill="#333333", outline="white", width=2)
            # el títol de PUNTS
            centre_x = x_base + (amplada_caixa / 2)
            self.w.create_text(centre_x, y_base + 15, text="PUNTS", font=("Arial", 10, "bold"), fill="#aaaaaa")
            
            # 3. el valor
            self.w.create_text(centre_x, y_base + 40, text=str(puntuacio), font=("Impact", 24), fill="white")
            
            self.puntuacio_anterior = puntuacio

            #EL DIBUIX DEL BONUS
            
            # Calculem quant temps ha passat des de que ha agafat l'última moneda
            ara = time.time()
            temps_passat = ara - temps_inici
            if temps_passat < 0.1: 
                temps_passat = 0.1 # Evitem dividir per 0

            # Calculem quants punts ens donarien ARA MATEIX
            bonus_potencial = int(500 / temps_passat) 
            self.w.create_text(822, 35, text=f"+{bonus_potencial}", 
                               font=("Impact", 13), fill="#DE6DB9", anchor="w")
        

            #  Dibuixem el bonus que has guanyat
            if self.temps_bonus > 0:
                cx = 900
                cy = 100
                self.w.create_text(cx, cy, text=self.text_bonus, font=("Impact", 20), fill="#FFD700")
                self.temps_bonus -= 1

    def dibuixar_bonus(self, punts):
        #Activa el missatge de bonus perquè es mostri a la pantalla.
        self.text_bonus = f"+{punts} PTS"
        self.temps_bonus = 30  # Durarà 30 frames 

    def dibuixa_moneda_carretera(self,p4):
        radi_moneda=10

        self.w.create_oval(
                self.vm.monAfinestra(p4).x - radi_moneda, self.vm.monAfinestra(p4).y - radi_moneda, 
                self.vm.monAfinestra(p4).x + radi_moneda, self.vm.monAfinestra(p4).y + radi_moneda, 
                fill="#FFD700",  
                outline="orange", 
                width=2
            )

    def dibuixa_vida(self, vida_actual):
        x_base = 20
        y_base = 500  
        amplada_barra = 200
        altura_barra = 15

        if vida_actual < 0: vida_actual = 0
        if vida_actual > 100: vida_actual = 100

        self.w.create_rectangle(x_base, y_base, x_base + amplada_barra, y_base + altura_barra,
                                fill="#FFFFFF", outline="white", width=4)

        amplada_actual = (vida_actual / 100) * amplada_barra
        
        color = "#74ef58" 
        if vida_actual <= 50:
            color = "#f2f479"
        if vida_actual <= 20:
            color = "#f35543" 

        if vida_actual > 0:
            self.w.create_rectangle(x_base, y_base, x_base + amplada_actual, y_base + altura_barra,
                                    fill=color, outline="")

        self.w.create_text(x_base + (amplada_barra/2), y_base + 8, text=f"{int(vida_actual)}%", 
                           font=("Arial", 9, "bold"), fill="black")
        
        
        self.w.create_rectangle(x_base, y_base - 25, x_base + 35, y_base -5,
                                fill="#FFFFFF", outline="white", width=2)
        
        self.w.create_text(x_base + 2, y_base - 25, text="VIDA", 
                           font=("Impact", 12), fill="black", anchor="nw")
        
        return vida_actual

 