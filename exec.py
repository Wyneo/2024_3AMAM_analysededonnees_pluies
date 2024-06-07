import pandas as pd


def extract_data_pluie(link,head,dys):
    boo_dys=1
    if(dys):
        boo_dys=0
    DF=pd.DataFrame(pd.read_excel(link,header=head,engine="xlrd",usecols=[0]+[i for i in range(1,62) if(i%2==boo_dys)]))
    DF["Date"]=DF["Date"].apply(lambda x:str(x).split(" ")[0])
    DF=DF.groupby(DF["Date"]).aggregate("sum")
    return(DF)


link=["donnees_pluvio_2018\\annee2018_6mn.xls","donnees_pluvio_2019\\annee2019_6mn.xls","donnees_pluvio_2020\\6mn_2020.xls","donnees_pluvio_2021\\6mn_2021.xls"]
head=[5,5,5,6]
DF_pluie_all=[]
DF_dys_all=[]
for i in range(4):
    DF_pluie_all.append(extract_data_pluie(link[i],head[i],False))
    DF_dys_all.append(extract_data_pluie(link[i],head[i],True))
DF_concat_pluie=pd.concat(DF_pluie_all)
DF_concat_dys=pd.concat(DF_dys_all)
DF_concat_dys["Unnamed: 62"]=0

DF_concat_dys.columns=DF_concat_pluie.columns

DF_concat_pluie=pd.DataFrame(DF_concat_pluie.reset_index().melt('Date'))
DF_concat_dys=pd.DataFrame(DF_concat_dys.reset_index().melt('Date'))
DF_concat_pluie=DF_concat_pluie.rename(columns={"variable":"Station", "value":"Hauteur"})
DF_concat_dys=DF_concat_dys.rename(columns={"variable":"Station","value":"Opérationnel"})
DF_concat_dys["Opérationnel"]=DF_concat_dys["Opérationnel"].apply(lambda x:False if("*" in str(x)) else True)
DF_concat_pluie["Opérationnel"]=DF_concat_dys["Opérationnel"]
DF_concat_pluie.to_csv("Data_Measure_All.csv",index=False)

DF_concat_pluie=DF_concat_pluie[DF_concat_dys["Opérationnel"]]
print(DF_concat_pluie)

DF_concat_pluie.to_csv("Data_Measure_Trié.csv",index=False)

"""
import pandas as pd
import matplotlib.pyplot as plt

df=pd.DataFrame(pd.read_csv("Data_Column_Each"))
df=df.drop(columns=["Unnamed: 0"])

df["Month"]=df["Date"].apply(lambda x:str(x).split("-")[1])
df["Year"]=df["Date"].apply(lambda x:str(x).split("-")[0])
df=df.drop(df[df["Year"]!="2020"].index)
print(df)
df=df.drop(["Month","Year"],axis=1)
df["Date"]=df["Date"].apply(lambda x:str(x).split("-")[0]+"-"+str(x).split("-")[1])
df_n=df.groupby(df["Date"]).aggregate("sum")
df_n=df_n.reset_index()
df_n.plot("Date","Hauteur")
plt.show()
"""