#!/usr/bin/env Python

"""Modules qui gère les balles et les missiles !

Usage:
======
    tout est dans le titre
"""

__authors__ = ("Ziggy")
__contact__ = ("")
__copyright__ = ""
__date__ = "18-10-2022"
__version__= "1.0"

from briques import *

#Balle
COULEUR_BALLE_DEFAUT = "lightslategray"
H_BALLE = 10
L_BALLE = H_BALLE
V0_BALLE_PAPA = DELTA_T/2 - 2      #10 pour delta t 20ms
V0_BALLE_JUJU = DELTA_T/5       #4 pour delta t 20ms

class Balle():
    def __init__(self,numero,x=0,y=0,angle=0,ancienne_ligne=0,ancienne_colonne=0,zut=False):
        """Constructeur de balle."""
        self.numero = numero
        self.x_balle = x
        self.y_balle = y
        self.angle_balle = angle
        self.ancienne_ligne = ancienne_ligne
        self.ancienne_colonne = ancienne_colonne
        self.zut = zut
        
    def __str__(self) :
        return (f"La Balle n°{self.numero} est en ({self.x_balle},{self.y_balle}) avec un angle de {self.angle_balle}")



class Projectile():
    def __init__(self,modele,puissance,tag='inconnu'):
        """Constructeur de missile."""
        self.tag = tag
        self.modele = modele
        self.puissance = puissance
        self.briques_impactes = []
        self.briques_impactes_sequence = [[],[],[],[],[],[]]
        if modele == 1 :
            self.longueur = 2
            self.hauteur = 2
            self.couleur = 'black'
            self.vitesse = 8
            self.briques_impactes.append([self.puissance,[0,0]])
        elif modele == 2 :
            self.longueur = 4
            self.hauteur = 8
            self.couleur = 'orange'
            self.couleur2 = 'black'
            self.vitesse = 6
            for i in range(self.puissance +1) :
                self.briques_impactes.append([self.puissance +1 - i,[0,-i]])
        elif modele == 3 :
            self.longueur = 8
            self.hauteur = 8
            self.couleur = 'red'
            self.vitesse = 4
            ligne = -4
            for li in MATRICE_3 :
                ligne += 1
                colonne = -4
                for modif in li :
                    colonne += 1
                    if self.puissance + modif > 0 :
                        self.briques_impactes.append([self.puissance + modif,[colonne,ligne]])
        elif modele == 4 :
            self.longueur = 12
            self.hauteur = 12
            self.couleur = 'deeppink'
            self.couleur2 = 'lightyellow'
            self.vitesse = 3
            ligne = -7
            for li in MATRICE_4 :
                ligne += 1
                colonne = -7
                for modif in li :
                    colonne += 1
                    if self.puissance + modif > 0 :
                        self.briques_impactes.append([self.puissance + modif,[colonne,ligne]])
            for truc in self.briques_impactes :
                la_colonne = truc[1][0] + 6
                la_ligne = truc[1][1] + 6
                la_sequence = MATRICE_4S[la_colonne][la_ligne]
                self.briques_impactes_sequence[la_sequence-1].append(truc)  
        
    def __str__(self) :
        return (f"Le Missile {self.tag} est de modèle : {self.modele}, Puissance = {self.puissance}")



L_3_1	=	[-2	,-2	,-2	,-2	,-2	,-2	,-2  ]
L_3_2	=	[-2	,-1	,-1	,-1	,-1	,-1	,-2  ]
L_3_3	=	[-2	,-1	,0	,0	,0	,-1	,-2  ]
L_3_4	=	[-2	,-1	,0	,0	,0	,-1	,-2  ]
L_3_5	=	[-2	,-1	,0	,0	,0	,-1	,-2  ]
L_3_6	=	[-2	,-1	,-1	,-1	,-1	,-1	,-2  ]
L_3_7	=	[-2	,-2	,-2	,-2	,-2	,-2	,-2  ]

MATRICE_3 = [L_3_1,	L_3_2,	L_3_3,	L_3_4,	L_3_5,	L_3_6,	L_3_7]

L_4_1	=	[-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2  ]
L_4_2	=	[-3	,-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2	,-3  ]
L_4_3	=	[-3	,-3	,-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2	,-3	,-3  ]
L_4_4	=	[-3	,-3	,-3	,-2	,-2	,-2	,-2	,-2	,-2	,-2	,-3	,-3	,-3  ]
L_4_5	=	[-3	,-3	,-3	,-2	,-1	,-1	,-1	,-1	,-1	,-2	,-3	,-3	,-3  ]
L_4_6	=	[-3	,-3	,-3	,-2	,-1	,0	,0	,0	,-1	,-2	,-3	,-3	,-3  ]
L_4_7	=	[-3	,-3	,-3	,-2	,-1	,0	,1	,0	,-1	,-2	,-3	,-3	,-3  ]
L_4_8	=	[-3	,-3	,-3	,-2	,-1	,0	,0	,0	,-1	,-2	,-3	,-3	,-3  ]
L_4_9	=	[-3	,-3	,-3	,-2	,-1	,-1	,-1	,-1	,-1	,-2	,-3	,-3	,-3  ]
L_4_10	=	[-3	,-3	,-3	,-2	,-2	,-2	,-2	,-2	,-2	,-2	,-3	,-3	,-3  ]
L_4_11	=	[-3	,-3	,-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2	,-3	,-3  ]
L_4_12	=	[-3	,-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2	,-3  ]
L_4_13	=	[-2	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-3	,-2  ]

MATRICE_4 = [L_4_1,	L_4_2,	L_4_3,	L_4_4,	L_4_5,	L_4_6,	L_4_7,	L_4_8,	L_4_9,	L_4_10,	L_4_11,	L_4_12,	L_4_13]

L_4S_1 	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]
L_4S_2 	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]
L_4S_3 	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]
L_4S_4 	=	[5	,5	,5	,4	,4	,4	,4	,4	,4	,4	,5	,5	,5  ]
L_4S_5 	=	[5	,5	,5	,4	,3	,3	,3	,3	,3	,4	,5	,5	,5  ]
L_4S_6  =	[5	,5	,5	,4	,3	,2	,2	,2	,3	,4	,5	,5	,5  ]
L_4S_7 	=	[5	,5	,5	,4	,3	,2	,1	,2	,3	,4	,5	,5	,5  ]
L_4S_8 	=	[5	,5	,5	,4	,3	,2	,2	,2	,3	,4	,5	,5	,5  ]
L_4S_9  =	[5	,5	,5	,4	,3	,3	,3	,3	,3	,4	,5	,5	,5  ]
L_4S_10	=	[5	,5	,5	,4	,4	,4	,4	,4	,4	,4	,5	,5	,5  ]
L_4S_11	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]
L_4S_12	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]
L_4S_13	=	[5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5	,5  ]

MATRICE_4S = [L_4S_1,	L_4S_2,	L_4S_3,	L_4S_4,	L_4S_5,	L_4S_6,	L_4S_7,	L_4S_8,	L_4S_9,	L_4S_10,	L_4S_11,	L_4S_12,	L_4S_13]





