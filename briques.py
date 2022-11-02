#!/usr/bin/env Python

"""Modules briques !

Usage:
======
    Contient les données des briques, les patterns et renvoie des objet briques et matrices de briques
    Contient la classe Joueur de l'appli casse-briques
    Contient aussi les données sur les power-up
"""

__authors__ = ("Ziggy")
__contact__ = ("")
__copyright__ = ""
__date__ = "09-10-2022"
__version__= "1.0"

import math

    #dimensions brique
H_BRIQUE = 23
L_BRIQUE = 23
INTER_BRIQUE = int((25 - L_BRIQUE)/2)
NB_COL = 25
NB_LIGNE = 25


#données gameplay
    #fenêtre de jeu
H_JEU = 700
L_JEU = NB_COL * (L_BRIQUE + 2 * INTER_BRIQUE)
H_DESSOUS = 300
H_MENU = H_JEU+ H_DESSOUS
L_MENU = 300
L_CADRE_JOUEUR = 150
DECALAGE = 4
DELTA_T = 30 #en millisecondes, le bon chiffre est 30
DELTA_T_SEC = DELTA_T/1000

    #Raquette
COULEUR_RAQUETTE = "midnightblue"
COULEUR_BORDS_RAQUETTE = "darkslategrey" 
H_RAQUETTE = 10
ANGLE_BORD = math.pi/4
L_RAQUETTE_JUJU = 150
Y_RAQUETTE = 650
VITESSE_RAQUETTE_SOURIS = 5   #20 en clavier 5 en souris
VITESSE_RAQUETTE_CLAVIER = 20   #20 en clavier 5 en souris
DEADZONE_SOURIS = 20



class Brique():
    def __init__(self,position,couleur,CORRESPONDANCE):
        """Constructeur de Brique."""
        # Position colonne et ligne
        self.colonne, self.ligne = position[0], position[1]
        # Couleur
        self.couleur_brique = couleur
        #détermination des valeurs en fonction de la couleur
        for elem in CORRESPONDANCE :
            if elem[1] == couleur :
                self.resistance = elem[2]
                self.v_point = elem[3]
                self.v_xp = elem[4]
                self.powerup = elem[5]
                self.v_golds = elem[6]
                
    def __str__(self) :
        return (f"La brique : {self.colonne} : {self.ligne} de résistance {self.resistance} est {self.couleur_brique}.\nElle vaut {self.v_point} point(s), {self.v_xp} xp et {self.v_golds} golds.\nBonus : {self.powerup}.")




#Pattern EMOJI

LISTE_INDICES_EMOJI = [     2      ,   1       ]     
LISTE_COULEUR_EMOJI = [  "black"   ,  "orange"  ]
LISTE_RESISTS_EMOJI = [     1      ,   0       ]
LISTE_POINTSS_EMOJI = [     5      ,   2       ]
LISTE_XPPPPPP_EMOJI = [     8      ,   0       ]
LISTE_POWERUP_EMOJI = [     0      ,   0       ]
LISTE_GOLDDDD_EMOJI = [     0      ,   0       ]

LIGNE1  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE2  = [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE3  = [0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0]
LIGNE4  = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
LIGNE5  = [0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0]
LIGNE6  = [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0]
LIGNE7  = [0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0]
LIGNE8  = [0,0,0,0,0,0,0,0,1,0,2,0,1,0,2,0,1,0,0,0,0,0,0,0,0]
LIGNE9  = [0,0,0,0,0,0,0,0,1,0,2,0,1,0,2,0,1,0,0,0,0,0,0,0,0]
LIGNE10 = [0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0]
LIGNE11 = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
LIGNE12 = [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0]
LIGNE13 = [0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,1,1,1,1,0,0,0,0,0,0]
LIGNE14 = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
LIGNE15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE16 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE17 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE18 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE19 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE21 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE22 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_EMOJI = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_EMOJI =[]    
for i in range(len(LISTE_COULEUR_EMOJI)):
    ensemble = [LISTE_INDICES_EMOJI[i],LISTE_COULEUR_EMOJI[i],LISTE_RESISTS_EMOJI[i],LISTE_POINTSS_EMOJI[i],LISTE_XPPPPPP_EMOJI[i],LISTE_POWERUP_EMOJI[i],LISTE_GOLDDDD_EMOJI[i]]
    CORRESPONDANCE_EMOJI += [ensemble]
 

 
#Pattern Rainbow

LISTE_INDICES_RAINBOW = [     7      ,       6     ,        5    ,      4      ,    3         ,      2      ,   1       ]     
LISTE_COULEUR_RAINBOW = ["red"       , "orange"    ,"yellow"     ,"greenyellow", "deepskyblue", "indigo"    ,"deeppink" ]
LISTE_RESISTS_RAINBOW = [      4     ,       3     ,        2    ,      2      ,    1         ,      1      ,   0       ]
LISTE_POINTSS_RAINBOW = [      100   ,       50    ,        30   ,      20     ,    10        ,      5      ,   2       ]
LISTE_XPPPPPP_RAINBOW = [      0     ,       1     ,        2    ,      3      ,    5         ,      8      ,   0       ]
LISTE_POWERUP_RAINBOW = [       0    ,        0    ,        0    ,      0      ,    0         ,      0      ,   0       ]
LISTE_GOLDDDD_RAINBOW = [       0    ,        0    ,        0    ,      0      ,    0         ,      0      ,   0       ]

#Pattern   1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
LIGNE1  = [7,0,7,7,7,0,7,7,7,7,7,7,0,7,7,7,7,7,7,0,7,7,7,0,7]
LIGNE2  = [7,7,0,7,7,7,0,7,7,7,7,0,7,0,7,7,7,7,0,7,7,7,0,7,7]
LIGNE3  = [6,6,6,0,6,6,6,0,6,6,0,6,6,6,0,6,6,0,6,6,6,0,6,6,6]
LIGNE4  = [0,6,6,6,0,6,6,6,0,0,6,6,6,6,6,0,0,6,6,6,0,6,6,6,0]
LIGNE5  = [5,0,5,5,5,0,5,5,0,0,5,5,5,5,5,0,0,5,5,0,5,5,5,0,5]
LIGNE6  = [5,5,0,5,5,5,0,0,5,5,0,5,5,5,0,5,5,0,0,5,5,5,0,5,5]
LIGNE7  = [0,4,4,0,4,4,0,0,4,4,4,0,4,0,4,4,4,0,0,4,4,0,4,4,0]
LIGNE8  = [4,0,4,4,0,0,4,4,0,4,4,4,0,4,4,4,0,4,4,0,0,4,4,0,4]
LIGNE9  = [3,3,0,3,0,0,3,3,3,0,3,3,3,3,3,0,3,3,3,0,0,3,0,3,3]
LIGNE10 = [3,3,3,0,3,3,0,3,3,3,0,3,3,3,0,3,3,3,0,3,3,0,3,3,3]
LIGNE11 = [2,2,0,2,0,2,2,0,2,2,2,0,2,0,2,2,2,0,2,2,0,2,0,2,2]
LIGNE12 = [2,0,2,2,2,0,2,2,0,2,2,2,0,2,2,2,0,2,2,0,2,2,2,0,2]
LIGNE13 = [0,1,1,1,1,1,0,1,1,0,1,0,1,0,1,0,1,1,0,1,1,1,1,1,0]
LIGNE14 = [0,0,1,1,0,1,1,0,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,0,0]
LIGNE15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE16 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE17 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE18 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE19 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE21 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE22 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_RAINBOW = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_RAINBOW =[]    
for i in range(len(LISTE_COULEUR_RAINBOW)):
    ensemble = [LISTE_INDICES_RAINBOW[i],LISTE_COULEUR_RAINBOW[i],LISTE_RESISTS_RAINBOW[i],LISTE_POINTSS_RAINBOW[i],LISTE_XPPPPPP_RAINBOW[i],LISTE_POWERUP_RAINBOW[i],LISTE_GOLDDDD_RAINBOW[i]]
    CORRESPONDANCE_RAINBOW += [ensemble]
    


#Pattern Four Juju

LISTE_INDICES_FOUR = [     7      ,       6     ,        5    ,      4      ,    3         ,      2      ,   1       ,      8      ,      9     ,      10    ]     
LISTE_COULEUR_FOUR = ["darkorange", "purple"    ,"deepskyblue","lawngreen"  , "yellow"     , "red"       ,"brown"    , "black"     ,"deeppink"  ,"firebrick1"]
LISTE_RESISTS_FOUR = [      4     ,       3     ,        2    ,      2      ,    1         ,      1      ,   0       , 0           ,0           ,      0     ]
LISTE_POINTSS_FOUR = [      100   ,       50    ,        30   ,      20     ,    10        ,      5      ,   2       , 5           ,      5     ,      9     ]
LISTE_XPPPPPP_FOUR = [      0     ,       1     ,        2    ,      3      ,    5         ,      8      ,   0       , 5           ,    5       ,      9     ]
LISTE_POWERUP_FOUR = [       0    ,        0    ,        0    ,      0      ,    0         ,      0      ,   0       , 0           ,0           ,      0     ]
LISTE_GOLDDDD_FOUR = [       0    ,        0    ,        0    ,      0      ,    0         ,      0      ,   0       , 0           ,0           ,      0     ]

#Pattern   1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
LIGNE1  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE2  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE3  = [0,0,0,0,0,0,0,2,2,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0]
LIGNE4  = [0,0,0,0,0,0,2,0,0,2,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0]
LIGNE5  = [0,0,0,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0]
LIGNE6  = [0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0]
LIGNE7  = [0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE8  = [0,0,0,0,0,0,0,0,0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE9  = [0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE10 = [8,0,0,8,0,0,0,0,10,10,10,10,10,10,10,10,10,10,0,0,0,8,0,0,8]
LIGNE11 = [0,8,0,8,0,0,0,0,3,2,2,2,3,3,2,2,2,3,0,0,0,8,0,8,0]
LIGNE12 = [0,0,1,1,1,0,0,0,4,2,8,2,4,4,2,8,2,4,0,0,1,1,1,0,0]
LIGNE13 = [8,8,1,1,1,1,1,1,9,2,2,2,9,9,2,2,2,9,1,1,1,1,1,8,8]
LIGNE14 = [0,0,1,1,1,0,0,0,5,5,5,5,5,5,5,5,5,5,0,0,1,1,1,0,0]
LIGNE15 = [0,8,0,8,0,0,0,0,6,6,6,8,8,8,8,6,6,6,0,0,0,8,0,8,0]
LIGNE16 = [8,0,0,8,0,0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,8,0,0,8]
LIGNE17 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE18 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE19 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE21 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE22 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_FOUR = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_FOUR =[]    
for i in range(len(LISTE_COULEUR_FOUR)):
    ensemble = [LISTE_INDICES_FOUR[i],LISTE_COULEUR_FOUR[i],LISTE_RESISTS_FOUR[i],LISTE_POINTSS_FOUR[i],LISTE_XPPPPPP_FOUR[i],LISTE_POWERUP_FOUR[i],LISTE_GOLDDDD_FOUR[i]]
    CORRESPONDANCE_FOUR += [ensemble]

#Pattern TEST

LISTE_INDICES_TEST = [     1           ,   2             ,   3             ,   4             ,   5             ,   6             ,   7             ,   8             ,   9             ]      
LISTE_COULEUR_TEST = [ "#ffff00"       ,"#ff0000"        ,"#F0B000"        ,"deepskyblue2"   ,"deepskyblue4"   ,"orange"         ,"lightgreen"     ,"white"          ,"grey"           ]
LISTE_RESISTS_TEST = [     0           ,   1             ,   2             ,   5             ,   0             ,   0             ,   20            ,   0             ,   0             ] 
LISTE_POINTSS_TEST = [     5           ,   50            ,   50            ,   50            ,   50            ,   50            ,   50            ,   6             ,   7             ] 
LISTE_XPPPPPP_TEST = [     1           ,   2             ,   0             ,   1             ,   3             ,   1             ,   1             ,   1             ,   1             ] 
LISTE_POWERUP_TEST = [     0           ,   0             ,      0          ,    0            ,  "multiballe"   ,   0             ,      0          ,    0            ,   0             ] 
LISTE_GOLDDDD_TEST = [      1          ,   0             ,      0          ,    0            ,   0             ,   0             ,   0             ,     0           ,   0             ] 

#Pattern   1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
LIGNE1  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE2  = [0,0,0,0,0,0,0,5,0,0,0,0,0,5,0,0,0,0,0,0,0,8,8,8,0]
LIGNE3  = [0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE4  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE5  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE6  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE7  = [3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,5,0,0,0]
LIGNE8  = [3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,5,0,0,0,0,0,0,0,0,0]
LIGNE9  = [3,3,3,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE10 = [2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE11 = [2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE12 = [2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,7,7,0,0,0,0]
LIGNE13 = [2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE14 = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE15 = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,5,5,0,0,0,0,0,0,0]
LIGNE16 = [1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,7,0,0]
LIGNE17 = [4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE18 = [4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE19 = [4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE20 = [4,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE21 = [4,4,4,4,4,4,4,2,2,2,2,2,2,0,0,0,5,0,0,0,0,0,0,0,0]
LIGNE22 = [0,6,0,6,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_TEST = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_TEST =[]    
for i in range(len(LISTE_COULEUR_TEST)):
    ensemble = [LISTE_INDICES_TEST[i],LISTE_COULEUR_TEST[i],LISTE_RESISTS_TEST[i],LISTE_POINTSS_TEST[i],LISTE_XPPPPPP_TEST[i],LISTE_POWERUP_TEST[i],LISTE_GOLDDDD_TEST[i]]
    CORRESPONDANCE_TEST += [ensemble]
 

#Pattern Vide

LISTE_INDICES_VIDE = [     1           ,   2             ,   3             ,   4             ,   5             ,   6             ,   7             ]     
LISTE_COULEUR_VIDE = [  "gold"         ,"lightcyan2"     ,"skyblue1"       ,"deepskyblue2"   ,"deepskyblue4"   ,"orange"         ,"lightgreen"     ]
LISTE_RESISTS_VIDE = [     0           ,   0             ,   1             ,   2             ,   3             ,   0             ,   0             ]
LISTE_POINTSS_VIDE = [     5           ,   5             ,   0             ,   1             ,   3             ,   4             ,   5             ]
LISTE_XPPPPPP_VIDE = [     8           ,   2             ,   0             ,   1             ,   3             ,   4             ,   5             ]
LISTE_POWERUP_VIDE = ["super_bonus"    ,  "multiballe"   ,"multiplicateur2",0                ,0                ,0                ,   0             ]
LISTE_GOLDDDD_VIDE = [     0           ,   0             ,   0             ,0                ,0                ,0                ,   0             ]

#Pattern   1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
LIGNE1  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE2  = [0,0,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE3  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE4  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE5  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE6  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE7  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE8  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE9  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE10 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE11 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE12 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE13 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE14 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE15 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE16 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE17 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE18 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE19 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE20 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE21 = [0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE22 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_VIDE = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_VIDE =[]    
for i in range(len(LISTE_COULEUR_VIDE)):
    ensemble = [LISTE_INDICES_VIDE[i],LISTE_COULEUR_VIDE[i],LISTE_RESISTS_VIDE[i],LISTE_POINTSS_VIDE[i],LISTE_XPPPPPP_VIDE[i],LISTE_POWERUP_VIDE[i],LISTE_GOLDDDD_VIDE[i]]
    CORRESPONDANCE_VIDE += [ensemble]



 
#Pattern diagonales

LISTE_INDICES_DIAG = [     1           ,   2             ,   3             ,   4             ,   5             ,   6             ,   7             ]     
LISTE_COULEUR_DIAG = [  "gold"         ,"lightcyan2"     ,"skyblue1"       ,"deepskyblue2"   ,"deepskyblue4"   ,"orange"         ,"lightgreen"     ]
LISTE_RESISTS_DIAG = [     0           ,   1             ,   2             ,   2             ,   3             ,   0             ,   0             ]
LISTE_POINTSS_DIAG = [     5           ,   5             ,   0             ,   1             ,   3             ,   4             ,   5             ]
LISTE_XPPPPPP_DIAG = [     8           ,   2             ,   0             ,   1             ,   3             ,   4             ,   5             ]
LISTE_POWERUP_DIAG = [     0           ,   0             ,   0             ,0                ,0                ,0                ,   0             ]
LISTE_GOLDDDD_DIAG = [     0           ,   0             ,   0             ,0                ,0                ,0                ,   0             ]

#Pattern   1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
LIGNE1  = [0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0]
LIGNE2  = [0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0]
LIGNE3  = [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]
LIGNE4  = [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0]
LIGNE5  = [0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]
LIGNE6  = [0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0]
LIGNE7  = [0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,0,0,0,0]
LIGNE8  = [0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,0,0,0,1]
LIGNE9  = [0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,1,3]
LIGNE10 = [0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,1,0,3]
LIGNE11 = [0,0,0,0,0,0,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,1,0,0,3]
LIGNE12 = [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,0,0,0,0,1,3,3,3,3]
LIGNE13 = [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,1,3,3,3,3,3]
LIGNE14 = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,1,3,3,3,3,3,3]
LIGNE15 = [0,0,0,0,0,3,2,1,0,0,0,0,0,0,0,0,0,1,2,3,3,3,3,3,3]
LIGNE16 = [0,0,0,0,3,2,1,0,0,0,0,0,0,0,0,0,1,0,0,2,3,3,3,3,3]
LIGNE17 = [0,0,0,3,2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,2,3,3,3,3]
LIGNE18 = [0,0,3,2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,3,3,3]
LIGNE19 = [0,3,2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,3,3]
LIGNE20 = [3,2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,2,3]
LIGNE21 = [2,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2]
LIGNE22 = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE23 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE24 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
LIGNE25 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
MATRICE_DIAG = [LIGNE1,LIGNE2,LIGNE3,LIGNE4,LIGNE5,LIGNE6,LIGNE7,LIGNE8,LIGNE9,LIGNE10,LIGNE11,LIGNE12,LIGNE13,LIGNE14,LIGNE15,LIGNE16,LIGNE17,LIGNE18,LIGNE19,LIGNE20,LIGNE21,LIGNE22,LIGNE23,LIGNE24,LIGNE25]

CORRESPONDANCE_DIAG =[]    
for i in range(len(LISTE_COULEUR_DIAG)):
    ensemble = [LISTE_INDICES_DIAG[i],LISTE_COULEUR_DIAG[i],LISTE_RESISTS_DIAG[i],LISTE_POINTSS_DIAG[i],LISTE_XPPPPPP_DIAG[i],LISTE_POWERUP_DIAG[i],LISTE_GOLDDDD_DIAG[i]]
    CORRESPONDANCE_DIAG += [ensemble] 



#LVL0
LVL0_1	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_2	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_3	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_4	=	[0,	1,	1,	1,	0,	1,	1,	1,	1,	1,	1,	0,	0,	0,	1,	1,	1,	1,	1,	1,	0,	1,	1,	1,	0  ]
LVL0_5	=	[0,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	0  ]
LVL0_6	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_7	=	[0,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	0,	0,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	0  ]
LVL0_8	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_9	=	[0,	4,	4,	4,	4,	4,	0,	0,	0,	4,	4,	4,	4,	4,	4,	4,	0,	0,	0,	4,	4,	4,	4,	4,	0  ]
LVL0_10	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_11	=	[0,	5,	5,	5,	5,	0,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	0,	5,	5,	5,	5,	0  ]
LVL0_12	=	[0,	5,	5,	5,	5,	5,	0,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	5,	0,	5,	5,	5,	5,	5,	0  ]
LVL0_13	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_14	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_15	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_16	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_17	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_18	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_19	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_20	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_21	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_22	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_23	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_24	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL0_25	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
MATRICE_LVL0	=	[LVL0_1,	LVL0_2,	LVL0_3,	LVL0_4,	LVL0_5,	LVL0_6,	LVL0_7,	LVL0_8,	LVL0_9,	LVL0_10,	LVL0_11,	LVL0_12,	LVL0_13,	LVL0_14,	LVL0_15,	LVL0_16,	LVL0_17,	LVL0_18,	LVL0_19,	LVL0_20,	LVL0_21,	LVL0_22,	LVL0_23,	LVL0_24,	LVL0_25  ]
																										
LISTE_INDICES_LVL0	=	[1,	2,	3,	4,	5  ]																				
LISTE_COULEUR_LVL0	=	["#808080",	"#FF0000",	"#FFC000",	"#92D050",	"#FFFF00"  ]																				
LISTE_RESISTS_LVL0	=	[2,	0,	1,	0,	0  ]																				
LISTE_POINTSS_LVL0	=	[0,	5,	3,	2,	1  ]																				
LISTE_XPPPPPP_LVL0	=	[1,	2,	1,	1,	1  ]																				
LISTE_POWERUP_LVL0	=	[0,	0,	0,	0,	0  ]																				
LISTE_GOLDDDD_LVL0	=	[1,	2,	1,	1,	1  ]																				
																		


CORRESPONDANCE_LVL0 =[]    
for i in range(len(LISTE_COULEUR_LVL0)):
    ensemble = [LISTE_INDICES_LVL0[i],LISTE_COULEUR_LVL0[i],LISTE_RESISTS_LVL0[i],LISTE_POINTSS_LVL0[i],LISTE_XPPPPPP_LVL0[i],LISTE_POWERUP_LVL0[i],LISTE_GOLDDDD_LVL0[i]]
    CORRESPONDANCE_LVL0 += [ensemble] 
    

#LVL1

LVL1_1	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_2	=	[0,	0,	5,	5,	5,	5,	5,	5,	0,	5,	0,	0,	0,	0,	0,	5,	0,	5,	5,	5,	5,	5,	5,	0,	0  ]
LVL1_3	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	5,	0,	0,	0,	5,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_4	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	5,	0,	5,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_5	=	[0,	0,	3,	3,	3,	0,	0,	0,	3,	3,	3,	3,	3,	3,	3,	3,	3,	0,	0,	0,	3,	3,	3,	0,	0  ]
LVL1_6	=	[0,	0,	3,	3,	3,	3,	3,	3,	3,	0,	3,	3,	0,	3,	3,	0,	3,	3,	3,	3,	3,	3,	3,	0,	0  ]
LVL1_7	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_8	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_9	=	[6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6,	6  ]
LVL1_10	=	[0,	0,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	0,	0  ]
LVL1_11	=	[0,	0,	2,	0,	0,	0,	0,	0,	0,	0,	4,	3,	2,	3,	4,	0,	0,	0,	0,	0,	0,	0,	2,	0,	0  ]
LVL1_12	=	[0,	0,	2,	0,	0,	1,	0,	0,	0,	4,	3,	0,	2,	0,	3,	4,	0,	0,	0,	1,	0,	0,	2,	0,	0  ]
LVL1_13	=	[0,	0,	2,	0,	0,	0,	0,	0,	4,	3,	0,	0,	2,	0,	0,	3,	4,	0,	0,	0,	0,	0,	2,	0,	0  ]
LVL1_14	=	[0,	0,	2,	0,	0,	0,	0,	4,	3,	0,	0,	0,	2,	0,	0,	0,	3,	4,	0,	0,	0,	0,	2,	0,	0  ]
LVL1_15	=	[0,	0,	2,	0,	0,	0,	4,	3,	0,	0,	0,	0,	2,	0,	0,	0,	0,	3,	4,	0,	0,	0,	2,	0,	0  ]
LVL1_16	=	[0,	0,	7,	7,	7,	7,	7,	7,	7,	7,	0,	0,	2,	0,	0,	7,	7,	7,	7,	7,	7,	7,	7,	0,	0  ]
LVL1_17	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_18	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_19	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_20	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_21	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_22	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_23	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_24	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL1_25	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
MATRICE_LVL1	=	[LVL1_1,	LVL1_2,	LVL1_3,	LVL1_4,	LVL1_5,	LVL1_6,	LVL1_7,	LVL1_8,	LVL1_9,	LVL1_10,	LVL1_11,	LVL1_12,	LVL1_13,	LVL1_14,	LVL1_15,	LVL1_16,	LVL1_17,	LVL1_18,	LVL1_19,	LVL1_20,	LVL1_21,	LVL1_22,	LVL1_23,	LVL1_24,	LVL1_25  ]
																										
LISTE_INDICES_LVL1	=	[1,	2,	3,	4,	5,	6,	7  ]																		
LISTE_COULEUR_LVL1	=	["#FFFF00",	"#8DB4E2",	"#9933FF",	"#F79646",	"#FF0000",	"#808080",	"#BFBFBF"  ]																		
LISTE_RESISTS_LVL1	=	[0,	1,	0,	1,	1,	2,	1  ]																		
LISTE_POINTSS_LVL1	=	[5,	1,	2,	1,	3,	1,	1  ]																		
LISTE_XPPPPPP_LVL1	=	[1,	1,	1,	1,	5,	0,	0  ]																		
LISTE_POWERUP_LVL1	=	["pplus",	0,	0,	0,	0,	0,	0  ]																		
LISTE_GOLDDDD_LVL1	=	[5,	1,	1,	1,	2,	0,	0  ]																		
																	


CORRESPONDANCE_LVL1 =[]    
for i in range(len(LISTE_COULEUR_LVL1)):
    ensemble = [LISTE_INDICES_LVL1[i],LISTE_COULEUR_LVL1[i],LISTE_RESISTS_LVL1[i],LISTE_POINTSS_LVL1[i],LISTE_XPPPPPP_LVL1[i],LISTE_POWERUP_LVL1[i],LISTE_GOLDDDD_LVL1[i]]
    CORRESPONDANCE_LVL1 += [ensemble] 

LVL2_1	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_2	=	[0,	0,	5,	0,	0,	0,	5,	0,	0,	0,	0,	0,	1,	0,	0,	6,	0,	0,	0,	6,	0,	0,	6,	0,	0  ]
LVL2_3	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_4	=	[0,	0,	0,	5,	0,	0,	0,	0,	5,	0,	0,	0,	1,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_5	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_6	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_7	=	[0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1  ]
LVL2_8	=	[0,	0,	0,	0,	7,	7,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4,	4  ]
LVL2_9	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_10	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_11	=	[1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0  ]
LVL2_12	=	[3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	3,	7,	7,	0,	0,	0,	0  ]
LVL2_13	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_14	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_15	=	[0,	0,	0,	0,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1  ]
LVL2_16	=	[0,	0,	0,	0,	7,	7,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2,	2  ]
LVL2_17	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_18	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_19	=	[1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0,	0,	0,	0  ]
LVL2_20	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_21	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_22	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_23	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_24	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
LVL2_25	=	[0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0,	0  ]
MATRICE_LVL2	=	[LVL2_1,	LVL2_2,	LVL2_3,	LVL2_4,	LVL2_5,	LVL2_6,	LVL2_7,	LVL2_8,	LVL2_9,	LVL2_10,	LVL2_11,	LVL2_12,	LVL2_13,	LVL2_14,	LVL2_15,	LVL2_16,	LVL2_17,	LVL2_18,	LVL2_19,	LVL2_20,	LVL2_21,	LVL2_22,	LVL2_23,	LVL2_24,	LVL2_25  ]
																										
LISTE_INDICES_LVL2	=	[1,	2,	3,	4,	5,	6,	7  ]																		
LISTE_COULEUR_LVL2	=	["#0D0D0D",	"#00B0F0",	"#99CC00",	"#FF0000",	"#FFC000",	"#FFFF00",	"#9933FF"  ]																		
LISTE_RESISTS_LVL2	=	[10,	0,	0,	0,	0,	0,	0  ]																		
LISTE_POINTSS_LVL2	=	[10,	1,	2,	5,	20,	50,	10  ]																		
LISTE_XPPPPPP_LVL2	=	[10,	2,	4,	10,	1,	1,	1  ]																		
LISTE_POWERUP_LVL2	=	[0,	0,	0,	0,	"super_bonus",	"multiballe",	"pplus"  ]																		
LISTE_GOLDDDD_LVL2	=	[5,	1,	2,	5,	1,	1,	1  ]																		


CORRESPONDANCE_LVL2 =[]    
for i in range(len(LISTE_COULEUR_LVL2)):
    ensemble = [LISTE_INDICES_LVL2[i],LISTE_COULEUR_LVL2[i],LISTE_RESISTS_LVL2[i],LISTE_POINTSS_LVL2[i],LISTE_XPPPPPP_LVL2[i],LISTE_POWERUP_LVL2[i],LISTE_GOLDDDD_LVL2[i]]
    CORRESPONDANCE_LVL2 += [ensemble]    


 
    
#Création du dico des patterns et des powerup
DICO_HISTOIRE = [[0,MATRICE_LVL0,CORRESPONDANCE_LVL0],[1,MATRICE_LVL1,CORRESPONDANCE_LVL1],[2,MATRICE_LVL2,CORRESPONDANCE_LVL2],[3,MATRICE_EMOJI,CORRESPONDANCE_EMOJI]]
DICO_PATTERNS = [["LVL1",MATRICE_LVL1,CORRESPONDANCE_LVL1],["LVL0",MATRICE_LVL0,CORRESPONDANCE_LVL0],["DIAG",MATRICE_DIAG,CORRESPONDANCE_DIAG],["VIDE",MATRICE_VIDE,CORRESPONDANCE_VIDE],["TEST",MATRICE_TEST,CORRESPONDANCE_TEST],["RAINBOW",MATRICE_RAINBOW,CORRESPONDANCE_RAINBOW],["FOUR",MATRICE_FOUR,CORRESPONDANCE_FOUR],["EMOJI",MATRICE_EMOJI,CORRESPONDANCE_EMOJI]]
DICO_POWERUP = [["live_up","+<3"],["pplus","P+"],["multiplicateur2","x2"],["multiplicateur5","x5"],["speed_down","Slow"],["no_bounce","NB"],["super_bonus","SB"],["multiballe","MB"]]

#données powerup
#Live UP
NB_VIE_SUP = 1

#Speed Down
DUREE_SD = 5
RATIO_SD = 2/3
COULEUR_SD = "Lightgreen"

#Super Bonus
DUREE_SB = 7
PUISSANCE_SB = 3
NO_BOUNCE_MODE = True
COULEUR_SB = "gold"

#Pplus
PUISSANCE_PPLUS = 1

#Multiplicateur2
DUREE_MULT2 = 10
COULEUR_MULT2 = "darkorange"

#Multiplicateur5
DUREE_MULT5 = 5
COULEUR_MULT5 = "red"

#no bounce
DUREE_NB = 10
COULEUR_NB = "white"

#multiballes
COULEUR_MB = "black"
NB_BALLES_SUP = 2
