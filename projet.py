import pandas as pd
import sklearn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

"""df=pd.read_excel("donnees_pluvio_2018\\01_janvier\\01_janvier_2018.xlsx",usecols="A,B,D,F,H,J", skiprows=[0,1,2,3,4,5,6,7],sheet_name=0,skipfooter=47)
df=pd.DataFrame(df)
print(df)"""
"""
#2018
d2018=pd.read_excel("donnees_pluvio_2018\\annee2018_6mn.xls",sheet_name=0,header=5,engine="xlrd",usecols=[0]+[i for i in range(1,62) if i%2==1])
d2018=pd.DataFrame(d2018)
#print(d2018)

d2018["Date"]=d2018["Date"].apply(lambda x: str(x).split(" ")[0])
d2018=d2018.groupby(['Date']).sum()
#print(d2018)

#2019
d2019=pd.read_excel("donnees_pluvio_2019\\annee2019_6mn.xls",sheet_name=0,header=5,engine="xlrd",usecols=[0]+[i for i in range(1,62) if i%2==1])
d2019=pd.DataFrame(d2019)
#print(d2019)

d2019["Date"]=d2019["Date"].apply(lambda x: str(x).split(" ")[0])
d2019=d2019.groupby(['Date']).sum()
#print(d2019)

#2020
d2020=pd.read_excel("donnees_pluvio_2020\\6mn_2020.xls",sheet_name=0,header=5,engine="xlrd",usecols=[0]+[i for i in range(1,62) if i%2==1])
d2020=pd.DataFrame(d2020)
#print(d2020)

d2020["Date"]=d2020["Date"].apply(lambda x: str(x).split(" ")[0])
d2020=d2020.groupby(['Date']).sum()
#print(d2020)

#2021
d2021=pd.read_excel("donnees_pluvio_2021\\6mn_2021.xls",sheet_name=0,header=6,engine="xlrd",usecols=[0]+[i for i in range(1,62) if i%2==1])
d2021=pd.DataFrame(d2021)
#print(d2021)

d2021["Date"]=d2021["Date"].apply(lambda x: str(x).split(" ")[0])
d2021=d2021.groupby(['Date']).sum()
#print(d2022.groupby(['Date']).sum())
#d2022=d2022.groupby(['Date'],group_keys=False).sum().apply(lambda x: x)
#print(d2021)


dtot=pd.concat([d2018,d2019,d2020,d2021])
#print(dtot)
dtot2=dtot.reset_index().melt("Date")
#print(dtot2)

#courbe pluie pendant les années, par jour
#somme de tout, quelle region plus plus, diagramme camembert
#acp, ville ou date plus d'importance? 
#acp premier tableau, quelle ville à le plus d'importance, combinaison linéaire de ville à un sens ?
#ville ou ça varie le plus, variance par mois 
#trouve localisation
"""

data = pd.DataFrame(pd.read_csv("Data_Measure_Trié.csv"))
data=data.drop("Opérationnel",axis="columns")
#print(data)


#Sans zsol

station = pd.DataFrame(pd.read_csv("liste_stations.csv", sep = "\t",usecols = ["nom","identifiant","lon","lat"]))
#print(station)

#= data["Station"].apply(lambda x: x.split(" ")[1:])     
#data["Station"] = data["Station"].apply(lambda x :str(x))
station["identifiant"] = station["identifiant"].apply(lambda x: str(x) if len(str(x)) >=2 else "0"+str(x))

new = station["identifiant"]+" "+station["nom"]

new_station=pd.DataFrame({"Station" : new, "lon" :station["lon"], "lat": station["lat"]})
#print(new_station)

data=data.merge(new_station)
#print(data)

data = data.set_index("Hauteur")
data["Station"] = data["Station"].apply(lambda x : x.split(" ")[0])
data["Annee"] = data["Date"].apply(lambda x : x.split("-")[0])
data["Mois"] = data["Date"].apply(lambda x : x.split("-")[1])
data["Mois"] = data["Mois"].apply(lambda x : int(x))
data = data.drop(["Date","Annee","Station"], axis="columns")

print(data)

print("mean", data["Mois"].mean())
print("std", data["Mois"].std()) #ATTENTION ECART TYPE

print("corrélation", data.corr())

#ACP 
acp = PCA(svd_solver='full')
sc = StandardScaler(with_mean=True, with_std=True)
data2 = sc.fit_transform(data)
print("DATA2", data2)
coord=acp.fit_transform(data2)

print("coord", coord) #influence par rapport à pluie 


#print(acp.n_components_)
#print(acp.explained_variance_)
#print(acp.explained_variance_ratio_)

n = data.shape[0]
p = data.shape[1]
eigval = (n-1)/n*acp.explained_variance_ #vp
#print(eigval)
sqrt_eigval = np.sqrt(eigval)
corvar = np.zeros((p,p)) #initialisation mat
for k in range(p):
    corvar[:,k] = acp.components_[k,:] * sqrt_eigval[k]
#print(corvar) #calcul mat correlation
print(pd.DataFrame({'id':data.columns,'COR_1':corvar[:,0],'COR_2':corvar[:,1],'COR_3':corvar[:,2]}))

fig, axes = plt.subplots(figsize=(8,8))
axes.set_xlim(-1,1)
axes.set_ylim(-1,1)

for j in range(p):
    plt.annotate(data.columns[j],(corvar[j,0],corvar[j,1]))
    
plt.plot([-1,1],[0,0],color='silver',linestyle='-',linewidth=1)
plt.plot([0,0],[-1,1],color='silver',linestyle='-',linewidth=1)

cercle = plt.Circle((0,0),1,color='blue',fill=False)
axes.add_artist(cercle)

plt.show()

#Avec zsol

"""
station = pd.DataFrame(pd.read_csv("liste_stations.csv", sep = "\t",usecols = ["nom","identifiant","lon","lat","zsol"]))
#print(station)


#= data["Station"].apply(lambda x: x.split(" ")[1:])     
#data["Station"] = data["Station"].apply(lambda x :str(x))
station["identifiant"] = station["identifiant"].apply(lambda x: str(x) if len(str(x)) >=2 else "0"+str(x))

new = station["identifiant"]+" "+station["nom"]

new_station=pd.DataFrame({"Station" : new, "lon" :station["lon"], "lat": station["lat"], "zsol" : station["zsol"]})
#print(new_station)

data=data.merge(new_station)
#print(data)

data = data.set_index("Hauteur")
data["Station"] = data["Station"].apply(lambda x : x.split(" ")[0])
data["Annee"] = data["Date"].apply(lambda x : x.split("-")[0])
data["Mois"] = data["Date"].apply(lambda x : x.split("-")[1])
data["Mois"] = data["Mois"].apply(lambda x : int(x))
data = data.drop(["Date","Annee","Station"], axis="columns")

print(data)

print("mean", data["Mois"].mean())
print("std", data["Mois"].std()) #ATTENTION ECART TYPE

print("corrélation", data.corr())

#ACP 
acp = PCA(svd_solver='full')
sc = StandardScaler(with_mean=True, with_std=True)
data2 = sc.fit_transform(data)
print("DATA2", data2)
coord=acp.fit_transform(data2)

print("coord", coord)

#print(acp.n_components_)
#print(acp.explained_variance_)
#print(acp.explained_variance_ratio_)

n = data.shape[0]
p = data.shape[1]
eigval = (n-1)/n*acp.explained_variance_ #vp
#print(eigval)
sqrt_eigval = np.sqrt(eigval)
corvar = np.zeros((p,p)) #initialisation mat
for k in range(p):
    corvar[:,k] = acp.components_[k,:] * sqrt_eigval[k]
#print(corvar) #calcul mat correlation
print(pd.DataFrame({'id':data.columns,'COR_1':corvar[:,0],'COR_2':corvar[:,1],'COR_3':corvar[:,2],'COR_4':corvar[:,3]}))

fig, axes = plt.subplots(figsize=(8,8))
axes.set_xlim(-1,1)
axes.set_ylim(-1,1)

for j in range(p):
    plt.annotate(data.columns[j],(corvar[j,0],corvar[j,1]))
    
plt.plot([-1,1],[0,0],color='silver',linestyle='-',linewidth=1)
plt.plot([0,0],[-1,1],color='silver',linestyle='-',linewidth=1)

cercle = plt.Circle((0,0),1,color='blue',fill=False)
axes.add_artist(cercle)

#plt.show()
"""



#faire deux acp avec et sans zsol : zsol assez corrélé avec lattitude donc 2ème acp pas forcément utile
#première acp les mois sont corrélés négativement 

#Fait : 
#Courbe précipitation
#pie proportion saison
#2 ACP

#A faire :
#carte avec folium (prop ville selon taille)
#box plot variance pour chaque station


#3eme coord : long <0, lat <0 : Sudouest, corrélé <0 à pluie : peu pas bcp sud ouest
#1eme coord : regarder quicieux (nord) givors(sud)

