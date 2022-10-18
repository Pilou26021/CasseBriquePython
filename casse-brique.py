from balle_pygame import *
from pygame.locals import *
from time import sleep
import random
vitesse=0.01
largeur_fenetre = 800
hauteur_fenetre = 600

class Balle:
    def __init__(self,x=50,y=20,dx=-3,dy=2,taille=10):
        self.taille=taille
        self.x=x #position X
        self.y=y #position Y
        self.dx=dx #vitesse déplacement axe X
        self.dy=dy #vitesse déplacement axe Y
        
    def avancer(self):
        self.x=self.x+self.dx
        self.y=self.y+self.dy
        self.rebond()
    
    def tracer(self):
        tracerBalle(fenetre,self)
        
    def rebond(self):
        if largeur_fenetre-self.taille<self.x or self.x<0:
            self.dx=self.dx*-1
        if hauteur_fenetre-self.taille<self.y or self.y<0:
            self.dy=self.dy*-1

    def horsjeux(self,raquette):
        if self.y>raquette.y:
            return "perdu"
           
class Raquette:
    def __init__(self,x=largeur_fenetre/2,y=hauteur_fenetre,largeurRaq=50,hauteurRaq=10):
        self.x=x
        self.y=y-hauteurRaq*4
        self.largeur=largeurRaq
        self.hauteur=hauteurRaq
    
    def tracer(self):
        if self.x<0:
            self.x+=4
        if self.x+self.largeur>=largeur_fenetre:
            self.x-=4
        tracerRaquette(fenetre, self)

    def collision(self,Balle):
        if Balle.y+Balle.taille>=self.y and Balle.x+Balle.taille>=self.x and Balle.x<=self.x+self.largeur:
            if Balle.y==self.y+self.hauteur or Balle.y+Balle.taille==self.y:
                Balle.dy=Balle.dy*-1
            else:
                Balle.dx=Balle.dx*-1

class Brique:
    def __init__(self,x=100,y=100,taille=20):
        self.x=x
        self.y=y
        self.taille=taille
        self.etat=True
        
    def tracer(self,Balle):
        if self.etat==True:
            self.collision(Balle)
            tracerBrique(fenetre,self)
        
    def collision(self,balle):
        if self.y+self.taille>=balle.y and self.y<=balle.y+balle.taille and self.x<=balle.x and self.x+self.taille>=balle.x:
            if balle.y==self.y+self.taille or balle.y+balle.taille==self.y:
                balle.dy=balle.dy*-1
                self.etat=False
            else:
                balle.dx=balle.dx*-1
                self.etat=False
    
class Grille:
    def __init__(self,taille,tailleb):
        x=100
        y=75
        self.grille=[]
        while taille!=0:
            if x>700:
                x=100
                y+=tailleb
            self.grille.append(Brique(x,y,tailleb))
            x+=tailleb+5
            taille-=1
    
    def jeux(self,Balle):
        for i in range(len(self.grille)):
            self.grille[i].tracer(Balle)






fenetre = ouvrir_fenetre(largeur_fenetre, hauteur_fenetre)
balle=Balle(largeur_fenetre//2,hauteur_fenetre//4)
raquette=Raquette()
deplacementx=0
grille=Grille(100,20)
while True:
    effacer(fenetre)
    balle.avancer()
    balle.tracer()
    raquette.tracer()
    raquette.collision(balle)
    grille.jeux(balle)
    if balle.horsjeux(raquette) == "perdu":
        print("perdu")
        pygame.quit()
        break
    actualiserAffichage(fenetre)
    raquette.x+=deplacementx
    sleep(vitesse)
    for event in pygame.event.get(): #détection evenement
        if event.type==MOUSEMOTION: #evenement sur la souris
            balle.x=event.pos[0] #balle placée sur le X de la souris
            balle.y=event.pos[1] #balle placée sur le Y de la souris
        if event.type==KEYDOWN:
            if event.key==K_LEFT:
                deplacementx=-4
            if event.key==K_RIGHT:
                deplacementx=4
        if event.type==KEYUP:
            deplacementx=0
