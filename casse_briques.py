#!/usr/bin/env Python

"""Jeux de Casse-Briques !

Usage:
======
    A définir
"""

__authors__ = ("Ziggy")
__contact__ = ("")
__copyright__ = ""
__date__ = "06-10-2022"
__version__= "1.0"

import sys
import os
import pygame
import math
import tkinter as tk
import random as rd
import threading as th
import time
from PIL import Image, ImageTk

from briques import *
from projectiles import *
from joueur_briques import *
                

INDICE_PATTERN_NG = "TEST"
INDICE_PATTERN_RELOAD = "EMOJI"


class Casse_Briques(tk.Tk):
    def __init__(self):
        """Constructeur de l'appli"""
        tk.Tk.__init__(self)
        #initialisation pygame, son et images
        pygame.init()
        pygame.mixer.init()
        #sons
        self.channel_powerup = pygame.mixer.Channel(1)
        fichier_sons = 'sons'
        son_bienvenue = pygame.mixer.Sound(os.path.join(fichier_sons, 'welcome_to_the_jungle.mp3'))
        self.son_service = pygame.mixer.Sound(os.path.join(fichier_sons, 'smack-1.mp3'))
        self.son_raquette = pygame.mixer.Sound(os.path.join(fichier_sons, 'mechanical-clonk-1.mp3'))
        self.son_mur = pygame.mixer.Sound(os.path.join(fichier_sons, 'Ballon contre mur.mp3'))
        self.son_touche_brique = pygame.mixer.Sound(os.path.join(fichier_sons, 'button-15.mp3'))
        self.son_casse_brique = pygame.mixer.Sound(os.path.join(fichier_sons, 'Mario_Bros_Coin_Sound.mp3'))
        self.son_lvlup = pygame.mixer.Sound(os.path.join(fichier_sons, '01-power-up-mario.mp3'))
        self.son_lance_missile1 = pygame.mixer.Sound(os.path.join(fichier_sons, 'Petard a meche.mp3'))
        self.son_lance_missile2 = pygame.mixer.Sound(os.path.join(fichier_sons, 'Coup de feu de 357 magnum 9 mm.mp3'))
        self.son_lance_missile3 = pygame.mixer.Sound(os.path.join(fichier_sons, 'Coup de feu de beretta m12 9 mm.mp3'))
        self.son_explo_missile1 = pygame.mixer.Sound(os.path.join(fichier_sons, 'bulletimpact.mp3'))
        self.son_explo_missile2 = pygame.mixer.Sound(os.path.join(fichier_sons, 'gun-gunshot-02.mp3'))
        self.son_explo_missile3 = pygame.mixer.Sound(os.path.join(fichier_sons, 'impact_explosion_03.mp3'))
        self.son_plus_missile = pygame.mixer.Sound(os.path.join(fichier_sons, 'Pistolet desarmement chien.mp3'))
        self.son_mort = pygame.mixer.Sound(os.path.join(fichier_sons, 'Docteur maboul.mp3'))
        self.son_powerup_liveup = pygame.mixer.Sound(os.path.join(fichier_sons, 'mario-1up.mp3'))
        self.son_powerup_pplus = pygame.mixer.Sound(os.path.join(fichier_sons, 'LASRGun_Blaster.mp3'))
        self.son_powerup_nobounce = pygame.mixer.Sound(os.path.join(fichier_sons, 'laseralien.mp3'))
        # pygame.mixer.Sound.set_volume(self.son_powerup_nobounce,0.1)
        self.son_powerup_superbonus = pygame.mixer.Sound(os.path.join(fichier_sons, 'Mario Star Power Sound Effect.mp3'))
        self.son_powerup_mult2 = pygame.mixer.Sound(os.path.join(fichier_sons, 'bumper.mp3'))
        self.son_partie_gagnee = pygame.mixer.Sound(os.path.join(fichier_sons, 'epicsaxguy.mp3'))
        self.son_partie_perdue = pygame.mixer.Sound(os.path.join(fichier_sons, 'directed-by-robert-b.mp3'))
        self.son_lolilol = pygame.mixer.Sound(os.path.join(fichier_sons, 'FART.mp3'))
        #son bienvenu
        # pygame.mixer.Sound.play(son_bienvenue)
        #Musiques
        self.channel_musique = pygame.mixer.Channel(0)
        fichier_musiques = 'sons\musiques'
        self.musique_lvl0 = pygame.mixer.Sound(os.path.join(fichier_musiques, 'Sonic-Green-Hill.mp3'))
        self.musique_lvl1 = pygame.mixer.Sound(os.path.join(fichier_musiques, 'iron-man-01.mp3'))
        self.musique_lvl2 = pygame.mixer.Sound(os.path.join(fichier_musiques, 'midnight-ride-01a.mp3'))
        self.dico_musique ={0:self.musique_lvl0,1:self.musique_lvl1,2:self.musique_lvl2}
        #décors
        decor_lvl0 = 'images\sol.png'
        decor_lvl1 = 'images\ciel.png'
        decor_lvl2 = 'images\sunset.png'
        self.dico_decor = {0 : decor_lvl0, 1 : decor_lvl1, 2 : decor_lvl2}
        #initialisation listes des threads
        self.liste_threads_sd = []
        self.liste_threads_mult2 = []
        self.liste_threads_mult5 = []
        self.liste_threads_nb = []
        self.liste_threads_sb = []
        self.liste_threads_souris = []
        #dimmensionnement et bloquage de la fenêtre
        self.geometry(f"{L_JEU + L_MENU + 2 * DECALAGE}x{H_MENU}+0+10")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.stop)
        self.arrete_souris = False
        #création des widgets
        # création canevas fenêtre de jeu
        self.canv = tk.Canvas(self, bg="white", height=H_JEU,width=L_JEU + 1)
        self.canv.place(x=DECALAGE ,y=DECALAGE)
        self.fond = self.canv.create_text(0,0,tags='fond')
        #frame menu
        self.cadre_menu = tk.Frame(self, height= H_MENU,width=L_MENU)
        self.cadre_menu.place(x=L_JEU + 2 * DECALAGE,y=DECALAGE)
        #Label titre
        tk.Label(self, text=f"{'SUPER':^13s}\n{'CASSE-BRIQUES':^13s}", font=('castellar',25)).place(x=L_JEU + 15 ,y= 10)
        # self.label_titre.place(x=L_JEU + 15 ,y= 10)
        #Label explication
        tk.Label(self, text="Bienvenue dans Casse-Briques\nClic gauche ou flèche du haut\npour lancer la balle\nDéplacement avec la souris ou les flèches",font=23).place(x=L_JEU + 10 ,y= int(H_JEU/5)-30)
        # self.label_bonjour.place(x=L_JEU + 10 ,y= int(H_JEU/5)-30)
        #cadre du joueur
        self.cadre_joueur = tk.Frame(self,width=L_CADRE_JOUEUR, bg = "#808080", bd = 2)
        self.label_joueur_nom = tk.Label(self.cadre_joueur,anchor=tk.W,bg ="#6600CC", font=('Eras Bold ITC',10))
        self.label_joueur_nom.grid(column=1, row = 1,sticky=tk.E+tk.W)
        self.label_joueur_niveau = tk.Label(self.cadre_joueur,bg ="#6600CC",anchor=tk.W, font=('Eras Bold ITC',10))
        self.label_joueur_niveau.grid(column=1, row = 3,sticky=tk.E+tk.W)
        self.cadre_joueur.columnconfigure(1, minsize=L_CADRE_JOUEUR)
        #Bouton choix profil
        self.bouton_choix_profil = tk.Button(self, text="Changer de profil",command=self.set_profils)
        self.bouton_choix_profil.place(x=L_JEU + int(L_MENU/2)-50,y= int(H_JEU/4)+100)
        #frame mode
        self.cadre_mode = tk.Frame(self, cursor="hand1",height=120,width=L_MENU)
        self.cadre_mode.place(x=L_JEU + 10 ,y= int(H_JEU/2)-30)
        #Label choix mode
        self.label_mode = tk.Label(self.cadre_mode, text="Choix du mode :", font=20)
        self.label_mode.place(x=1,y=1) 
        #Radiobouton choix mode
        self.choix_mode = tk.StringVar(self.cadre_mode,value="Histoire")
        self.radio_papa = tk.Radiobutton(self.cadre_mode, text="Histoire", variable=self.choix_mode, value="Histoire", command=self.set_niveau)
        self.radio_papa.place(x=1, y=30)
        self.radio_infini = tk.Radiobutton(self.cadre_mode, text="Infini", variable=self.choix_mode, value="Infini", command=self.set_niveau)
        self.radio_infini.place(x=1, y=60)
        self.radio_juju = tk.Radiobutton(self.cadre_mode, text="Juju", variable=self.choix_mode, value="Juju", command=self.set_niveau)
        self.radio_juju.place(x=1, y=90)
        #forcage du mode Histoire au démarrage
        self.vitesse_balle = V0_BALLE_PAPA
        #Boutons launch
        self.bouton_lancer = tk.Button(self, text="Nouvelle partie",command=self.nouvelle_partie)
        self.bouton_lancer.place(x=L_JEU + int(L_MENU/2) - 40,y= int(H_JEU/2)+100)
        #Boutons quitter
        self.bouton_quitter = tk.Button(self, text="Quitter",command=self.stop)
        self.bouton_quitter.place(x=L_JEU + int(L_MENU/2) - 40 + 20,y= int(H_JEU/2) + 130)
        #Frame highscore
        self.cadre_highscores = tk.Frame(self, cursor="man",height=101,width=L_MENU-DECALAGE, bg = "#808080")
        self.cadre_highscores.place(x=L_JEU + 10 ,y= H_JEU -100)
        #Label highscores
        self.label_meilleurs = tk.Label(self.cadre_highscores,width=15,anchor = tk.W, text="Meilleurs Scores :", font=20, bg = "#808080")
        self.label_meilleurs.place(x=1,y=1) 
        self.label_record_papa = tk.Label(self.cadre_highscores,width=32,anchor = tk.W, text="Mode Histoire :", font=20, bg = "#C5D9F1")
        self.label_record_papa.place(x=1,y=26)
        self.label_record_infini = tk.Label(self.cadre_highscores,width=32,anchor = tk.W, text="Mode Infini :", font=20, bg = "#C5D9F1")
        self.label_record_infini.place(x=1,y=51)
        self.label_record_juju = tk.Label(self.cadre_highscores,width=32,anchor = tk.W, text="Mode Juju :", font=20, bg = "#C5D9F1")
        self.label_record_juju.place(x=1,y=76)
        #cadre des upgrades
        self.cadre_upgrades = tk.Frame(self,bg = "#808080", bd = 2)
        self.cadre_upgrades.place(x=2*DECALAGE + L_CADRE_JOUEUR,y=H_JEU + 2*DECALAGE)
        self.label_upgrades = tk.Label(self.cadre_upgrades, font =('bold','-15'),bg = "#99CC00")
        self.label_upgrades.grid(column=1,row=1,sticky = tk.W+tk.E, columnspan=4,pady=(2,1))
        liste_L_raq = ["L_raq",[self.label_upgrades]]
        #up raquette
        label_L_raq1 = tk.Label(self.cadre_upgrades,anchor = tk.W, text="Améliorations Raquette :",font=('bold','-15'),bg = "#99CC00")
        label_L_raq1.grid(column=1, columnspan=3,row=2,sticky = tk.W+tk.E,pady=(1,0))
        liste_L_raq[1].append(label_L_raq1)
        label_L_raq2 = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Largeur du centre :",font=('bold','-10'),bg = "#99CC00")
        label_L_raq2.grid(column=3,row=3,sticky = tk.W+tk.E,pady=(1,0))
        liste_L_raq[1].append(label_L_raq2)
        self.label_lraq = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_lraq.grid(column=4,row=3,sticky = tk.W+tk.E,pady=(1,0),padx=(0,1))
        liste_L_raq[1].append(self.label_lraq)
        label_B_raq = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Largeur des bords :",font=('bold','-10'),bg = "#99CC00")
        label_B_raq.grid(column=3,row=4,sticky = tk.W+tk.E,pady=(1,0))
        liste_B_raq = ["B_raq",[label_B_raq]]
        self.label_lbords = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_lbords.grid(column=4,row=4,sticky = tk.W+tk.E,pady=(1,0),padx=(0,1))
        liste_B_raq[1].append(self.label_lbords)
        label_mania_raq = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Maniabilité :",font=('bold','-10'),bg = "#99CC00")
        label_mania_raq.grid(column=3,row=5,sticky = tk.W+tk.E,pady=1)
        liste_mania_raq = ["Maniabilité_raq",[label_mania_raq]]
        self.label_maniabilite = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_maniabilite.grid(column=4,row=5,sticky = tk.W+tk.E,pady=1,padx=(0,1))
        liste_mania_raq[1].append(self.label_maniabilite)
        #up missiles
        label_mis1 = tk.Label(self.cadre_upgrades,anchor = tk.W, text="Améliorations Missiles :",font=('bold','-13'),bg = "#99CC00")
        label_mis1.grid(column=1, columnspan=3,row=6,sticky = tk.W+tk.E,pady=(1,0))
        liste_up_missiles = ["Missiles",[label_mis1]]
        label_mis2 = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Modèle :",font=('bold','-10'),bg = "#99CC00")
        label_mis2.grid(column=3,row=7,sticky = tk.W+tk.E,pady=(1,0))
        liste_up_missiles[1].append(label_mis2)
        self.label_mod_missile = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_mod_missile.grid(column=4,row=7,sticky = tk.W+tk.E,pady=(1,0),padx=(0,1))
        liste_up_missiles[1].append(self.label_mod_missile)
        label_mis3 = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Puissance :",font=('bold','-10'),bg = "#99CC00")
        label_mis3.grid(column=3,row=8,sticky = tk.W+tk.E,pady=(1,0))
        liste_up_missiles[1].append(label_mis3)
        self.label_pmissile = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_pmissile.grid(column=4,row=8,sticky = tk.W+tk.E,pady=(1,0),padx=(0,1))
        liste_up_missiles[1].append(self.label_pmissile)
        label_mis4 = tk.Label(self.cadre_upgrades,anchor = tk.E, text="Quantité max. :",font=('bold','-10'),bg = "#99CC00")
        label_mis4.grid(column=3,row=9,sticky = tk.W+tk.E,pady=1)
        liste_up_missiles[1].append(label_mis4)
        self.label_nbmissile = tk.Label(self.cadre_upgrades,font=('bold','-10'),bg = "#99CC00")
        self.label_nbmissile.grid(column=4,row=9,sticky = tk.W+tk.E,pady=1,padx=(0,1))
        liste_up_missiles[1].append(self.label_nbmissile)
        #up autres
        label_vie1 = tk.Label(self.cadre_upgrades,anchor = tk.W, text="Vies au départ :",font=('bold','-14'),bg = "#99CC00")
        label_vie1.grid(column=3,row=10,sticky = tk.W+tk.E,pady=1)
        liste_up_vies = ["Vies",[label_vie1]]
        self.label_viemax = tk.Label(self.cadre_upgrades,font=('bold','-13'),bg = "#99CC00")
        self.label_viemax.grid(column=4,row=10,sticky = tk.W+tk.E,pady=1,padx=(0,1))
        liste_up_vies[1].append(self.label_viemax)
        label_puis1 = tk.Label(self.cadre_upgrades,anchor = tk.W, text="Puissance balle :",font=('bold','-14'),bg = "#99CC00")
        label_puis1.grid(column=3,row=11,sticky = tk.W+tk.E,pady=(1,2))
        liste_P_balle = ["P_balle",[label_puis1]]
        self.label_puissance_flat = tk.Label(self.cadre_upgrades,font=('bold','-13'),bg = "#99CC00")     
        self.label_puissance_flat.grid(column=4,row=11,sticky = tk.W+tk.E,pady=(1,2),padx=(0,1))    
        liste_P_balle[1].append(self.label_puissance_flat)
        #zone ephemere
        self.ephemere = []
        #L raq
        bouttonplus_raq_L = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_raq_L.cget('text'),"L_raq"))
        bouttonplus_raq_L.grid(column=1,row=3,pady=(1,0))
        self.ephemere.append(bouttonplus_raq_L)
        liste_L_raq[1].append(bouttonplus_raq_L)
        bouttonmoins_raq_L = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_raq_L.cget('text'),"L_raq"))
        bouttonmoins_raq_L.grid(column=2,row=3,pady=(1,0))
        self.ephemere.append(bouttonmoins_raq_L)
        liste_L_raq[1].append(bouttonmoins_raq_L)
        label_nv = tk.Label(self.cadre_upgrades,text=f"{'Nouvelle':^10s}\n{'valeur':^10s}",font=('bold','-10'),bg = "#99CC00")
        label_nv.grid(column=5,row=2,sticky = tk.W+tk.E,pady=(1,0),padx=1)
        self.ephemere.append(label_nv)
        liste_L_raq[1].append(label_nv)
        label_cout_futur = tk.Label(self.cadre_upgrades,text="Coût point\nsuivant",font=('bold','-10'),bg = "#99CC00")
        label_cout_futur.grid(column=6,row=2,sticky = tk.W+tk.E,pady=(1,0))
        self.ephemere.append(label_cout_futur)
        liste_L_raq[1].append(label_cout_futur)
        self.label_nv_L_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_L_raq.grid(column=5,row=3,sticky = tk.W+tk.E,pady=(1,0),padx=1)
        self.ephemere.append(self.label_nv_L_raq)
        liste_L_raq[1].append(self.label_nv_L_raq)
        self.label_cout_L_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_L_raq.grid(column=6,row=3,sticky = tk.W+tk.E,pady=(1,0))
        self.ephemere.append(self.label_cout_L_raq)
        liste_L_raq[1].append(self.label_cout_L_raq)           
        #B raq
        bouttonplus_raq_B = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_raq_B.cget('text'),"B_raq"))
        bouttonplus_raq_B.grid(column=1,row=4,pady=(1,0))
        self.ephemere.append(bouttonplus_raq_B)
        liste_B_raq[1].append(bouttonplus_raq_B)
        bouttonmoins_raq_B = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_raq_B.cget('text'),"B_raq"))
        bouttonmoins_raq_B.grid(column=2,row=4,pady=(1,0))
        self.ephemere.append(bouttonmoins_raq_B)
        liste_B_raq[1].append(bouttonmoins_raq_B)
        self.label_nv_B_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_B_raq.grid(column=5,row=4,sticky = tk.W+tk.E,pady=(1,0),padx=1)
        self.ephemere.append(self.label_nv_B_raq)
        liste_B_raq[1].append(self.label_nv_B_raq)
        self.label_cout_B_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_B_raq.grid(column=6,row=4,sticky = tk.W+tk.E,pady=(1,0))
        self.ephemere.append(self.label_cout_B_raq)
        liste_B_raq[1].append(self.label_cout_B_raq) 
        #Maniabilité
        bouttonplus_raq_M = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_raq_M.cget('text'),"Maniabilité_raq"))
        bouttonplus_raq_M.grid(column=1,row=5,pady=1)
        self.ephemere.append(bouttonplus_raq_M)
        liste_mania_raq[1].append(bouttonplus_raq_M)
        bouttonmoins_raq_M = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_raq_M.cget('text'),"Maniabilité_raq"))
        bouttonmoins_raq_M.grid(column=2,row=5,pady=1)
        self.ephemere.append(bouttonmoins_raq_M)
        liste_mania_raq[1].append(bouttonmoins_raq_M)
        self.label_nv_mania_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_mania_raq.grid(column=5,row=5,sticky = tk.W+tk.E,pady=1,padx=1)
        self.ephemere.append(self.label_nv_mania_raq)
        liste_mania_raq[1].append(self.label_nv_mania_raq)
        self.label_cout_mania_raq = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_mania_raq.grid(column=6,row=5,sticky = tk.W+tk.E,pady=1)
        self.ephemere.append(self.label_cout_mania_raq)
        liste_mania_raq[1].append(self.label_cout_mania_raq) 
        #Missiles
        #Modèles
        bouttonplus_mis_mod = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_mis_mod.cget('text'),"Missiles_M"))
        bouttonplus_mis_mod.grid(column=1,row=7,pady=(1,0))
        self.ephemere.append(bouttonplus_mis_mod)
        liste_up_missiles[1].append(bouttonplus_mis_mod) 
        bouttonmoins_mis_mod = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_mis_mod.cget('text'),"Missiles_M"))
        bouttonmoins_mis_mod.grid(column=2,row=7,pady=(1,0))
        self.ephemere.append(bouttonmoins_mis_mod)
        liste_up_missiles[1].append(bouttonmoins_mis_mod) 
        self.label_nv_mis_mod = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_mis_mod.grid(column=5,row=7,sticky = tk.W+tk.E,pady=(1,0),padx=1)
        self.ephemere.append(self.label_nv_mis_mod)
        liste_up_missiles[1].append(self.label_nv_mis_mod)
        self.label_cout_mis_mod = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_mis_mod.grid(column=6,row=7,sticky = tk.W+tk.E,pady=(1,0))
        self.ephemere.append(self.label_cout_mis_mod)
        liste_up_missiles[1].append(self.label_cout_mis_mod) 
        #Puissance
        bouttonplus_mis_P = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_mis_P.cget('text'),"Missiles_P"))
        bouttonplus_mis_P.grid(column=1,row=8,pady=(1,0))
        self.ephemere.append(bouttonplus_mis_P)
        liste_up_missiles[1].append(bouttonplus_mis_P) 
        bouttonmoins_mis_P = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_mis_P.cget('text'),"Missiles_P"))
        bouttonmoins_mis_P.grid(column=2,row=8,pady=(1,0))
        self.ephemere.append(bouttonmoins_mis_P)
        liste_up_missiles[1].append(bouttonmoins_mis_P) 
        self.label_nv_mis_P = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_mis_P.grid(column=5,row=8,sticky = tk.W+tk.E,pady=(1,0),padx=1)
        self.ephemere.append(self.label_nv_mis_P)
        liste_up_missiles[1].append(self.label_nv_mis_P)
        self.label_cout_mis_P = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_mis_P.grid(column=6,row=8,sticky = tk.W+tk.E,pady=(1,0))
        self.ephemere.append(self.label_cout_mis_P)
        liste_up_missiles[1].append(self.label_cout_mis_P)
        #Quantité
        bouttonplus_mis_Q = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_mis_Q.cget('text'),"Missiles_Q"))
        bouttonplus_mis_Q.grid(column=1,row=9,pady=1)
        self.ephemere.append(bouttonplus_mis_Q)
        liste_up_missiles[1].append(bouttonplus_mis_Q)
        bouttonmoins_mis_Q = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_mis_Q.cget('text'),"Missiles_Q"))
        bouttonmoins_mis_Q.grid(column=2,row=9,pady=1)
        self.ephemere.append(bouttonmoins_mis_Q)
        liste_up_missiles[1].append(bouttonmoins_mis_Q)
        self.label_nv_mis_Q = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_nv_mis_Q.grid(column=5,row=9,sticky = tk.W+tk.E,pady=1,padx=1)
        self.ephemere.append(self.label_nv_mis_Q)
        liste_up_missiles[1].append(self.label_nv_mis_Q)
        self.label_cout_mis_Q = tk.Label(self.cadre_upgrades,font=23,bg = "#99CC00")
        self.label_cout_mis_Q.grid(column=6,row=9,sticky = tk.W+tk.E,pady=1)
        self.ephemere.append(self.label_cout_mis_Q)
        liste_up_missiles[1].append(self.label_cout_mis_Q)
        #Vie
        bouttonplus_vie = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_vie.cget('text'),"Vies"))
        bouttonplus_vie.grid(column=1,row=10,pady=1)
        self.ephemere.append(bouttonplus_vie)
        liste_up_vies[1].append(bouttonplus_vie)
        bouttonmoins_vie = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_vie.cget('text'),"Vies"))
        bouttonmoins_vie.grid(column=2,row=10,pady=1)
        self.ephemere.append(bouttonmoins_vie)
        liste_up_vies[1].append(bouttonmoins_vie)
        self.label_nv_viemax = tk.Label(self.cadre_upgrades,font=20,bg = "#99CC00")
        self.label_nv_viemax.grid(column=5,row=10,sticky = tk.W+tk.E,pady=1,padx=1)
        self.ephemere.append(self.label_nv_viemax)
        liste_up_vies[1].append(self.label_nv_viemax)
        self.label_cout_viemax = tk.Label(self.cadre_upgrades,font=20,bg = "#99CC00")
        self.label_cout_viemax.grid(column=6,row=10,sticky = tk.W+tk.E,pady=1)
        self.ephemere.append(self.label_cout_viemax)
        liste_up_vies[1].append(self.label_cout_viemax)
        #P balle
        bouttonplus_pballe = tk.Button(self.cadre_upgrades, text="+",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonplus_pballe.cget('text'),"P_balle"))
        bouttonplus_pballe.grid(column=1,row=11,pady=(1,2))
        self.ephemere.append(bouttonplus_pballe)
        liste_P_balle[1].append(bouttonplus_pballe)
        bouttonmoins_pballe = tk.Button(self.cadre_upgrades, text="-",font=('bold','-8'),height=1, width = 1,command= lambda: self.set_upgrades(bouttonmoins_pballe.cget('text'),"P_balle"))
        bouttonmoins_pballe.grid(column=2,row=11,pady=(1,2))
        self.ephemere.append(bouttonmoins_pballe)
        liste_P_balle[1].append(bouttonmoins_pballe)
        self.label_nv_P_balle = tk.Label(self.cadre_upgrades,font=20,bg = "#99CC00")
        self.label_nv_P_balle.grid(column=5,row=11,sticky = tk.W+tk.E,pady=(1,2),padx=1)
        self.ephemere.append(self.label_nv_P_balle)
        liste_P_balle[1].append(self.label_nv_P_balle)
        self.label_cout_P_balle = tk.Label(self.cadre_upgrades,font=20,bg = "#99CC00")
        self.label_cout_P_balle.grid(column=6,row=11,sticky = tk.W+tk.E,pady=(1,2))
        self.ephemere.append(self.label_cout_P_balle)
        liste_P_balle[1].append(self.label_cout_P_balle)
        bouton_valider = tk.Button(self.cadre_upgrades, text="Valider ?",command=self.premier_service, height=-1)
        bouton_valider.grid(column=5, columnspan=2,row=1,ipadx=5,pady=(2,1),padx=(5,2),sticky=tk.E)
        self.ephemere.append(bouton_valider)
        liste_L_raq[1].append(bouton_valider)
        self.cadre_upgrades.columnconfigure(1, minsize=1,weight = 1)
        self.cadre_upgrades.columnconfigure(2, minsize=1,weight = 1)
        self.cadre_upgrades.columnconfigure(3,weight = 10)
        self.cadre_upgrades.columnconfigure(4,weight = 10)
        self.cadre_upgrades.columnconfigure(5,weight = 10)
        self.cadre_upgrades.columnconfigure(6,weight = 10)
        self.cadre_upgrades.columnconfigure(7,weight = 10)
        self.dico_widget = dict([liste_L_raq,liste_B_raq,liste_mania_raq,liste_up_missiles,liste_up_vies,liste_P_balle])
        for up in self.dico_widget :
            for widg in self.dico_widget[up]:
                widg.grid_remove()
        #bouton et bind mute
        self.musique_muet = False
        self.sons_muet = False
        self.var_bm = tk.IntVar()
        self.bouton_mute = tk.Checkbutton(self, text="Sons et musique (M)", variable = self.var_bm, command = self.change_mute)
        self.bouton_mute.place(x=L_JEU + 3*DECALAGE, y = H_JEU/3 -20)
        self.var_bms = tk.IntVar()
        self.bouton_mute_musique = tk.Checkbutton(self, text="Musique (L)", variable = self.var_bms, command = self.change_musiques)
        self.bouton_mute_musique.place(x=L_JEU + 3*DECALAGE, y = H_JEU/3)
        self.var_bs = tk.IntVar()
        self.bouton_mute_sons = tk.Checkbutton(self, text="Sons (K)", variable = self.var_bs, command = self.change_sons)
        self.bouton_mute_sons.place(x=L_JEU + 3*DECALAGE, y = H_JEU/3+20)
        self.bouton_mute.select()
        self.bouton_mute_musique.select()
        self.bouton_mute_sons.select()
        self.bind("m", self.raccourci_muet)
        self.bind("l", self.raccourci_muet)
        self.bind("k", self.raccourci_muet)
        #Initialisation de la première partie
        self.set_profils() #set_profils lance nouvelle partie

    def raccourci_muet(self,event):
        if event.char == 'm':
            self.bouton_mute.invoke()
        elif event.char == 'l':
            self.bouton_mute_musique.invoke()
        if event.char == 'k':
            self.bouton_mute_sons.invoke()
          
    def change_mute(self):
        if self.var_bm.get() == 1 :
            self.musique_muet = False
            self.bouton_mute_musique.select()
            self.sons_muet = False
            self.bouton_mute_sons.select()
        else :
            self.musique_muet = True
            self.bouton_mute_musique.deselect()
            self.sons_muet = True
            self.bouton_mute_sons.deselect()
        if self.musique_muet :
            pygame.mixer.pause()
        else: pygame.mixer.unpause()

        
    def change_musiques(self):
        if self.var_bms.get() == 1 :
            self.musique_muet = False
            if self.var_bs.get() == 1 :
                self.bouton_mute.select()
        else :
            self.musique_muet = True
            self.bouton_mute.deselect()
        if self.musique_muet :
            pygame.mixer.pause()
        else: pygame.mixer.unpause()
        
    def change_sons(self):
        if self.var_bs.get() == 1 :
            self.sons_muet = False
            if self.var_bms.get() == 1 :
                self.bouton_mute.select()
        else :
            self.sons_muet = True
            self.bouton_mute.deselect()
        

    """Fonction pour le mode de jeu, a finir"""
     
    def set_niveau(self,event=None):
        if self.choix_mode.get() == "Histoire" :
            self.vitesse_balle = V0_BALLE_PAPA
            self.l_raquette = self.joueur_courant.attributs[0]
            self.attributes('-fullscreen', False)
            self.geometry(f"{L_JEU + L_MENU + 2 * DECALAGE}x{H_MENU}+10+10")
            self.resizable(width=False, height=False)
        elif self.choix_mode.get() == "Juju" :
            self.vitesse_balle = V0_BALLE_JUJU
            self.l_raquette = L_RAQUETTE_JUJU
            self.attributes('-fullscreen', True)
        self.nouvelle_partie()

    """Fonctions qui lance les nouvelles parties ou nouvelle manche après une mort
    
        - nouvelle_partienouvelle_partie(self,event=None)
            vide les threads, defreeze les menus, crée tout le décor et charge tous les attributs du joueur
        - nouvelle_manche(self)
            defreeze quelques boutons et rebind le service
    """
  
    def nouvelle_partie(self,event=None) :
        self.arrete_souris = True
        #On attend que les powerup se terminent avant nouvelle partie
        matrice_threads = [self.liste_threads_sd,self.liste_threads_mult2,self.liste_threads_mult5,self.liste_threads_nb,self.liste_threads_sb] #,self.liste_threads_souris]
        for liste_thr in matrice_threads :
            for thr in liste_thr :
                thr.join()
        #vidage liste des threads
        self.liste_threads_sd = []
        self.liste_threads_pplus = []
        self.liste_threads_nb = []
        self.liste_threads_sb = []
        self.liste_threads_souris = []
        #récupération des scores
        self.get_highscore()
        #defreeze
        for child in self.cadre_mode.winfo_children():
            child.configure(state=tk.NORMAL)
        self.bouton_choix_profil.configure(state=tk.NORMAL)
        self.bouton_lancer.configure(state=tk.NORMAL)
        #coupage du son de victoire si besoin
        pygame.mixer.Sound.stop(self.son_partie_gagnee) 
        #On efface tout
        self.canv.delete('all')
        self.balle_servie = False
        self.en_pause = False
        self.liste_widg_a_cacher = []
        self.eph_a_vider = []
        #création (ou MAJ) du joueur et affichage
        self.get_profils()
        if self.new_player :
            self.joueur_courant = Joueur([self.le_joueur,1,0,[0,0,0],"LVL0",[20,1,'Inexistante',2,1,'1-1','5-1','0-0-0'],0,0])
            self.joueur_provisoire = Joueur([self.le_joueur,1,0,[0,0,0],"LVL0",[20,1,'Inexistante',2,1,'1-1','5-1','0-0-0'],0,0])        
        else:
            for prof in self.liste_profils :
                if prof[0] == self.le_joueur :
                    self.joueur_courant = Joueur(prof)
                    self.joueur_provisoire = Joueur(prof)                
        self.label_joueur_nom.configure(text=f"Joueur : {self.joueur_courant.nom:<15s}")
        self.label_joueur_niveau.configure(text=f"Niveau : {self.joueur_courant.niveau:<2d}")
        self.cadre_joueur.place(x=2*DECALAGE,y=H_JEU + 2*DECALAGE)
        #
        #Binding
        self.bind("n", self.nouvelle_partie)
        self.bind("<Escape>", self.stop)
        self.bind("f",self.prout)
        #MAJ du cadre UPGRADES
        #si première partie du joueur, on skip la phase d'upgrade
        if self.joueur_courant.niveau == 1:
            self.maj_valeur_et_cadre_upgrades(situation = 'définitive')
            self.premier_service()
        #sinon on MAJ le cadre upgrade et on initialise tous les paliers
        else:
            self.maj_valeur_et_cadre_upgrades(situation = 'définitive')
            self.palier_init_L_raq = self.joueur_provisoire.palier_nv_cout("L_raq",self.joueur_provisoire.attributs[0])[0]
            self.palier_init_B_raq = self.joueur_provisoire.palier_nv_cout("B_raq",self.joueur_provisoire.attributs[1])[0]
            self.palier_init_Maniabilite_raq = self.joueur_provisoire.palier_nv_cout("Maniabilité_raq",self.joueur_provisoire.attributs[2])[0]
            self.palier_init_Missiles_M = self.joueur_provisoire.palier_nv_cout("Missiles_M",self.joueur_provisoire.missile_M)[0]
            self.palier_init_Missiles_P = self.joueur_provisoire.palier_nv_cout("Missiles_P",self.joueur_provisoire.missile_P,self.joueur_provisoire.missile_M)[0]
            self.palier_init_Missiles_Q = self.joueur_provisoire.palier_nv_cout("Missiles_Q",self.joueur_provisoire.missile_Q,self.joueur_provisoire.missile_M)[0]
            self.palier_init_viemax = self.joueur_provisoire.palier_nv_cout("Vies",self.joueur_provisoire.attributs[3])[0]
            self.palier_init_P_balle = self.joueur_provisoire.palier_nv_cout("P_balle",self.joueur_provisoire.attributs[4])[0]
            self.maj_valeur_et_cadre_upgrades(situation = 'provisoire')          
                    
    def maj_valeur_et_cadre_upgrades(self,situation):
        if situation == 'définitive':
            joueur = self.joueur_courant
        else:
            joueur = self.joueur_provisoire
        #Affiche tout
        for up in self.dico_widget :
            for widg in self.dico_widget[up]:
                widg.grid()
        #MAJ pts UP
        self.label_upgrades.config(text=f"Upgrades : {joueur.points_upgrades} point(s) disponible(s)")
        #MAJ des valeurs et affichages
        #up raquette
        if situation == 'définitive':
            self.label_lraq.config(text=f"{joueur.attributs[0]}")
            self.label_lbords.config(text=f"{joueur.attributs[1]}")
            self.label_maniabilite.config(text=f"{joueur.attributs[2]}")
        self.l_raquette = joueur.attributs[0]
        self.l_bords_raquette = joueur.attributs[1]
        if joueur.attributs[2] == 'Inexistante' :
            self.rapidite_raquette = 0.022
            self.rapidite_raquette_clavier = 10        
        elif joueur.attributs[2] == 'Pas top' :
            self.rapidite_raquette = 0.015
            self.rapidite_raquette_clavier = 10
        elif joueur.attributs[2] == 'Acceptable':
            self.rapidite_raquette = 0.003
            self.rapidite_raquette_clavier = 20
        elif joueur.attributs[2] == 'Premium':
            self.rapidite_raquette = 0.0001
            self.rapidite_raquette_clavier = 50
        #up missiles
        self.modele_missiles = joueur.missile_M
        self.puissance_missiles = joueur.missile_P
        self.projectile_type = Projectile(self.modele_missiles,self.puissance_missiles,'type')
        if situation == 'définitive':
            self.label_mod_missile.config(text=f"{self.modele_missiles}")
            self.label_pmissile.config(text=f"{self.puissance_missiles}")        
            self.label_nbmissile.config(text=f"{joueur.missile_Q}")       
            # up autres       
            self.label_viemax.config(text=f"{joueur.attributs[3]}")        
            self.label_puissance_flat.config(text=f"{joueur.attributs[4]}") 
        #MAJ pt UP
        self.label_upgrades.config(text=f"Upgrades : {joueur.points_upgrades} point(s) disponible(s)")
        #maj cout pts suivant  
        if joueur.palier_nv_cout("L_raq",joueur.attributs[0])[3]:
            cout = joueur.palier_nv_cout("L_raq",joueur.attributs[0])[2]
            self.label_cout_L_raq.config(text=f"{cout}",font=23,bg = "#99CC00")
        else :
            niveau = joueur.palier_nv_cout("L_raq",joueur.attributs[0])[4]
            self.label_cout_L_raq.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.palier_nv_cout("B_raq",joueur.attributs[1])[3]:
            cout = joueur.palier_nv_cout("B_raq",joueur.attributs[1])[2]
            self.label_cout_B_raq.config(text=f"{cout}",font=23,bg = "#99CC00") 
        else:
            niveau = joueur.palier_nv_cout("B_raq",joueur.attributs[1])[4]
            self.label_cout_B_raq.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.palier_nv_cout("Maniabilité_raq",joueur.attributs[2])[3]:
            cout = joueur.palier_nv_cout("Maniabilité_raq",joueur.attributs[2])[2]
            self.label_cout_mania_raq.config(text=f"{cout}",font=23,bg = "#99CC00")
        else:
            niveau = joueur.palier_nv_cout("Maniabilité_raq",joueur.attributs[2])[4]
            self.label_cout_mania_raq.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.palier_nv_cout("Missiles_M",joueur.missile_M)[3]:
            cout = joueur.palier_nv_cout("Missiles_M",joueur.missile_M)[2]
            self.label_cout_mis_mod.config(text=f"{cout}",font=23,bg = "#99CC00")
        else:
            niveau = joueur.palier_nv_cout("Missiles_M",joueur.missile_M)[4]
            self.label_cout_mis_mod.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.missile_M != 0 :
            if joueur.palier_nv_cout("Missiles_P",joueur.missile_P,joueur.missile_M)[3]:
                cout = joueur.palier_nv_cout("Missiles_P",joueur.missile_P,joueur.missile_M)[2]
                self.label_cout_mis_P.config(text=f"{cout}",font=23,bg = "#99CC00") 
            else:
                niveau = joueur.palier_nv_cout("Missiles_P",joueur.missile_P,joueur.missile_M)[4]
                self.label_cout_mis_P.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
            if joueur.palier_nv_cout("Missiles_Q",joueur.missile_Q,joueur.missile_M)[3]:    
                cout = joueur.palier_nv_cout("Missiles_Q",joueur.missile_Q,joueur.missile_M)[2]
                self.label_cout_mis_Q.config(text=f"{cout}",font=23,bg = "#99CC00") 
            else:
                niveau = joueur.palier_nv_cout("Missiles_Q",joueur.missile_Q,joueur.missile_M)[4]
                self.label_cout_mis_Q.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.palier_nv_cout("Vies",joueur.attributs[3])[3]:    
            cout = joueur.palier_nv_cout("Vies",joueur.attributs[3])[2]
            self.label_cout_viemax.config(text=f"{cout}",font=23,bg = "#99CC00")
        else:
            niveau = joueur.palier_nv_cout("Vies",joueur.attributs[3])[4]
            self.label_cout_viemax.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        if joueur.palier_nv_cout("P_balle",joueur.attributs[4])[3]:    
            cout = joueur.palier_nv_cout("P_balle",joueur.attributs[4])[2]
            self.label_cout_P_balle.config(text=f"{cout}",font=23,bg = "#99CC00")
        else:
            niveau = joueur.palier_nv_cout("P_balle",joueur.attributs[4])[4]
            self.label_cout_P_balle.config(text=f"Niv. requis {niveau}",font=('',-10,''),bg = "#FF0000")
        #enlève tous les ephemeres si situation = définitive et vide ceux qui ont été modifiés
        if situation == 'définitive' :
            for widg in self.eph_a_vider :
                widg.config(text='')
            for widg in self.ephemere :
                widg.grid_remove()
        #cache les truc pas UNLOCKS
        for upgrade in NIVEAU_UNLOCKS :
            if NIVEAU_UNLOCKS[upgrade] > joueur.niveau :
                self.liste_widg_a_cacher.append(self.dico_widget[upgrade])
        for groupe in self.liste_widg_a_cacher :
                for widg in groupe :
                    widg.grid_remove()

    
    def set_upgrades(self,boutton_appel=None,upgrade=None):
        blocage = False
        #MAJ valeurs suivantes
        # if boutton_appel == '+':                                                       
        if upgrade == "L_raq":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("L_raq",self.joueur_provisoire.attributs[0])
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_L_raq = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.attributs[0] = triple[1]
                    self.label_nv_L_raq.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_L_raq) 
                    self.eph_a_vider.append(self.label_cout_L_raq) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_L_raq > self.palier_init_L_raq :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("L_raq",self.joueur_provisoire.attributs[0])
                    self.palier_courant_L_raq -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.attributs[0] = triple[1]
                    if self.palier_courant_L_raq == self.palier_init_L_raq:
                        self.label_nv_L_raq.config(text='')
                    else :
                        self.label_nv_L_raq.config(text=f"{triple[1]}")
                else: blocage = True
        if upgrade == "B_raq":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("B_raq",self.joueur_provisoire.attributs[1])
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_B_raq = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.attributs[1] = triple[1]
                    self.label_nv_B_raq.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_B_raq)  
                    self.eph_a_vider.append(self.label_cout_B_raq)  
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_B_raq > self.palier_init_B_raq :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("B_raq",self.joueur_provisoire.attributs[1])
                    self.palier_courant_B_raq -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.attributs[1] = triple[1]
                    if self.palier_courant_B_raq == self.palier_init_B_raq:
                        self.label_nv_B_raq.config(text='')
                    else :
                        self.label_nv_B_raq.config(text=f"{triple[1]}")
                else: blocage = True
        if upgrade == "Maniabilité_raq":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("Maniabilité_raq",self.joueur_provisoire.attributs[2])
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_Maniabilite_raq = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.attributs[2] = triple[1]
                    self.label_nv_mania_raq.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_mania_raq) 
                    self.eph_a_vider.append(self.label_cout_mania_raq) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_Maniabilite_raq > self.palier_init_Maniabilite_raq :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("Maniabilité_raq",self.joueur_provisoire.attributs[2])
                    self.palier_courant_Maniabilite_raq -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.attributs[2] = triple[1]
                    if self.palier_courant_Maniabilite_raq == self.palier_init_Maniabilite_raq:
                        self.label_nv_mania_raq.config(text='')
                    else :
                        self.label_nv_mania_raq.config(text=f"{triple[1]}")
                else: blocage = True
        if upgrade == "Missiles_M":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("Missiles_M",self.joueur_provisoire.missile_M)
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_Missiles_M = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.ancienP = self.joueur_provisoire.missile_P
                    self.ancienQ = self.joueur_provisoire.missile_Q
                    self.joueur_provisoire.modele_up()
                    self.label_nv_mis_mod.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_mis_mod) 
                    self.eph_a_vider.append(self.label_cout_mis_mod) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_Missiles_M > self.palier_init_Missiles_M :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("Missiles_M",self.joueur_provisoire.missile_M)
                    self.palier_courant_Missiles_M -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.modele_down(self.ancienP,self.ancienQ)
                    if self.palier_courant_Missiles_M == self.palier_init_Missiles_M:
                        self.label_nv_mis_mod.config(text='')
                    else :
                        self.label_nv_mis_mod.config(text=f"{triple[1]}") 
                else: blocage = True
        if upgrade == "Missiles_P":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("Missiles_P",self.joueur_provisoire.missile_P,self.joueur_provisoire.missile_M)
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_Missiles_P = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.maj_missile_P(triple[1])
                    self.label_nv_mis_P.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_mis_P) 
                    self.eph_a_vider.append(self.label_cout_mis_P) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_Missiles_P > self.palier_init_Missiles_P :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("Missiles_P",self.joueur_provisoire.missile_P,self.joueur_provisoire.missile_M)
                    self.palier_courant_Missiles_P -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.maj_missile_P(triple[1])
                    if self.palier_courant_Missiles_P == self.palier_init_Missiles_P:
                        self.label_nv_mis_P.config(text='')
                    else :
                        self.label_nv_mis_P.config(text=f"{triple[1]}")
                else: blocage = True
        if upgrade == "Missiles_Q":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("Missiles_Q",self.joueur_provisoire.missile_Q,self.joueur_provisoire.missile_M)
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_Missiles_Q = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.maj_missile_Q(triple[1])
                    self.label_nv_mis_Q.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_mis_Q) 
                    self.eph_a_vider.append(self.label_cout_mis_Q) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_Missiles_Q > self.palier_init_Missiles_Q :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("Missiles_Q",self.joueur_provisoire.missile_Q,self.joueur_provisoire.missile_M)
                    self.palier_courant_Missiles_Q -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.maj_missile_Q(triple[1])
                    if self.palier_courant_Missiles_Q == self.palier_init_Missiles_Q:
                        self.label_nv_mis_Q.config(text='')
                    else :
                        self.label_nv_mis_Q.config(text=f"{triple[1]}") 
                else: blocage = True
        if upgrade == "Vies":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("Vies",self.joueur_provisoire.attributs[3])
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_viemax = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.attributs[3] = triple[1]
                    self.label_nv_viemax.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_viemax) 
                    self.eph_a_vider.append(self.label_cout_viemax) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_viemax > self.palier_init_viemax :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("Vies",self.joueur_provisoire.attributs[3])
                    self.palier_courant_viemax -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.attributs[3] = triple[1]
                    if self.palier_courant_viemax == self.palier_init_viemax :
                        self.label_nv_viemax.config(text='')
                    else :
                        self.label_nv_viemax.config(text=f"{triple[1]}")
                else: blocage = True
        if upgrade == "P_balle":
            if boutton_appel == '+':
                triple = self.joueur_provisoire.palier_nv_cout("P_balle",self.joueur_provisoire.attributs[4])
                if triple[1] != "max" and triple[2]<= self.joueur_provisoire.points_upgrades and triple[3] :
                    self.palier_courant_P_balle = triple[0]+1
                    self.joueur_provisoire.points_upgrades -= triple[2]
                    self.joueur_provisoire.attributs[4] = triple[1]
                    self.label_nv_P_balle.config(text=f"{triple[1]}")
                    self.eph_a_vider.append(self.label_nv_P_balle) 
                    self.eph_a_vider.append(self.label_cout_P_balle) 
                else: blocage = True
            elif boutton_appel == '-':
                if self.palier_courant_P_balle > self.palier_init_P_balle :
                    triple = self.joueur_provisoire.palier_nv_cout_retour("P_balle",self.joueur_provisoire.attributs[4])
                    self.palier_courant_P_balle -= 1
                    self.joueur_provisoire.points_upgrades += triple[2]
                    self.joueur_provisoire.attributs[4] = triple[1]
                    if self.palier_courant_P_balle == self.palier_init_P_balle :
                        self.label_nv_P_balle.config(text='')
                    else :
                        self.label_nv_P_balle.config(text=f"{triple[1]}")
                else: blocage = True
        if blocage and self.sons_muet == False :
            pygame.mixer.Sound.play(self.son_plus_missile)
        self.maj_valeur_et_cadre_upgrades(situation = 'provisoire')  
        
            
    def premier_service(self):
        #validation des up dépensés
        self.joueur_courant.attributs = self.joueur_provisoire.attributs
        self.joueur_courant.missile_M = self.joueur_provisoire.missile_M
        self.joueur_courant.missile_P = self.joueur_provisoire.missile_P
        self.joueur_courant.missile_Q = self.joueur_provisoire.missile_Q
        self.joueur_courant.points_upgrades = self.joueur_provisoire.points_upgrades
        #MAJ des cadres upgrades sans les ephemeres
        if self.joueur_courant.niveau > 1:
            self.maj_valeur_et_cadre_upgrades(situation = 'définitive')
        #bool pour thread souris
        self.arrete_souris = False
        # BINDING DES ACTIONS.
        self.bind("<Right>", self.raquette_droite_clavier)
        self.bind("<Left>", self.raquette_gauche_clavier)
        self.bind("<Motion>",self.mouvement_souris)
        self.bind("<space>",self.pause)
        #binding ou rebinding du service
        self.bind("<Up>",self.move)
        self.canv.bind("<Button-1>",self.move)
        #génération du monde
        self.level_courant = 0
        self.gen_monde(self.level_courant)
        #La vie
        self.pt_vie = self.joueur_courant.attributs[3]
        self.label_vie = self.canv.create_text(X_VIE + 20, Y_VIE, text=f"{self.pt_vie}", fill='red', state=tk.DISABLED, font=('',-20,'bold'),tags='coeur')
        self.fichier_image_coeur = Image.open('images\coeur.png')
        self.fichier_image_coeur_redim = self.fichier_image_coeur.resize((20,20))
        self.image_coeur = ImageTk.PhotoImage(self.fichier_image_coeur_redim)
        self.canv.create_image(X_VIE,Y_VIE,anchor=tk.CENTER, image = self.image_coeur)
        #la puissance
        self.puissance_balle = self.joueur_courant.attributs[4]
        self.puissance_bonus = 0
        self.label_puissance = self.canv.create_text(X_VIE + 90, Y_VIE, text=f"Puissance : {self.puissance_balle+self.puissance_bonus}", fill="slateblue", state=tk.DISABLED, font=('',-15,'bold'))
        #le niveau/xp
        largeur_barre_xp = int(self.joueur_courant.xp / (self.joueur_courant.xp + self.joueur_courant.xp_avant_lvlup) * 124)
        self.barre_xp = self.canv.create_rectangle(L_JEU/2-142, Y_VIE - 12,L_JEU/2-142 + largeur_barre_xp, Y_VIE +8, fill='#9933FF')
        self.label_niveau_xp = self.canv.create_text(L_JEU/2-80, Y_VIE, text=f"Niveau : {self.joueur_courant.niveau}   xp : {self.joueur_courant.xp}", fill="green2", state=tk.DISABLED, font=('',-15,'bold'))
        #l'argent
        self.fichier_image_coin = Image.open('images\coins-game.png')
        self.fichier_image_coin_redim = self.fichier_image_coin.resize((20,20))
        self.image_coin = ImageTk.PhotoImage(self.fichier_image_coin_redim)
        self.canv.create_image(L_JEU/2+15, Y_VIE-2,anchor=tk.CENTER, image = self.image_coin)
        self.label_gold = self.canv.create_text(L_JEU/2+45, Y_VIE, text=f"{self.joueur_courant.golds}", fill="gold", state=tk.DISABLED, font=('',-15,'bold'))
        #missiles
        self.nb_missiles_restant = self.joueur_courant.missile_Q
        self.fichier_image_munitions = Image.open(r'images\bullets.png')
        self.fichier_image_munitions_redim = self.fichier_image_munitions.resize((20,20))
        self.image_munitions = ImageTk.PhotoImage(self.fichier_image_munitions_redim)
        self.canv.create_image(3*L_JEU/4-65, Y_VIE,anchor=tk.CENTER, image = self.image_munitions)
        self.label_munitions = self.canv.create_text(3*L_JEU/4-40, Y_VIE, text=f"{self.nb_missiles_restant}", fill="#D60093", state=tk.DISABLED, font=('',-15,'bold')) 
        #le score
        self.mult_flat = 1
        self.mult_bonus = 1
        self.le_score = 0
        self.label_points = self.canv.create_text(L_JEU - 90, Y_VIE, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}", fill="black", state=tk.DISABLED, font=('',-15,'bold')) 
        #le mode rebond
        self.no_bounce_nb = False
        self.no_bounce_sb = False
        #compteur bonus
        self.cpt_sb = 0
        self.cpt_sd = 0
        self.cpt_mult2 = 0
        self.cpt_mult5 = 0
        self.cpt_nb = 0
        #compteur missile
        self.cpt_missiles = 0
        #init service
        self.t_move = time.time()
        self.sens_raquette = 'gauche'
        #génération raquette
        self.x_raquette = int(L_JEU/2) - int(self.l_raquette/2)
        self.la_raquette_gauche = self.canv.create_oval(self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE, fill = COULEUR_BORDS_RAQUETTE, outline = COULEUR_BORDS_RAQUETTE, tags='raquette')
        self.la_raquette_droite = self.canv.create_oval(self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE, fill = COULEUR_BORDS_RAQUETTE,outline = COULEUR_BORDS_RAQUETTE, tags='raquette')
        self.la_raquette = self.canv.create_rectangle(self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE, fill = COULEUR_RAQUETTE, tags='raquette')           
        #génération balle
        self.couleur_balle = COULEUR_BALLE_DEFAUT
        self.liste_balles = []
        self.cpt_balles = 0
        self.balle0 = Balle(0,x = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2), y = Y_RAQUETTE - H_BALLE - 1)
        self.liste_balles.append(self.balle0)
        self.la_balle = self.canv.create_oval(self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE, fill = self.couleur_balle, tags='balle0')  
        tag_test = self.canv.gettags(self.la_balle) 
       
                      
    def nouvelle_manche(self):
        self.balle_servie = False
        #defreeze du boutton nouvelle partie
        self.bouton_lancer.configure(state=tk.NORMAL)
        #on supprime raquette et balle
        self.canv.delete('raquette')
        for boule in self.liste_balles :
            self.canv.delete(f"balle{boule.numero}")        
        #rebinding du service
        self.bind("<Up>",self.move)
        self.canv.bind("<Button-1>",self.move)
        #reset multiplicateur flat
        self.mult_flat = 1
        #génération raquette
        self.x_raquette = int(L_JEU/2) - int(self.l_raquette/2)
        self.la_raquette_gauche = self.canv.create_oval(self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE, fill = COULEUR_BORDS_RAQUETTE,outline = COULEUR_BORDS_RAQUETTE, tags='raquette')
        self.la_raquette_droite = self.canv.create_oval(self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE, fill = COULEUR_BORDS_RAQUETTE,outline = COULEUR_BORDS_RAQUETTE, tags='raquette')
        self.la_raquette = self.canv.create_rectangle(self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE, fill = COULEUR_RAQUETTE, tags='raquette')  
        #génération balle
        self.liste_balles = []
        self.cpt_balles = 0
        self.balle0 = Balle(0,x = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2), y = Y_RAQUETTE - H_BALLE - 1)
        self.liste_balles.append(self.balle0)
        self.la_balle = self.canv.create_oval(self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE, fill = self.couleur_balle, tags='balle0')     

    """Fonctions gèrent les evénements en jeu et lance des threads pour ne pas tout freezer
    
        - gen_monde, casse_une_brique, cree_et_lance_missile, pause
    """

    def gen_monde(self,indice_dico):
        
        #briques
        self.liste_briques = []
        if self.choix_mode.get() == "Histoire" :   
            le_dico_level = DICO_HISTOIRE
            if indice_dico >= len(DICO_HISTOIRE)-1:
                lindice = len(DICO_HISTOIRE)-1
            else : lindice = indice_dico
        elif self.choix_mode.get() == "Juju" :
            lindice = "FOUR"
            le_dico_level = DICO_PATTERNS
        #décor
        self.canv.delete('décor')
        self.fichier_image_fond = Image.open(self.dico_decor[lindice])
        self.fichier_image_fond_redim = self.fichier_image_fond.resize((L_JEU+DECALAGE,H_JEU+DECALAGE))
        self.image_fond = ImageTk.PhotoImage(self.fichier_image_fond_redim)
        self.canv.create_image(0,0,anchor=tk.NW, image = self.image_fond,tags = 'décor')
        if lindice != 0 :
            self.canv.tag_lower('décor', 'coeur')
        for pat in le_dico_level :
            if lindice == pat[0] :
                la_matrice = pat[1]
                la_correspondance = pat[2]
        for ligne in range(0,NB_LIGNE):
            for col in range(0,NB_COL) :
                indice = la_matrice[ligne][col]
                for truc in la_correspondance :
                    if truc[0] == indice :
                        la_couleur = truc[1]
                        la_position = [col,ligne]
                        la_brique = Brique(la_position , la_couleur,la_correspondance)
                        self.liste_briques += [la_brique]
        #affichage dans le canva
        for bri in self.liste_briques :
            x = DECALAGE + (bri.colonne * (L_BRIQUE + 2 * INTER_BRIQUE)) 
            y = DECALAGE + (bri.ligne * (H_BRIQUE + 2 * INTER_BRIQUE))
            letag = f"position{bri.colonne}:{bri.ligne}"
            self.canv.create_rectangle(x,y,x+L_BRIQUE,y+H_BRIQUE, fill = bri.couleur_brique, width = 2, tags=letag)
            if bri.powerup != 0 :
                for power in DICO_POWERUP :
                    if bri.powerup == power[0]:
                        le_texte = power[1]
                letagtext = f"positiontexte{bri.colonne}:{bri.ligne}"
                self.canv.create_text( x + L_BRIQUE/2, y + H_BRIQUE/2, text=le_texte, tags=letagtext, fill="red")
        #gère la musique des lvl
        pygame.mixer.Channel(0).stop()
        if self.musique_muet == False :
            musique = self.dico_musique[lindice]
            pygame.mixer.Channel(0).play(musique)
            
    def casse_une_brique(self,puissance,brique_touchee,balle=None):
        for bri in self.liste_briques :
            if bri.colonne == brique_touchee[0] and bri.ligne == brique_touchee[1] : #contact 
                self.mult_flat += 0.01 * min((puissance,bri.resistance+1))
            #modif brique lorsqu'elle est touchée
                if bri.resistance > puissance - 1 :
                    if self.sons_muet == False :
                        pygame.mixer.Sound.play(self.son_touche_brique)
                    bri.resistance -= puissance                           
                    nb_pplein = int(2*bri.resistance) + 1
                    nb_pvide = int(20 - bri.resistance)
                    le_dash = (nb_pplein,nb_pvide)
                    if bri.resistance == 3 :
                        le_stipple = 'gray75'
                    elif bri.resistance == 2 :
                        le_stipple = 'gray50'
                    elif bri.resistance == 1 :
                        le_stipple = 'gray25'
                    elif bri.resistance == 0 :
                        le_stipple = 'gray12'
                    else :
                        le_stipple = '' 
                    self.canv.itemconfigure(f"position{bri.colonne}:{bri.ligne}",dash = le_dash, dashoff=3, stipple=le_stipple)
                else : #destruction brique et powerup
                    if bri.powerup != 0 : #si il y a un powerup a la destruction
                        self.gen_powerup(bri.powerup,balle=balle)
                    elif self.sons_muet == False :
                        pygame.mixer.Sound.play(self.son_casse_brique)
                    #MAJ score, argent et xp
                    self.le_score += bri.v_point * self.mult_flat * self.mult_bonus                    
                    self.canv.itemconfigure(self.label_points, text=f"Score : {int(self.le_score):0>9d}")
                    self.joueur_courant.golds += bri.v_golds
                    self.canv.itemconfigure(self.label_gold, text=f"{self.joueur_courant.golds}")
                    ancien_niveau = self.joueur_courant.niveau
                    self.joueur_courant.maj_xp(bri.v_xp)
                    largeur_barre_xp = int(self.joueur_courant.xp / (self.joueur_courant.xp + self.joueur_courant.xp_avant_lvlup) * 124)
                    self.canv.coords(self.barre_xp,L_JEU/2-142, Y_VIE - 12,L_JEU/2-142 + largeur_barre_xp, Y_VIE +8)                    
                    if self.joueur_courant.niveau - ancien_niveau > 0 :
                        if self.sons_muet == False :
                            pygame.mixer.Sound.play(self.son_lvlup)
                        self.label_upgrades.config(text=f"Upgrades : {self.joueur_courant.points_upgrades} point(s) disponible(s)")
                    self.canv.itemconfigure(self.label_niveau_xp, text=f"Niveau : {self.joueur_courant.niveau} xp : {self.joueur_courant.xp}")
                    self.canv.delete(f"position{bri.colonne}:{bri.ligne}")
                    self.canv.delete(f"positiontexte{bri.colonne}:{bri.ligne}")
                    self.liste_briques.remove(bri)
                    #regen des briques
                    if self.liste_briques == []:
                        self.balle_servie = False
                        self.level_courant += 1
                        self.gen_monde(self.level_courant)
                        self.nouvelle_manche()
        
    def prout(self,event):
        print("PROUT !!!!!!!")
        pygame.mixer.Sound.play(self.son_lolilol)
        
    def cree_et_lance_missile(self,event):
        modele_missile = self.modele_missiles
        puissance_missile = self.puissance_missiles
        #fonction missile lancée par des threads
        def tir_missile(self,le_missile):
            x_missile = self.x_raquette + self.l_raquette/2
            colonne_missile = int((x_missile - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
            y_missile = Y_RAQUETTE
            liste_dessins_missile =[]
            if modele_missile == 1 :
                if self.sons_muet == False :
                    pygame.mixer.Sound.play(self.son_lance_missile1)
                le_son_boum = self.son_explo_missile1
                liste_dessins_missile.append(self.canv.create_rectangle(x_missile-le_missile.longueur/2,y_missile,x_missile +le_missile.longueur/2,y_missile + le_missile.hauteur, fill = le_missile.couleur, tags=f"missile{le_missile.tag}"))
            elif modele_missile == 2 :
                if self.sons_muet == False :
                    pygame.mixer.Sound.play(self.son_lance_missile2)
                le_son_boum = self.son_explo_missile2              
                liste_dessins_missile.append(self.canv.create_oval(x_missile - le_missile.longueur/2, y_missile - le_missile.longueur/2 , x_missile + le_missile.longueur/2, y_missile + le_missile.longueur/2, fill = le_missile.couleur2, tags=f"missile{le_missile.tag}"))
                liste_dessins_missile.append(self.canv.create_rectangle(x_missile-le_missile.longueur/2,y_missile,x_missile +le_missile.longueur/2,y_missile + le_missile.hauteur, fill = le_missile.couleur, tags=f"missile{le_missile.tag}"))
            elif modele_missile == 3:
                if self.sons_muet == False :
                    pygame.mixer.Sound.play(self.son_lance_missile3)
                le_son_boum = self.son_explo_missile3
                liste_dessins_missile.append(self.canv.create_oval(x_missile-le_missile.longueur/2,y_missile,x_missile +le_missile.longueur/2,y_missile + le_missile.hauteur, fill = le_missile.couleur, tags=f"missile{le_missile.tag}"))
            elif modele_missile == 4 : 
                if self.sons_muet == False :
                    pygame.mixer.Sound.play(self.son_lance_missile3)
                le_son_boum = self.son_explo_missile3                
                liste_dessins_missile.append(self.canv.create_rectangle(x_missile-le_missile.longueur/2-2,y_missile-2,x_missile +le_missile.longueur/2+2,y_missile + le_missile.hauteur+2, fill = le_missile.couleur2, tags=f"missile{le_missile.tag}"))
                liste_dessins_missile.append(self.canv.create_oval(x_missile-le_missile.longueur/2,y_missile,x_missile +le_missile.longueur/2,y_missile + le_missile.hauteur, fill = le_missile.couleur, tags=f"missile{le_missile.tag}"))
            touche = False
            while touche == False :
                time.sleep(DELTA_T_SEC)
                if self.en_pause ==False :
                    y_missile -= le_missile.vitesse
                    ligne_missile = int((y_missile - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                    tag_missile = (f"position{colonne_missile}:{ligne_missile}")
                    if self.canv.find_withtag(tag_missile) == ():
                        for dessin in liste_dessins_missile :
                            ancienne_coordonnees = self.canv.coords(dessin)
                            nouvelle_coordonnees = (ancienne_coordonnees[0],ancienne_coordonnees[1] - le_missile.vitesse,ancienne_coordonnees[2],ancienne_coordonnees[3] - le_missile.vitesse)
                            self.canv.coords(dessin,nouvelle_coordonnees)
                            if len(liste_dessins_missile) > 1 :
                                if self.canv.itemcget(dessin,'fill') == le_missile.couleur :
                                    self.canv.itemconfigure(dessin,fill = le_missile.couleur2 )
                                else :
                                    self.canv.itemconfigure(dessin,fill = le_missile.couleur )
                    else:
                        self.canv.delete(f"missile{le_missile.tag}")
                        if modele_missile == 1 or modele_missile == 2 or modele_missile == 3 :
                            if self.sons_muet == False :
                                pygame.mixer.Sound.play(le_son_boum)
                            for truc in le_missile.briques_impactes :
                                la_puissance = truc[0]
                                loffset_colonne = truc[1][0]
                                loffset_ligne = truc[1][1]
                                self.casse_une_brique(la_puissance,[colonne_missile + loffset_colonne, ligne_missile + loffset_ligne])
                        elif modele_missile == 4 :
                            for sequence in self.projectile_type.briques_impactes_sequence :
                                if self.sons_muet == False :
                                    pygame.mixer.Sound.play(le_son_boum)
                                for truc in sequence :
                                    la_puissance = truc[0]
                                    loffset_colonne = truc[1][0]
                                    loffset_ligne = truc[1][1]
                                    self.casse_une_brique(la_puissance,[colonne_missile + loffset_colonne, ligne_missile + loffset_ligne])
                                time.sleep(0.5)
                        touche = True
                    if y_missile <= DECALAGE : #missile au plafond
                        self.canv.delete(f"missile{le_missile.tag}")
                        touche = True           
        #test du nombre de missile et lancement du missile
        self.cpt_missiles += 1
        if self.nb_missiles_restant == 0 :
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_plus_missile)
        else :
            self.nb_missiles_restant -= 1
            self.canv.itemconfigure(self.label_munitions, text=f"{self.nb_missiles_restant}") 
            un_missile = Projectile(modele_missile,puissance_missile,self.cpt_missiles)
            self.thread_missile = th.Thread(target=tir_missile,args=(self,un_missile))
            self.thread_missile.start()
    
    def pause(self,event):
        self.thread_pause = th.Thread(target=self.vrai_pause)
        self.thread_pause.start()
        
    def vrai_pause(self):
        self.en_pause = not self.en_pause
        if self.en_pause :
            self.canv.create_text(L_JEU/2, H_JEU/2+30,anchor=tk.CENTER, text="            JEU EN PAUSE\nESPACE POUR REPRENDRE", fill="black", state=tk.DISABLED, font=('',-40,'bold'),tags='pause')
            print("jeu en pause")
        else :
            if self.balle_servie :
                self.move()
            self.canv.delete('pause')
            print("reprise du jeu")

    """Fonctions gèrent les powerup en jeu et lance des threads pour ne pas tout freezer """
     
    def gen_powerup(self,le_powerup,balle=None):
        #Codes des différents power-up
        if le_powerup == "live_up":
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_liveup)
            self.pt_vie += NB_VIE_SUP
            self.canv.itemconfigure(self.label_vie, text=f"{self.pt_vie}")
        elif le_powerup == "speed_down":
            self.cpt_sd += 1
            le_nom = f"SD_{self.cpt_sd}"
            self.thread_speed_down = th.Thread(name=le_nom,target=self.speed_down,args=(self.cpt_sd,))
            self.liste_threads_sd.append(self.thread_speed_down)
            self.thread_speed_down.start()
        elif le_powerup == "super_bonus":
            pygame.mixer.Sound.stop(self.son_powerup_superbonus)
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_superbonus,maxtime=DUREE_SB*1000)
            self.cpt_sb += 1
            le_nom = f"SB_{self.cpt_sb}"
            self.thread_super_bonus = th.Thread(name=le_nom,target=self.super_bonus,args=(self.cpt_sb,))
            self.liste_threads_sb.append(self.thread_super_bonus)
            self.thread_super_bonus.start()
        elif le_powerup == "pplus":
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_pplus)
            self.puissance_balle += PUISSANCE_PPLUS
        elif le_powerup == "multiplicateur2" :
            pygame.mixer.Sound.stop(self.son_powerup_mult2)
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_mult2,maxtime=DUREE_MULT2*1000)
            self.cpt_mult2 += 1
            le_nom = f"mult2_{self.cpt_mult2}"
            self.thread_mult2 = th.Thread(name=le_nom,target=self.mult2,args=(self.cpt_mult2,))
            self.liste_threads_mult2.append(self.thread_mult2)
            self.thread_mult2.start()
        elif le_powerup == "multiplicateur5" :    
            self.cpt_mult5 += 1
            le_nom = f"mult5_{self.cpt_mult5}"
            self.thread_mult5 = th.Thread(name=le_nom,target=self.mult5,args=(self.cpt_mult5,))
            self.liste_threads_mult5.append(self.thread_mult5)
            self.thread_mult5.start()
        elif le_powerup == "no_bounce" :
            pygame.mixer.Sound.stop(self.son_powerup_nobounce)
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_nobounce,maxtime=DUREE_NB*1000)
            self.cpt_nb += 1
            le_nom = f"NB_{self.cpt_nb}"
            self.thread_bounce = th.Thread(name=le_nom,target=self.no_bounceur,args=(self.cpt_nb,))
            self.liste_threads_nb.append(self.thread_bounce)
            self.thread_bounce.start()
        elif le_powerup == "multiballe":
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_powerup_pplus)
            for i in range(0,NB_BALLES_SUP):
                self.cpt_balles += 1
                nouvel_angle = math.fmod(balle.angle_balle + (i+1) * 2 * math.pi / (1 + NB_BALLES_SUP), 2 * math.pi)              
                if abs(math.sin(nouvel_angle)) < 1/2 :
                    if math.sin(nouvel_angle) >= 0 :
                        nouvel_angle = math.pi/6
                    elif math.sin(nouvel_angle) < 0 :
                        nouvel_angle = -1 * math.pi/6
                une_balle = Balle(self.cpt_balles,x=balle.x_balle,y=balle.y_balle,angle=nouvel_angle,ancienne_ligne=balle.ancienne_ligne,ancienne_colonne=balle.ancienne_colonne)
                son_tag = f"balle{une_balle.numero}"
                self.canv.create_oval(une_balle.x_balle,une_balle.y_balle,une_balle.x_balle+L_BALLE,une_balle.y_balle+H_BALLE, fill = self.couleur_balle, tags=son_tag)
                self.liste_balles.append(une_balle)
          
    #définition des toutes les fonctions powerup appelées par des threads différents

    def speed_down(self,numero):
        self.vitesse_balle *= RATIO_SD
        self.couleur_balle = COULEUR_SD
        time.sleep(DUREE_SD)
        for thr in self.liste_threads_sd: #on parcours tous les threads sd
            if thr.is_alive() and thr.name != f"SB_{numero}" :   #test s'il existe un autre actif on reste avec la bonne couleur
                pass
            else :
                self.couleur_balle = COULEUR_BALLE_DEFAUT #ce qui ne doit pas être modifié si un autre thread sd encore en cours
        self.vitesse_balle /= RATIO_SD #ce doit être modifié dans tous les cas

    def mult2(self,numero):
        self.mult_bonus *= 2
        self.couleur_balle = COULEUR_MULT2
        time.sleep(DUREE_MULT2)
        for thr in self.liste_threads_mult2: #on parcours tous les threads du même bonus
            if thr.is_alive() and thr.name != f"mult2_{numero}" :   #test s'il existe un autre actif
                pass
            else :
                self.couleur_balle = COULEUR_BALLE_DEFAUT #ce qui ne doit pas être modifié si un autre thread encore en cours
        self.mult_bonus *= 1/2 #ce doit être modifié dans tous les cas
        
    def mult5(self,numero):
        self.mult_bonus *= 5
        self.couleur_balle = COULEUR_MULT5
        time.sleep(DUREE_MULT5)
        for thr in self.liste_threads_mult5: #on parcours tous les threads du même bonus
            if thr.is_alive() and thr.name != f"mult5_{numero}" :   #test s'il existe un autre actif
                pass
            else :
                self.couleur_balle = COULEUR_BALLE_DEFAUT #ce qui ne doit pas être modifié si un autre thread encore en cours
        self.mult_bonus *= 1/5 #ce doit être modifié dans tous les cas
        
    def no_bounceur(self,numero):
        self.no_bounce_nb = True
        self.couleur_balle = COULEUR_NB
        time.sleep(DUREE_NB)
        for thr in self.liste_threads_nb: #on parcours tous les threads du même bonus
            if thr.is_alive() and thr.name != f"NB_{numero}" :   #test s'il existe un autre actif
                pass
            else :
                self.couleur_balle = COULEUR_BALLE_DEFAUT #ce qui ne doit pas être modifié si un autre thread encore en cours
                self.no_bounce_nb = False        

    def super_bonus(self,numero):
        self.no_bounce_sb = NO_BOUNCE_MODE
        self.puissance_bonus += PUISSANCE_SB
        self.couleur_balle = COULEUR_SB
        time.sleep(DUREE_SB)
        for thr in self.liste_threads_sb: #on parcours tous les threads sb
            if thr.is_alive() and thr.name != f"SB_{numero}" :   #s'il existe un autre actif on reste en no bounce et avec la bonne couleur
                pass
            else :
                self.no_bounce_sb = False
                self.couleur_balle = COULEUR_BALLE_DEFAUT
        self.puissance_bonus -= PUISSANCE_SB                 
     

    
    """Fonctions principale
    
        - gère la balle et ses conséquence (cassage brique, gain de points, etc)
        - gère le service au début
        - on passe en balle_servie = True quand elle est appelé (uniquement par le service)
    """
    
    def move(self,event=None):
        """Déplace la baballe (appelée itérativement avec la méthode after)."""
        if self.en_pause == False :
            #on passe in game
            if event != None : #si move appelée par le service (clic ou flèche du haut)
                #test orientation service
                delta_t = time.time() - self.t_move          
                if delta_t < 0.0001 :  #service rapide
                    angle_service = 5*math.pi/6
                elif delta_t < 0.005 :  #service moyen
                    angle_service = 3*math.pi/4
                elif delta_t < 0.1 :  #service lent
                    angle_service = 2*math.pi/3
                else :  #service plat
                    angle_service = math.pi/2 + 0.001
                if self.sens_raquette == 'droite' :
                    self.balle0.angle_balle = math.pi - angle_service
                elif self.sens_raquette == 'gauche' :
                    self.balle0.angle_balle = angle_service
                self.balle_servie = True
                if self.sons_muet == False :
                    pygame.mixer.Sound.play(self.son_service)
                #Unbind du service pour mettre sur missiles
                self.bind("<Up>",self.cree_et_lance_missile)
                self.canv.bind("<Button-1>",self.cree_et_lance_missile)
            #freeze du menu
                for child in self.cadre_mode.winfo_children():
                    child.configure(state=tk.DISABLED)
                self.bouton_choix_profil.configure(state=tk.DISABLED)
                self.bouton_lancer.configure(state=tk.DISABLED)
            #calcul du mode rebond sur cette itération
            self.no_bounce = self.no_bounce_nb or self.no_bounce_sb
            #Début des tests pour gérer les rebonds
            for balle in self.liste_balles :                
                #tests murs
                #mur droit et direction droite
                if ((balle.x_balle + L_BALLE) >= L_JEU + DECALAGE) and (math.cos(balle.angle_balle) > 0) :
                        balle.angle_balle = math.fmod(math.pi - balle.angle_balle, 2 * math.pi)
                        if self.sons_muet == False :
                            pygame.mixer.Sound.play(self.son_mur)
                #mur gauche et balle vers la gauche
                if (balle.x_balle <= DECALAGE) and (math.cos(balle.angle_balle) < 0) :
                        balle.angle_balle = math.fmod(math.pi - balle.angle_balle, 2 * math.pi)
                        if self.sons_muet == False :
                            pygame.mixer.Sound.play(self.son_mur)
                #plafond
                if balle.y_balle <= DECALAGE :
                    balle.angle_balle *= -1 
                    if self.sons_muet == False :
                        pygame.mixer.Sound.play(self.son_mur)   
                    
                #ZONE DES BRIQUES !!!
                if balle.y_balle <= (DECALAGE + (NB_LIGNE * (H_BRIQUE + 2 * INTER_BRIQUE))):
                    #test pour connaitre la direction et définir le point "en avant" de la balle
                    if math.cos(balle.angle_balle) > 0 and math.sin(balle.angle_balle) > 0 :
                        # haut droite
                        colonne_balle = int((balle.x_balle + L_BALLE - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
                        ligne_balle = int((balle.y_balle - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                    elif math.cos(balle.angle_balle) < 0 and math.sin(balle.angle_balle) > 0 :
                        #haut gauche
                        colonne_balle = int((balle.x_balle - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
                        ligne_balle = int((balle.y_balle - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                    elif math.cos(balle.angle_balle) < 0 and math.sin(balle.angle_balle) < 0 :
                        #bas gauche
                        colonne_balle = int((balle.x_balle - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
                        ligne_balle = int((balle.y_balle + H_BALLE - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                    elif math.cos(balle.angle_balle) > 0 and math.sin(balle.angle_balle) < 0 :
                        #bas droite
                        colonne_balle = int((balle.x_balle + L_BALLE - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
                        ligne_balle = int((balle.y_balle + H_BALLE - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                    tag_balle = (f"position{colonne_balle}:{ligne_balle}")
                    brique_touche = []
                    if self.canv.find_withtag(tag_balle) != ():
                        if balle.ancienne_colonne == colonne_balle : # contact par le haut ou par le bas                             
                            angle_provisoire_balle = -1*balle.angle_balle
                            brique_touche += [[colonne_balle,ligne_balle]]
                        elif balle.ancienne_ligne == ligne_balle : #contact par la gauche ou droite
                            angle_provisoire_balle = math.fmod(math.pi - balle.angle_balle, 2*math.pi)
                            brique_touche += [[colonne_balle,ligne_balle]]
                        elif balle.ancienne_colonne < colonne_balle and balle.ancienne_ligne < ligne_balle :
                            #on vient de Haut gauche
                            tag_a_chercher1 = f"position{colonne_balle-1}:{ligne_balle}" #tag de la brique de gauche pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle-1}" #tag de la brique de dessus pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                angle_provisoire_balle = math.fmod(math.pi - balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle,ligne_balle]]
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                angle_provisoire_balle = -1*balle.angle_balle
                                brique_touche += [[colonne_balle,ligne_balle]]
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle-1,ligne_balle],[colonne_balle,ligne_balle-1]]
                        elif balle.ancienne_colonne < colonne_balle and balle.ancienne_ligne > ligne_balle :
                            #on vient de Bas gauche
                            tag_a_chercher1 = f"position{colonne_balle-1}:{ligne_balle}" #tag de la brique de gauche pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle+1}" #tag de la brique de dessous pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                angle_provisoire_balle = math.fmod(math.pi - balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle,ligne_balle]]
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                angle_provisoire_balle = -1*balle.angle_balle
                                brique_touche += [[colonne_balle,ligne_balle]]
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle-1,ligne_balle],[colonne_balle,ligne_balle+1]]
                        elif balle.ancienne_colonne > colonne_balle and balle.ancienne_ligne > ligne_balle :
                            #on vient de Bas droite
                            tag_a_chercher1 = f"position{colonne_balle+1}:{ligne_balle}" #tag de la brique de droite pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle+1}" #tag de la brique de dessous pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                angle_provisoire_balle = math.fmod(math.pi - balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle,ligne_balle]]
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                angle_provisoire_balle = -1*balle.angle_balle
                                brique_touche += [[colonne_balle,ligne_balle]]
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle+1,ligne_balle],[colonne_balle,ligne_balle+1]]
                        elif balle.ancienne_colonne > colonne_balle and balle.ancienne_ligne < ligne_balle :
                            #on vient de haut droite
                            tag_a_chercher1 = f"position{colonne_balle+1}:{ligne_balle}" #tag de la brique de droite pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle-1}" #tag de la brique de dessus pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                angle_provisoire_balle = math.fmod(math.pi - balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle,ligne_balle]]
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                angle_provisoire_balle = -1*balle.angle_balle
                                brique_touche += [[colonne_balle,ligne_balle]]
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle+1,ligne_balle],[colonne_balle,ligne_balle-1]]
                    #cas du traverssage de diagonale            
                    else:                                      
                        if balle.ancienne_colonne < colonne_balle and balle.ancienne_ligne < ligne_balle :
                            #on vient de Haut gauche
                            tag_a_chercher1 = f"position{colonne_balle-1}:{ligne_balle}" #tag de la brique de gauche pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle-1}" #tag de la brique de dessus pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                pass
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                pass
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle-1,ligne_balle],[colonne_balle,ligne_balle-1]]
                        elif balle.ancienne_colonne < colonne_balle and balle.ancienne_ligne > ligne_balle :
                            #on vient de Bas gauche
                            tag_a_chercher1 = f"position{colonne_balle-1}:{ligne_balle}" #tag de la brique de gauche pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle+1}" #tag de la brique de dessous pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                pass
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                pass
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle-1,ligne_balle],[colonne_balle,ligne_balle+1]]
                        elif balle.ancienne_colonne > colonne_balle and balle.ancienne_ligne > ligne_balle :
                            #on vient de Bas droite
                            tag_a_chercher1 = f"position{colonne_balle+1}:{ligne_balle}" #tag de la brique de droite pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle+1}" #tag de la brique de dessous pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                pass
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                pass
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle+1,ligne_balle],[colonne_balle,ligne_balle+1]]
                        elif balle.ancienne_colonne > colonne_balle and balle.ancienne_ligne < ligne_balle :
                            #on vient de haut droite
                            tag_a_chercher1 = f"position{colonne_balle+1}:{ligne_balle}" #tag de la brique de droite pour voir si elle existe
                            tag_a_chercher2 = f"position{colonne_balle}:{ligne_balle-1}" #tag de la brique de dessus pour voir si elle existe
                            if self.canv.find_withtag(tag_a_chercher1) == ():
                                pass
                            elif self.canv.find_withtag(tag_a_chercher2) == ():
                                pass
                            else :
                                angle_provisoire_balle = math.fmod(math.pi + balle.angle_balle, 2*math.pi)
                                brique_touche += [[colonne_balle+1,ligne_balle],[colonne_balle,ligne_balle-1]]
                    for bri in self.liste_briques :
                        for bri_touche in brique_touche :
                            if bri.colonne == bri_touche[0] and bri.ligne == bri_touche[1] : #contact 
                                # self.mult_flat += 0.01 * min((self.puissance_balle + self.puissance_bonus,bri.resistance+1))
                                if bri.resistance < (self.puissance_balle + self.puissance_bonus) and self.no_bounce : #si résistance brique < puissance balle et mode no bounce => pas de rebond
                                    pass
                                else :
                                    balle.angle_balle = angle_provisoire_balle         
                    #modif brique lorsqu'elle est touchée
                    for bri_touche in brique_touche :
                        self.casse_une_brique(self.puissance_balle + self.puissance_bonus,bri_touche,balle=balle) 
                if self.balle_servie == True :
                    #zone raquette et pas encore raté
                    if (balle.y_balle + H_BALLE) >= Y_RAQUETTE and (math.sin(balle.angle_balle) < 0) and balle.zut == False :
                        #test endroit touché (gauche, centre ou droit)
                        if   self.x_raquette - self.l_bords_raquette - L_BALLE/2 <= balle.x_balle + L_BALLE/2 < self.x_raquette - 2/3*self.l_bords_raquette - L_BALLE/2 : #touché a extreme gauche
                            angle_provisoire = math.fmod(- 2 * ANGLE_BORD + balle.angle_balle, 2*math.pi)
                        elif self.x_raquette - 2/3*self.l_bords_raquette - L_BALLE/2 <=  balle.x_balle + L_BALLE/2 < self.x_raquette : #touché a gauche
                            angle_provisoire = math.fmod(-2 * math.asin((balle.x_balle + L_BALLE/2 - self.x_raquette)/(self.l_bords_raquette+ L_BALLE/2)) - balle.angle_balle, 2*math.pi)
                        elif self.x_raquette <= balle.x_balle + L_BALLE/2 <= self.x_raquette + self.l_raquette : #touché au centre
                            angle_provisoire = -1*balle.angle_balle
                        elif self.x_raquette + self.l_raquette < balle.x_balle + L_BALLE/2 <= self.x_raquette + self.l_raquette + 2/3*self.l_bords_raquette + L_BALLE/2 : #touché a droite
                            angle_provisoire = math.fmod(-2 * math.asin((balle.x_balle + L_BALLE/2 - self.x_raquette - self.l_raquette)/(self.l_bords_raquette+ L_BALLE/2)) - balle.angle_balle,2*math.pi)
                        elif self.x_raquette + self.l_raquette + 2/3*self.l_bords_raquette + L_BALLE/2  < balle.x_balle + L_BALLE/2 <= self.x_raquette + self.l_raquette + self.l_bords_raquette + L_BALLE/2 : #touché a extreme droite
                            angle_provisoire = math.fmod(-2 * ANGLE_BORD - balle.angle_balle,2*math.pi)
                        else :
                            balle.zut = True
                        #si on a touché avec la raquette
                        if balle.zut == False :
                            if -11*math.pi/6 <= angle_provisoire <= -7*math.pi/6 or math.pi/6 <= angle_provisoire <= 5*math.pi/6 : #si dans la fourchette 5Pi/6 <=> Pi/6, on assigne le résultat du calcul
                                balle.angle_balle = angle_provisoire
                            else : # sinon on test si on va a droite ou a gauche et on bloque a pi/6 ou 5pi/6
                                if math.cos(angle_provisoire) >= 0 :
                                    balle.angle_balle = math.pi/6
                                else :
                                    balle.angle_balle = 5*math.pi/6
                            if self.sons_muet == False :
                                pygame.mixer.Sound.play(self.son_raquette)
                    #La mort
                    if balle.y_balle >= H_JEU + 2 * DECALAGE :
                        self.liste_balles.remove(balle)
                        self.canv.delete(f"balle{balle.numero}")
                        if not self.liste_balles :
                            if self.pt_vie == 0 :
                                self.fin_partie()
                            else :
                                if self.sons_muet == False :
                                    pygame.mixer.Sound.play(self.son_mort)
                                #on perd une vie
                                self.pt_vie -= 1
                                self.canv.itemconfigure(self.label_vie, text=f"{self.pt_vie}")
                                #on perd 1 de puissance flat si puissance flat >=2
                                # if self.puissance_balle >= 2 :
                                    # self.puissance_balle -= 1
                                    # self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}")
                                self.nouvelle_manche()
                    else :
                        #fin des tests, assignation nouveau x et y, stockage des anciens pour savoir d'où on vient
                        balle.ancienne_ligne = int((balle.y_balle - DECALAGE)/(H_BRIQUE + 2 * INTER_BRIQUE))
                        balle.ancienne_colonne = int((balle.x_balle - DECALAGE)/(L_BRIQUE + 2 * INTER_BRIQUE))
                        # Mise à jour des coord balle et des labels jeux si tjs in game
                        if self.balle_servie == True :
                            balle.x_balle = balle.x_balle + self.vitesse_balle * math.cos(balle.angle_balle)
                            balle.y_balle = balle.y_balle - self.vitesse_balle * math.sin(balle.angle_balle) 
                            self.canv.coords(f"balle{balle.numero}", balle.x_balle,balle.y_balle,balle.x_balle+L_BALLE,balle.y_balle+H_BALLE) 
                            self.canv.itemconfigure(f"balle{balle.numero}", fill=self.couleur_balle)
                            self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}") 
                            self.canv.itemconfigure(self.label_points, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}") 
            if self.balle_servie == True :
                # Rappel de move toutes les pas de temps.
                self.after(DELTA_T, self.move)

    """Fonctions qui gère les évènements de fin de partie     """

    def fin_partie(self, event=None):
        self.balle_servie = False
        #coupe la musique
        pygame.mixer.Sound.stop(self.musique_lvl0)
        #sauvegarde du profil
        self.save_profils()
        #fenêtre de fin
        fenetre_fin = tk.Toplevel(self)
        fenetre_fin.geometry(f"{int(L_JEU/2)}x{int(H_JEU/4)}+{int(L_JEU/3)}+{int(H_JEU/2)}")
        fenetre_fin.resizable(width=False, height=False)
        fenetre_fin.title("Fin de partie")
        def fermeture():
            pygame.mixer.Sound.stop(self.son_partie_gagnee)
            fenetre_fin.destroy()
            self.nouvelle_partie()
        if self.set_highscore():
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_partie_gagnee,loops=-1)             
            la_phrase = f"Félicitations !! Nouveaux record : {int(self.le_score)}"
        else :
            if self.sons_muet == False :
                pygame.mixer.Sound.play(self.son_partie_perdue)
            la_phrase = f"Fin de partie ! Votre score : {int(self.le_score)}"
        label_fin = tk.Label(fenetre_fin, text=la_phrase)
        label_fin.place(x=int(L_JEU/4),y=int(H_JEU/8-20),anchor=tk.CENTER)
        bouton_fin = tk.Button(fenetre_fin, text="Super !",command=fermeture)
        bouton_fin.place(x=int(L_JEU/4),y=int(H_JEU/8+10),anchor=tk.CENTER)
        fenetre_fin.protocol("WM_DELETE_WINDOW", fermeture)                       
         
    """Fonctions gèrent les déplacement de la raquette souris ou clavier     """
                            
    def pointeur(self,event):
        self.x_souris = event.x + event.widget.winfo_rootx()

    
    def mouvement_souris(self,event):
        if self.en_pause == False :
            self.x_souris = event.x + event.widget.winfo_rootx()
            self.bind("<Motion>",self.pointeur)
            if self.x_raquette + self.canv.winfo_rootx() <= event.x + event.widget.winfo_rootx() :
                self.thread_raquette_droite = th.Thread(target=self.raquette_droite,daemon=True)
                self.liste_threads_souris.append(self.thread_raquette_droite)
                self.thread_raquette_droite.start()
            elif self.x_raquette + self.canv.winfo_rootx() > event.x + event.widget.winfo_rootx() :
                self.thread_raquette_gauche = th.Thread(target=self.raquette_gauche,daemon=True)
                self.liste_threads_souris.append(self.thread_raquette_gauche)
                self.thread_raquette_gauche.start()
             
    def raquette_droite(self):
            while self.arrete_souris == False and self.en_pause == False and self.x_souris-(self.x_raquette + self.canv.winfo_rootx()) > DEADZONE_SOURIS/2 :
                if (self.x_raquette + self.l_raquette) <= L_JEU - 2 :
                    self.x_raquette += VITESSE_RAQUETTE_SOURIS
                    self.canv.coords(self.la_raquette_gauche,self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE)
                    self.canv.coords(self.la_raquette_droite,self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE)
                    self.canv.coords(self.la_raquette, self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE)
                    if self.balle_servie == False : #Mise à jour des coord balle et des labels jeux
                        self.sens_raquette = 'droite'
                        self.t_move = time.time()
                        self.balle0.x_balle = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2)
                        self.canv.coords(self.la_balle, self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE)
                        self.canv.itemconfigure(self.la_balle, fill=self.couleur_balle)
                        self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}") 
                        self.canv.itemconfigure(self.label_points, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}") 
                time.sleep(self.rapidite_raquette)
            if self.arrete_souris == False :
                self.bind("<Motion>",self.mouvement_souris) 

        
    def raquette_gauche(self):
            while self.arrete_souris == False and self.en_pause == False and self.x_souris-(self.x_raquette + self.canv.winfo_rootx()) < DEADZONE_SOURIS/2 :
                if self.x_raquette > DECALAGE :
                    self.x_raquette -= VITESSE_RAQUETTE_SOURIS
                    self.canv.coords(self.la_raquette_gauche,self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE)
                    self.canv.coords(self.la_raquette_droite,self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE)
                    self.canv.coords(self.la_raquette, self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE)
                    if self.balle_servie == False : #Mise à jour des coord balle et des labels jeux
                        self.sens_raquette = 'gauche'
                        self.t_move = time.time()
                        self.balle0.x_balle = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2)
                        self.canv.coords(self.la_balle, self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE)
                        self.canv.itemconfigure(self.la_balle, fill=self.couleur_balle) 
                        self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}") 
                        self.canv.itemconfigure(self.label_points, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}") 
                time.sleep(self.rapidite_raquette)
            if self.arrete_souris == False :
                self.bind("<Motion>",self.mouvement_souris) 
  

    def raquette_droite_clavier(self,event):
        if self.en_pause == False :
            if (self.x_raquette + self.l_raquette) <= L_JEU - 2 :
                self.x_raquette += self.rapidite_raquette_clavier
                self.canv.coords(self.la_raquette_gauche,self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE)
                self.canv.coords(self.la_raquette_droite,self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE)
                self.canv.coords(self.la_raquette, self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE)
                if self.balle_servie == False : #Mise à jour des coord balle et des labels jeux
                    self.sens_raquette = 'droite'
                    self.t_move = time.time()
                    self.balle0.x_balle = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2)
                    self.canv.coords(self.la_balle, self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE)
                    self.canv.itemconfigure(self.la_balle, fill=self.couleur_balle)
                    self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}") 
                    self.canv.itemconfigure(self.label_points, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}") 
        
    def raquette_gauche_clavier(self,event):
        if self.en_pause == False :
            if self.x_raquette > DECALAGE :
                self.x_raquette -= self.rapidite_raquette_clavier
                self.canv.coords(self.la_raquette_gauche,self.x_raquette - self.l_bords_raquette,Y_RAQUETTE ,self.x_raquette + self.l_bords_raquette,Y_RAQUETTE + H_RAQUETTE)
                self.canv.coords(self.la_raquette_droite,self.x_raquette + self.l_raquette - self.l_bords_raquette ,Y_RAQUETTE , self.x_raquette + self.l_raquette + self.l_bords_raquette, Y_RAQUETTE + H_RAQUETTE)
                self.canv.coords(self.la_raquette, self.x_raquette,Y_RAQUETTE,self.x_raquette+self.l_raquette,Y_RAQUETTE+H_RAQUETTE)
                if self.balle_servie == False :
                    self.sens_raquette = 'gauche'
                    self.t_move = time.time()
                    self.balle0.x_balle = self.x_raquette + int(self.l_raquette/2) - (L_BALLE/2)
                    self.canv.coords(self.la_balle, self.balle0.x_balle,self.balle0.y_balle,self.balle0.x_balle+L_BALLE,self.balle0.y_balle+H_BALLE)
                    self.canv.itemconfigure(self.la_balle, fill=self.couleur_balle) 
                    self.canv.itemconfigure(self.label_puissance, text=f"Puissance : {self.puissance_balle + self.puissance_bonus}") 
                    self.canv.itemconfigure(self.label_points, text=f"Score (x{self.mult_flat*self.mult_bonus:.2f}) : {int(self.le_score):0>7d}")    
     
    """Fonctions gèrent les fichiers externe
    
        - get_highscore
        - set_highscore
        - get_profils
        - set_profils (gère aussi la création de nouveaux joueurs)
    """
     
    def get_highscore(self):
        try :
            filin = open('highscores.txt', 'r')
            seq = filin.readlines()
            del seq[0]
            joueur_papa = (seq[0].split("\t\t"))[1]
            score_papa = int((seq[0].split("\t\t"))[2])
            joueur_infini = (seq[1].split("\t\t"))[1]
            score_infini = int((seq[1].split("\t\t"))[2])
            joueur_juju = (seq[2].split("\t\t"))[1]
            score_juju = int((seq[2].split("\t\t"))[2])
            filin.close()
        except FileNotFoundError :
            joueur_papa = " "
            score_papa = 0
            joueur_infini = " "
            score_infini = 0
            joueur_juju = " "
            score_juju = 0
        self.label_record_papa.config  (text=f"Mode Histoire : {score_papa:>07d} par {joueur_papa:<10s}")
        self.label_record_infini.config(text=f"Mode Infini :  {score_infini:>07d} par {joueur_infini:<10s}")
        self.label_record_juju.config  (text=f"Mode Juju :   {score_juju:>07d} par {joueur_juju:<10s}")
            
    def set_highscore(self):
        try :
            filout = open('highscores.txt', 'r')
            seq = filout.readlines()
            filout.close()
        except FileNotFoundError :
            seq=['Mode\t\tJoueur\t\tScore\n', 'Histoire\t\tPersonne\t\t0\n', 'Infini\t\tPersonne\t\t0\n', 'Juju\t\tPersonne\t\t0\n']
        if self.choix_mode.get() == "Histoire" :
            indice = 1
        elif self.choix_mode.get() == "Infini" :
            indice = 2
        elif self.choix_mode.get() == "Juju" :
            indice = 3
        seq_decoupe = seq[indice].split("\t\t")
        highscore_actuel = int((seq[indice].split("\t\t"))[2])
        if self.le_score > highscore_actuel :
            record_battu = True
            ligne_a_ecrire = f"{self.choix_mode.get()}\t\t{self.joueur_courant.nom}\t\t{int(self.le_score)}\n"
            del seq[indice]
            seq.insert(indice,ligne_a_ecrire)
            filout = open('highscores.txt', 'w+')
            for li in seq :
                filout.write(li)
            filout.close()
        else :
            record_battu = False
        return record_battu
     
    def get_profils(self):
        self.liste_profils = []
        try :
            filin = open('profils.txt', 'r')
            seq = filin.readlines()
            del seq[0]
            for li in seq:
                joueur = (li.split("\t"))[0]
                niveau = int((li.split("\t"))[1])
                xp = int((li.split("\t"))[2])
                record = [int((li.split("\t"))[3]),int((li.split("\t"))[4]),int((li.split("\t"))[5])]
                level = (li.split("\t"))[6]
                attributs = [int((li.split("\t"))[7]),int((li.split("\t"))[8]),(li.split("\t"))[9],int((li.split("\t"))[10]),int((li.split("\t"))[11]),(li.split("\t"))[12],(li.split("\t"))[13],(li.split("\t"))[14]]
                golds = int((li.split("\t"))[15])
                points_upgrades = int((li.split("\t"))[16])
                self.liste_profils.append([joueur,niveau,xp,record,level,attributs,golds,points_upgrades])
            filin.close()
        except FileNotFoundError :
            pass

    def set_profils(self):
        # self.arrete_souris = True
        self.get_profils()
        fenetre_profils = tk.Toplevel(self)
        fenetre_profils.geometry(f"{int(L_JEU/2)+40}x{int(H_JEU/4)+50}+{int(L_JEU/3)}+{int(H_JEU/3)}")
        fenetre_profils.resizable(width=False, height=False)
        fenetre_profils.title("Choix du profil")
        fenetre_profils.transient(self)              
        label_choix_profil = tk.Label(fenetre_profils, text="Choisissez un profil existant ou créez un nouveau joueur")
        label_choix_profil.grid(column=1,row=1)                
        def nouveau_joueur():
            fenetre_nouveau_joueur = tk.Toplevel(fenetre_profils)
            fenetre_nouveau_joueur.geometry(f"{int(L_JEU/3)}x{int(H_JEU/6)}+{int(L_JEU/3)+50}+{int(H_JEU/2)-100}")
            fenetre_nouveau_joueur.resizable(width=False, height=False)
            fenetre_nouveau_joueur.title("Nouveau Joueur")
            fenetre_nouveau_joueur.transient(fenetre_profils)
            #Label nom du joueur
            label_nom_joueur = tk.Label(fenetre_nouveau_joueur, text="Nom du Joueur :", font=20)
            label_nom_joueur.place(x=42,y=10)
            #Entrée nom joueur
            entree_joueur = tk.Entry(fenetre_nouveau_joueur,takefocus=True,width = 30)
            entree_joueur.place(x=12,y=40)
            entree_joueur.focus_force()
            def fermeture_nouveau_joueur(event=None):
                if entree_joueur.get()!="":
                    self.le_joueur=entree_joueur.get()
                    self.liste_profils.append([entree_joueur.get(),1,0,[0,0,0],"LVL0",[20,1,'Inexistante',2,1,'1-1','5-1','0-0-0'],0,0])
                    fenetre_nouveau_joueur.destroy()
                    fenetre_nouveau_joueur.update()
                    fermeture(event='joueur créé')                      
                else:
                    fenetre_nouveau_joueur.destroy()
                    fenetre_nouveau_joueur.update()
                    nouveau_joueur()
            tk.Button(fenetre_nouveau_joueur, text="Ok",command=fermeture_nouveau_joueur).place(x=83,y=70)
            fenetre_nouveau_joueur.protocol("WM_DELETE_WINDOW", fermeture_nouveau_joueur)
            fenetre_nouveau_joueur.bind('<Return>',fermeture_nouveau_joueur)
        bouton_nouveau_joueur = tk.Button(fenetre_profils, text="Nouveau Joueur",command=nouveau_joueur)
        bouton_nouveau_joueur.grid(column=1,row=2)
        listbox = tk.Listbox(fenetre_profils,height=6,selectmode=tk.SINGLE)
        for prof in self.liste_profils :
            listbox.insert(tk.END,prof[0])
        listbox.grid(column=1,row=3)
        listbox.select_set(0)
        def fermeture(event=None):
            if event == 'joueur créé':
                fenetre_profils.destroy()
                fenetre_profils.update()
                self.new_player = True
                self.nouvelle_partie()
            elif listbox.curselection()!= ():
                self.le_joueur=listbox.get(listbox.curselection()[0])
                fenetre_profils.destroy()
                fenetre_profils.update()
                self.new_player = False
                self.nouvelle_partie()
            else :
                nouveau_joueur()
        bouton_ok = tk.Button(fenetre_profils, text="Ok",command=fermeture)
        bouton_ok.grid(column=1,row=4)                                        
        fenetre_profils.protocol("WM_DELETE_WINDOW", fermeture) 
        
    def save_profils(self):
        try :
            filout = open('profils.txt', 'r')
            seq = filout.readlines()
            filout.close()
            del seq[0]
            if self.new_player == True :
                self.new_player = False
                lindice = len(seq)+1
            else:
                for prof in seq :
                    if self.joueur_courant.nom == prof.split("\t")[0]:
                        lindice = seq.index(prof)
                del seq[lindice]
        except FileNotFoundError : #normalement arrive uniquement a la première ouverture du jeu
            seq=[]
            lindice = 0
            self.new_player = False
        ligne_a_ecrire = f"{self.joueur_courant.nom}\t{self.joueur_courant.niveau}\t{self.joueur_courant.xp}\t{self.joueur_courant.record[0]}\t{self.joueur_courant.record[1]}\t{self.joueur_courant.record[2]}\t{self.joueur_courant.level}\t{self.joueur_courant.attributs[0]}\t{self.joueur_courant.attributs[1]}\t{self.joueur_courant.attributs[2]}\t{self.joueur_courant.attributs[3]}\t{self.joueur_courant.attributs[4]}\t{self.joueur_courant.attributs[5]}\t{self.joueur_courant.attributs[6]}\t{self.joueur_courant.attributs[7]}\t{self.joueur_courant.golds}\t{self.joueur_courant.points_upgrades}\n"   
        seq.insert(lindice,ligne_a_ecrire)
        seq.insert(0,'Nom\tNiveau\tXP\tHistoire\tJuju\tInfini\tLast lvl\tSkills : A\tB\tC\tD\tE\tF\tG\tH\tGold\tUp Pts\n')
        filout = open('profils.txt', 'w+')
        for li in seq :
            filout.write(li)
        filout.close()
    
            
    def stop(self, esc=None):
        """Quitte l'application."""
        # self.balle_servie = False
        self.arrete_souris = True
        matrice_threads = [self.liste_threads_sd,self.liste_threads_mult2,self.liste_threads_mult5,self.liste_threads_nb,self.liste_threads_sb] #,self.liste_threads_souris]
        for liste_thr in matrice_threads :
            for thr in liste_thr :
                thr.join()
        pygame.quit()
        self.quit()
        
    def RGB(self,rgb):
        return "#%02x%02x%02x" % rgb 


if __name__ == "__main__":
    # ici débute le programme principal  
    myapp = Casse_Briques()
    myapp.title("                                                 CASSE-BRIQUES")
    myapp.mainloop()

    
