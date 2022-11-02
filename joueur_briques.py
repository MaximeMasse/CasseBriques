#!/usr/bin/env Python

"""Modules joueur !

Usage:
======
  
"""

__authors__ = ("Ziggy")
__contact__ = ("")
__copyright__ = ""
__date__ = "09-10-2022"
__version__= "1.0"

import math

from briques import *


    #Vie
X_VIE = 20
Y_VIE = H_JEU - 15
VIE_PAPA = 5
VIE_JUJU = 100
    #Attributs
Y_ATTRIBUTS = H_JEU + 50


#Correspondance xp niveau
XP_LEVEL = [0,	10,	15,	20,	25,	30,	35,	40,	45,	50,	60,	70,	80,	90,	100,	110,	120,	130,	140,	150,	160,	170,	180,	190,	200,	225,	250,	275,	300,	325,	350,	375,	400,	425,	450,	475,	500,	550,	600,	650,	700,	750,	800,	850,	900,	950,	1000,	1100,	1200,	1300,	1400]



class Joueur():
    def __init__(self, liste_prof):
        """Constructeur de Joueur."""
        # Nom
        self.nom = liste_prof[0]
        #données
        self.niveau = int(liste_prof[1])
        self.xp = int(liste_prof[2])
        if self.niveau < 50 :
            self.xp_avant_lvlup = XP_LEVEL[self.niveau] - self.xp
        else : self.xp_avant_lvlup = 0
        self.record = liste_prof[3]
        self.level = liste_prof[4]
        self.attributs = liste_prof[5]
        self.golds = int(liste_prof[6])
        self.points_upgrades = int(liste_prof[7])
        self.missile_M = int(self.attributs[7].split('-')[0])
        self.missile_P = int(self.attributs[7].split('-')[1])
        self.missile_Q = int(self.attributs[7].split('-')[2])
        self.live_up = int(self.attributs[5].split('-')[0])
        self.pplus_up = int(self.attributs[5].split('-')[1])
        self.sb_up = int(self.attributs[6].split('-')[0])
        self.mb_up = int(self.attributs[6].split('-')[1])
        self.dico_gold = {"live_up": self.live_up, "pplus" : self.pplus_up, "super_bonus" : self.sb_up, "multiballe" : self.mb_up}

    def modele_up(self):
        self.missile_M +=1
        self.missile_P = DICO_MISSILES[self.missile_M][0][0][0]
        self.missile_Q = DICO_MISSILES[self.missile_M][1][0][0]
        self.attributs[7] = f"{self.missile_M}-{self.missile_P}-{self.missile_Q}"
        
    def modele_down(self,ancienP,ancienQ):
        self.missile_M -=1
        self.missile_P = ancienP
        self.missile_Q = ancienQ
        self.attributs[7] = f"{self.missile_M}-{self.missile_P}-{self.missile_Q}"
        
    def maj_missile_P(self,nv):
        self.missile_P = nv
        self.attributs[7] = f"{self.missile_M}-{self.missile_P}-{self.missile_Q}"
        
    def maj_missile_Q(self,nv):
        self.missile_Q = nv
        self.attributs[7] = f"{self.missile_M}-{self.missile_P}-{self.missile_Q}"
    
    def maj_xp(self,nb_xp):
        nouveau_xp = self.xp + nb_xp
        xp_trop_grand = True
        while xp_trop_grand :
            if nouveau_xp >= XP_LEVEL[self.niveau] :
                nouveau_xp -= XP_LEVEL[self.niveau]
                self.niveau += 1
                self.points_upgrades += 1
            else :
                self.xp = nouveau_xp
                xp_trop_grand = False
                self.xp_avant_lvlup = XP_LEVEL[self.niveau] - self.xp
            
    def __str__(self) :
        return (f"Joueur {self.nom}, nv. {self.niveau}, xp = {self.xp}. {self.golds} golds et {self.points_upgrades} pts d'upgrades en stock\nUpgrades : {self.attributs}\nMissiles : M : {self.missile_M}, P : {self.missile_P}, Q : {self.missile_Q}")
        
    def palier_nv_cout(self,upgrade,valeur_actuelle,modele='None'):
        p=-1
        if modele == 'None' :
            le_dico = DICO_UPGRADES[upgrade]
        elif upgrade ==  "Missiles_P" :
            le_dico = DICO_MISSILES[modele][0]
        elif upgrade ==  "Missiles_Q" :
            le_dico = DICO_MISSILES[modele][1]
        else :
            print('pnv bug, modèle de missile requis')
        for palier in le_dico :
            if le_dico[palier][0] == valeur_actuelle :
                p = palier
                nv = le_dico[palier+1][0]
                cout = le_dico[palier+1][1]
                lvl_requis = le_dico[palier+1][2]
                if self.niveau < lvl_requis :
                    peut_up = False
                else: peut_up = True
        if p == -1 :
            print(f"pnv bug, valeur {valeur_actuelle} non trouvée")
        else:
            return(p,nv,cout,peut_up,lvl_requis)
            
    def palier_nv_cout_retour(self,upgrade,valeur_actuelle,modele='None'):
        p=-1
        if modele == 'None' :
            le_dico = DICO_UPGRADES[upgrade]
        elif upgrade ==  "Missiles_P" :
            le_dico = DICO_MISSILES[modele][0]
        elif upgrade ==  "Missiles_Q" :
            le_dico = DICO_MISSILES[modele][1]
        else :
            print('pnv_retour bug, modèle de missile requis')
        for palier in le_dico :
            if le_dico[palier][0] == valeur_actuelle :
                p = palier
                nv = le_dico[palier-1][0]
                cout = le_dico[palier][1]
        if p == -1 :
            print(f"pnv_retour bug, valeur {valeur_actuelle} non trouvée")
        else:
            return(p,nv,cout)




#dico d'upgrades
NIVEAU_UNLOCKS = {"L_raq":2 , "B_raq":3, "Maniabilité_raq":4, "Missiles":10, "Vies":5, "P_balle":7 } 
DICO_L_raq = {0:(20,0,2), 1:(25,1,2), 2:(30,1,2), 3:(35,1,5), 4:(40,1,8), 5:(50,2,10), 6:(60,2,15), 7:("max","max",50)}            #total = 8
DICO_B_raq = {0:(1,0,3), 1:(5,1,3), 2:(10,1,5), 3:(15,1,8), 4:(20,1,10), 5:(25,1,15), 6:(30,1,20), 7:("max","max",50)}              #total = 6 total_c = 14    
DICO_mania_raq = {0:('Inexistante',0,4), 1:('Pas top',2,4), 2:('Acceptable',2,10), 3:('Premium',3,25), 4:("max","max",50)}   #total = 7 total_c = 21   
DICO_Vies = {0:(2,0,5), 1:(3,1,5), 2:(4,1,5), 3:(5,1,5), 4:(6,1,10), 5:(7,1,10), 6:(8,1,10), 7:(9,1,20), 8:(10,1,25), 9:("max","max",50)} #total = 8 total_c = 29              
DICO_P_balle = {0:(1,0,7), 1:(2,2,7), 2:(3,2,15), 3:(4,2,25), 4:(5,2,40), 5:("max","max",50)}                                   #total = 8 total_c = 37  
DICO_Missiles_mod = {0:(0,0,10), 1:(1,2,10), 2:(2,3,20), 3:(3,4,30), 4:(4,5,40), 5:("max","max",50)}                              #total = 14total_c = 51  
DICO_M1_P = {0:(2,0,0), 1:(3,1,0), 2:(4,1,0), 3:("max","max",50)}                                                        #total = 2 total_c = 53  
DICO_M1_Q = {0:(10,0,0), 1:(15,1,0), 2:(20,1,0), 3:("max","max",50)}                                                        #total = 2 total_c = 55          
DICO_M2_P = {0:(1,0,0), 1:(2,1,0), 2:(3,1,0), 3:("max","max",50)}                                                        #total = 2 total_c = 57  
DICO_M2_Q = {0:(10,0,0), 1:(15,1,0), 2:(20,1,0), 3:("max","max",50)}                                                   #total = 2 total_c = 59              
DICO_M3_P = {0:(1,0,0), 1:(2,2,0), 2:(3,2,0), 3:("max","max",50)}                                                        #total = 4 total_c = 63  
DICO_M3_Q = {0:(10,0,0), 1:(15,1,0), 2:(20,1,0), 3:("max","max",50)}                                                       #total = 4 total_c = 67  
DICO_M4_P = {0:(1,0,0), 1:(2,3,0), 2:(3,3,0), 3:("max","max",50)}                                                        #total = 6 total_c = 73  
DICO_M4_Q = {0:(10,0,0), 1:(15,1,0), 2:(20,1,0), 3:("max","max",50)}                                                      #total = 6 total_c = 79    
DICO_MISSILES = {0:({0:(0,0,0),1:(1,0,0)},{0:(0,0,0),1:(1,0,0)}), 1:(DICO_M1_P,DICO_M1_Q) ,2:(DICO_M2_P,DICO_M2_Q) , 3:(DICO_M3_P,DICO_M3_Q) , 4:(DICO_M4_P,DICO_M4_Q)}  

DICO_UPGRADES = {"L_raq":DICO_L_raq, "B_raq":DICO_B_raq, "Maniabilité_raq":DICO_mania_raq, "Vies":DICO_Vies, "P_balle":DICO_P_balle, "Missiles_M":DICO_Missiles_mod ,"Missiles_P":(DICO_M1_P,DICO_M2_P,DICO_M3_P,DICO_M4_P),"Missiles_Q":(DICO_M1_Q,DICO_M2_Q,DICO_M3_Q,DICO_M4_Q)}

        