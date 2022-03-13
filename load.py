# Auteur Guillaume ROUSSEAU, Novembre 2020
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.optimize import curve_fit
from datetime import date
from datetime import datetime
import fnmatch
import os,time

dx=UpdateData()

#print("dx",dx)

#dx="2021-01-07"
#path="/content/drive/My Drive/Colab Notebooks/"
path="./RawData/"
#reg,cheflieu,tncc,ncc,nccenr,libelle
region={}
region["01"]="GUADELOUPE"
region["02"]="MARTINIQUE"
region["03"]="GUYANE"
region["04"]="LA REUNION"
region["06"]="MAYOTTE"
region["11"]="ILE DE FRANCE"
region["24"]="CENTRE VAL DE LOIRE"
region["27"]="BOURGOGNE FRANCHE COMTE"
region["28"]="NORMANDIE"
region["32"]="HAUTS DE FRANCE"
region["44"]="GRAND EST"
region["52"]="PAYS DE LA LOIRE"
region["53"]="BRETAGNE"
region["75"]="NOUVELLE AQUITAINE"
region["76"]="OCCITANIE"
region["84"]="AUVERGNE RHONE ALPES"
region["93"]="PROVENCE ALPES COTE D AZUR"
region["94"]="CORSE"

trancheage={
    0:'0 à 99+ ans', 
    9:'0 à 9 ans', 
    19:'10 à 19 ans', 
    29:'20 à 29 ans', 
    39:'30 à 39 ans', 
    49:'40 à 49 ans', 
    59:'50 à 59 ans', 
    69:'60 à 69 ans', 
    79:'70 à 79 ans', 
    89:'80 à 89 ans', 
    90:'90 à 99+ ans' 
    }

def dt(a,m,j):
    nall=date(2020,12,31)-date(2020,1,1)
    nb=date(a,m,j)-date(2020,1,1)
    return nb.days/nall.days*12+1

debut_confinement_1=dt(2020,3,17)
fin_confinement_1=dt(2020,5,11)

debut_couvrefeu_1=dt(2020,10,17)
fin_couvrefeu_1=dt(2020,10,30)

debut_confinement_2=dt(2020,10,30)
fin_confinement_2=dt(2020,11,28)

debut_couvrefeu_2=dt(2020,11,28)
fin_couvrefeu_2=dt(2021,3,19)

debut_confinement_3=dt(2021,3,20)
fin_confinement_3=dt(2021,4,3)

debut_confinement_4=dt(2021,4,3)
fin_confinement_4=dt(2021,5,2)


debut_couvrefeu_3=dt(2021,5,3)
fin_couvrefeu_3=dt(int(dx[:4]),int(dx[5:7]),int(dx[8:]))




color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
              '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
              '#bcbd22', '#17becf']

data3,fields,dfields=ReadClasseAge(dx)

dataN=ReadNouveaux(dx)