
from tkinter import * # type: ignore
import time
import keyboard

from visiodelmon.FinPunt import *
from visiodelmon.MonPunt import *
from visiodelmon.VisioDelMon import *

from Tram import *
from Cotxe import *
from CentrarCarretera import *

from Dibuixos import *

from LecturesJson import *

llegir=LecturesJson()

carreteres=llegir.trams_json(fitxer="carretera.json")

cotxe=llegir.cotxes_json("carretera.json")[0]
#-------------------------------------------------------------------------------------------------------

altura_finestra= 600 
amplada_finestra= 1000 

amplada_mon=24
altura_mon=24

vm=VisioDelMon(amplada_mon, altura_mon, amplada_finestra, altura_finestra)

Fmin=vm.FA
Fmax=vm.FC

Mmin=vm.MA
Mmax=vm.MC

tk=Tk()
# he buscat Hex color picker a google per trobar el color verd
# si fas control click damunt de Canvas pots veure les funcions que té
w=Canvas(tk,width=Fmax.x,height=Fmax.y, background="#aee3a6" )
w.pack()

cc=CentrarCarretera(w,carreteres,vm, amplada_mon/amplada_finestra * altura_finestra )

d=Dibuixos(w,vm,cotxe)

FPS = 24 # frames per segon 
segons_per_frame = 1.0 / FPS # Això dona aprox 0.041 segons

def click_jugar():
    global estat_joc
    estat_joc = "jugant"
    # amaguem el botó per no veure'l mentre conduïm
    boto_inici.place_forget()

boto_inici = Button(w, text="COMENÇAR A JUGAR", 
                    command=click_jugar, 
                    font=("Impact", 20), 
                    bg="#8E305A", fg="black")

estat_joc= "menu"

while True:
    try:
        if not tk.winfo_exists():
            break

        if estat_joc=="menu":
            boto_inici.place(x=350, y=250, width=300, height=80) 
            PUNTUACIO=0
            VIDA=100
            cotxe.x_centre = cc.inici.x
            cotxe.y_centre = cc.inici.y

            cotxe.direccio_x = carreteres[0].dir_x
            cotxe.direccio_y = carreteres[0].dir_y

            cotxe.v=0

            cc.generar_punts_inicials()
            cc.temps_inici_tram = time.time()
        
        elif estat_joc=="jugant":

            w.delete("all")

            # 1. ACCELERACIÓ i FRENADA
            if keyboard.is_pressed("up arrow"):
                # Si prems amunt, accelerem fins al màxim
                if cotxe.v < cotxe.v_max:
                    cotxe.v += cotxe.acceleracio
            
            elif keyboard.is_pressed("down arrow"):
                # Si prems avall, frenem o anem marxa enrere
                if cotxe.v > 0:
                    cotxe.v -= cotxe.frenada # Frena fort
                else:
                    cotxe.v -= cotxe.acceleracio # Marxa enrere (més suau)
            
            else:
                # Si NO prems res, apliquem fricció (el cotxe perd inèrcia)
                cotxe.v *= cotxe.friccio
                
                # Si la velocitat és molt petita, el parem del tot per no tenir decimals infinits
                if abs(cotxe.v) < 0.5:
                    cotxe.v = 0

            # 2. GIR 

            if keyboard.is_pressed("left arrow"):
                cotxe.gira(0.05 )
                
            if keyboard.is_pressed("right arrow"):
                cotxe.gira(-0.05 )

            cotxe.mou(segons_per_frame)

            #----------
            vm.centraFinestra(
                cotxe.x_centre, 
                cotxe.y_centre, 
                cotxe.direccio_x, 
                cotxe.direccio_y
            )
            cc.actualitza(cotxe,PUNTUACIO,d,VIDA)
            PUNTUACIO=cc.puntuacio
            VIDA=cc.vida

            d.pintar_gespa()

            cc.pinta(d)
            
            cotxe.pinta(w,vm)

            d.dibuixa_velocitat()

            d.dibuixa_puntuacio(PUNTUACIO, cc.temps_inici_tram)

            VIDA=d.dibuixa_vida(VIDA)
            VIDA=VIDA-0.1 #disminueix sempre per no fer res

            if VIDA<0.1:
                estat_joc="menu"


        w.update()

        time.sleep(segons_per_frame)

    except TclError:
        break