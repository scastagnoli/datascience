# Riassunto concetti di base:


Gli esempi presentati illustrano due tipi di analisi statistiche diverse:
1. categoriale (abbiamo riferimenti a categorie)
2. temporale (abbiamo riferimenti temporali)

## Funzioni
Le funzioni pandas che andiamo ad applicare sono diverse e possono essere riassunte nella seguente tabella:  

| Funzione                       | Tipologia analisi      | Categoriale | Temporale | Descrizione                                                                              | Esempio                                       |
| ------------------------------ | ---------------------- | ---- | ----- | ---------------------------------------------------------------------------------------- | --------------------------------------------- |
| `describe()`                   | Statistica descrittiva | ✅    | ✅     | Riepilogo completo: media, std, min, max, quartili (numeriche) e frequenze (categoriche) | `df.describe()`                               |
| `mean()`                       | Statistica descrittiva | ✅    | ✅     | Media aritmetica, sensibile agli outlier                                                 | `df["num"].mean()`                            |
| `median()`                     | Statistica descrittiva | ✅    | ✅     | Valore centrale robusto                                                                  | `df["num"].median()`                          |
| `quantile()`                   | Statistica descrittiva | ✅    | ✅     | Percentili (es. Q1, Q3)                                                                  | `df["num"].quantile(0.25)`                    |
| `value_counts()`               | Frequenze              | ✅    | ❌     | Conta le occorrenze per categoria                                                        | `df["col"].value_counts()`                    |
| `value_counts(normalize=True)` | Frequenze              | ✅    | ❌     | Frequenze relative (%)                                                                   | `df["col"].value_counts(normalize=True)`      |
| `crosstab()`                   | Frequenze              | ✅    | ❌     | Tabella incrociata tra due variabili                                                     | `pd.crosstab(df["A"], df["B"])`               |
| `groupby()`                    | Aggregazione           | ✅    | ✅     | Raggruppa i dati per chiave                                                              | `df.groupby("col")["num"].sum()`              |
| `groupby().mean()`             | Aggregazione           | ✅    | ✅     | Media per gruppo                                                                         | `df.groupby("col")["num"].mean()`             |
| `groupby().sum()`              | Aggregazione           | ✅    | ✅     | Somma per gruppo                                                                         | `df.groupby("col")["num"].sum()`              |
| `sort_values()`                | Aggregazione           | ✅    | ✅     | Ordina per valori                                                                        | `df.sort_values("num")`                       |
| `sort_index()`                 | Analisi temporale      | ❌    | ✅     | Ordina per indice (tempo)                                                                | `df.set_index("Year").sort_index()`           |
| `pct_change()`                 | Analisi temporale      | ❌    | ✅     | Variazione percentuale tra osservazioni                                                  | `df["num"].pct_change()`                      |
| `lineplot()`                   | Analisi temporale      | ❌    | ✅     | Visualizza trend nel tempo                                                               | `sns.lineplot(data=df, x="Year", y="num")`    |
| `corr()`                       | Relazioni              | ❌    | ✅     | Correlazione tra variabili numeriche                                                     | `df.corr(numeric_only=True)`                  |
| `heatmap()`                    | Relazioni              | ❌    | ✅     | Visualizzazione matrice di correlazione                                                  | `sns.heatmap(df.corr(numeric_only=True))`     |
| `plot(kind="hist")`            | Distribuzioni          | ✅    | ✅     | Distribuzione variabile numerica                                                         | `df["num"].plot(kind="hist")`                 |
| `plot(kind="bar")`             | Distribuzioni          | ✅    | ❌     | Grafico frequenze o aggregazioni                                                         | `df["col"].value_counts().plot(kind="bar")`   |
| `countplot()`                  | Distribuzioni          | ✅    | ❌     | Frequenze categorie (grafico)                                                            | `sns.countplot(data=df, x="col")`             |
| `isna()`                       | Data cleaning          | ✅    | ✅     | Individua valori mancanti                                                                | `df.isna().sum()`                             |
| `dropna()`                     | Data cleaning          | ✅    | ✅     | Rimuove valori nulli                                                                     | `df.dropna()`                                 |
| `fillna()`                     | Data cleaning          | ✅    | ✅     | Imputa valori mancanti                                                                   | `df["num"].fillna(df["num"].median())`        |
| `drop_duplicates()`            | Data cleaning          | ✅    | ✅     | Elimina duplicati                                                                        | `df.drop_duplicates()`                        |
| `replace()`                    | Data cleaning          | ✅    | ✅     | Sostituisce valori                                                                       | `df["col"].replace(0, None)`                  |
| `astype()`                     | Data cleaning          | ✅    | ✅     | Converte tipo dati                                                                       | `df["col"].astype(str)`                       |
| `str.strip()`                  | Pulizia testo          | ✅    | ❌     | Rimuove spazi iniziali/finali                                                            | `df["col"].str.strip()`                       |
| `str.upper()`                  | Pulizia testo          | ✅    | ❌     | Converte testo in maiuscolo                                                              | `df["col"].str.upper()`                       |  


## Grafica con Seaborn
Una volta creato un VirtualEnv è sufficiente installare Seaborn con ```pip install seaborn``` e analizzare gli esempi presenti nella galleria ufficiale Seaborn:

Nota: gli esempi si concentrano solo sulla creazione del grafico e non sulla sua visualizzazione per cui bisogna seguire il seguente schema:
```python
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["SSL_CERT_FILE"] = certifi.where()
 

import matplotlib.pyplot as plt

#qui si copia l'esempio della galleria Seaborn
import seaborn as sns
sns.set_theme(style="ticks")

df = sns.load_dataset("anscombe")#https://en.wikipedia.org/wiki/Anscombe%27s_quartet
sns.lmplot(
    data=df, x="x", y="y", col="dataset", hue="dataset",
    col_wrap=2, palette="muted", ci=None,
    height=4, scatter_kws={"s": 50, "alpha": 1}
)
#fine esempio galleria Seaborn

plt.show()
```
```Anscombe``` è un particolare dataset in cui tutti i 4 dataset presenti hanno lo stesso valore delle grandezze statistiche fondamentali. Possiamo verificare questo tramite il seguente codice:
```python
import seaborn as sns
import pandas as pd
import numpy as np

df = sns.load_dataset("anscombe")

def calcola_statistiche(g):
    slope, intercept = np.polyfit(g["x"], g["y"], 1)#calcolo m e q della retta di regressione fra x e y (grado 1): y=mx+q
    return pd.Series({
        "mean_x": g["x"].mean(),
        "mean_y": g["y"].mean(),
        "var_x": g["x"].var(),
        "var_y": g["y"].var(),
        "corr": g["x"].corr(g["y"]),
        "slope": slope,
        "intercept": intercept
    })

stats = df.groupby("dataset").apply(calcola_statistiche)

print(stats)
```

Possiamo applicare la stessa grafica a un altro dataset (```tips```):
```python
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="ticks")

# Nuovo dataset
df = sns.load_dataset("tips")
#posso visualizzare il valore della colonna day con df["day"].unique()
# Stessa logica di prima
sns.lmplot(
    data=df,
    x="total_bill",
    y="tip",
    col="day",           # aggrego per day. Non indicandolo i grafici vengono messi nello stesso piano cartesiano
    hue="day",
    col_wrap=2,          # se non indico col questo parametro non deve essere inserito
    palette="muted",    #scelgo la tipologia di colori meno saturi. Alternative: deep, bright, paste, dark, colorblind. Possiamo definire una palette personalizzata:
    """
    palette={
    "Thur": "blue",
    "Fri": "green",
    "Sat": "red",
    "Sun": "orange"
}"""
    ci=None,    #nessun intervallo di confidenza per la retta
    height=4,
    scatter_kws={"s": 50, "alpha": 0.7} #imposto dimensione dei punti e trasparenza
)

plt.show()
```
