import pandas as pd

def extract_data_pluie(link,head):
    DF=pd.DataFrame(pd.read_excel(link,header=head,engine="xlrd",usecols=[0]+[i for i in range(1,62) if(i%2==1)]))
    DF["Date"]=DF["Date"].apply(lambda x:str(x).split(" ")[0])
    DF=DF.groupby(DF["Date"]).aggregate("sum")
    return(DF)

link=["donnees_pluvio_2018\\annee2018_6mn.xls","donnees_pluvio_2019\\annee2019_6mn.xls","donnees_pluvio_2020\\6mn_2020.xls","donnees_pluvio_2021\\6mn_2021.xls"]
head=[5,5,5,6]
DF_all=[]
for i in range(4):
    DF_all.append(extract_data_pluie(link[i],head[i]))
DF_concat=pd.concat(DF_all)
pd.options.display.max_rows = 999
print(DF_concat)
DF_concat.to_csv("Dataset_All")


