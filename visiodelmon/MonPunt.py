# aquí només hi ha la classe de MonPunt que és un punt del mon 

import math

class MonPunt:
    def __init__(self, x, y):  
        self.x = x
        self.y = y

    #Calcula la distància entre 2 MonPunt's
    def distancia(self, un_altre_monpunt):
        return math.sqrt((self.x - un_altre_monpunt.x)**2 + (self.y - un_altre_monpunt.y)**2)
    
    def recta(self,un_altre_monpunt):
        # tenim els punt P=(self.x,self.y) i Q=(un_altre_monpunt.x,un_altre_monpunt.y)
        # el vector PQ= (un_altre_monpunt.x - self.x,un_altre_monpunt.y - self.y)
        # l'ortogonal a PQ és (-un_altre_monpunt.y + self.y,un_altre_monpunt.x - self.x) = (a,b)
        a=self.y - un_altre_monpunt.y 
        b=un_altre_monpunt.x - self.x
        # busco c tq a*x + b*y +c =0
        c= -( a*self.x + b*self.y )

        #això defineix la recta de P a Q
        # i si un punt x,y esta a una banda de la recta donarà a*x + b*y +c >0
        # i si està a l'altra banda de la recta donarà a*x + b*y +c <0

        return a,b,c


    #Per mostrar els valors en cas de fer un print a un objecte d'aquesta classe
    def __repr__(self):
        return f"El punt del mon: ({self.x},{self.y})"
    
    def __iter__(self):
        # Això serveix per fer:
        #x, y = MonPunt(10, 20)      # Ara x valdrà 10 i y valdrà 20   
        yield self.x
        yield self.y

    def __add__(self, monpunt):# per poder fer una suma de punts
        nou_x = self.x + monpunt.x
        nou_y = self.y + monpunt.y
        return MonPunt(nou_x, nou_y)

    def __sub__(self, monpunt):# per poder fer una resta de punts
        nou_x = self.x - monpunt.x
        nou_y = self.y - monpunt.y
        return MonPunt(nou_x, nou_y)