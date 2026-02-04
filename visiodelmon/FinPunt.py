# aquí només hi ha la classe de FinPunt que és un punt de la finestra virtual

class FinPunt:   #x,y són enters, ja que són pixels de pantalla
    def __init__(self,x,y):
        self.x=x
        self.y=y

    #Per mostrar els valors en cas de fer un print a un obejcte d'aquesta classe
    def __repr__(self):
        return f"El punt de la finestra: ({self.x},{self.y})"
    
