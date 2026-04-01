import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "tempo": [0, 1, np.nan, 5, 6,7,8],
    "valore": [10, np.nan, np.nan, 40, 65,100, 110]
})
print("Iniziale:")
print(df)

#df = df.dropna(how='all')
print("Media = ", df["tempo"].mean())
print("Mediana = ", df["tempo"].median())
df['tempo'] = df["tempo"].fillna(df["tempo"].median())
print("Prima:")
print(df)

#Interpolazione
#Attenzione: per interpolare all'ordine N devo avere nella colonna N+1 valori validi
df_interp = df.interpolate(method="polynomial", order=1)
print("\nDopo interpolate (order=1):")
print(df_interp)

df_interp = df.interpolate(method="polynomial", order=2)
print("\nDopo interpolate (order=2):")
print(df_interp)

# Grafico
df["interp_order1"] = df["valore"].interpolate(method="polynomial", order=1)
df["interp_order2"] = df["valore"].interpolate(method="polynomial", order=2)
df["interp_order3"] = df["valore"].interpolate(method="polynomial", order=3)

plt.figure()

# Linee
sns.lineplot(data=df, x="tempo", y="interp_order1", label="order=1", errorbar= None)
sns.lineplot(data=df, x="tempo", y="interp_order2", label="order=2", errorbar=None)
sns.lineplot(data=df, x="tempo", y="interp_order3", label="order=3", errorbar=None)

# Punti originali
sns.scatterplot(data=df, x="tempo", y="interp_order1", color="black", label="originale")
#mettendo y="valore" avremmo il punto (5, NaN) che ovviamente non sarebbe visualizzato

plt.title("Confronto interpolazione")
plt.ylabel("Ordini di interpolazione")
plt.xlabel("Tempo")
plt.show()
