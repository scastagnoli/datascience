## Predisporre l'ambiente
### Installare
1. Visual Studio Code (VSCode)
2. estensioni di VSCode:
    - 2.1. Python (di Microsoft)
    - 2.2 Juputer (di Microsoft)

### Link di riferimento:
- https://www.w3schools.com/python/pandas/default.asp
- https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
- https://www.kaggle.com/code/residentmario/creating-reading-and-writing

### Creazione e uso di un virtual env
Un virtual env Python è una cartella all'interno della quale utilizzo una versione di Python installata sul mio PC ma con un elenco di librerie isolato dal resto del PC.
Per creare un virtual env nella cartella "esercizio":
```bash
python3 -m venv esercizio
```
Una volta creato il virtual env devo attivarlo con il comando seguente eseguito dalla cartella in cui ho creato il virtual env:
```bash
source bin/activate
```
A conferma che il virtual env sia stato attivato correttamente compare il nome della cartella corrente all'interno di parentesi tonde a sinistra del prompt corrente.
Il virtual env può essere disattivato semplicemente con:
```bash
deactivate
```
Il virtual env può essere attivato e deattivato senza problemi.
Una volta attivato possiamo usare il comando seguente per installare Pandas:
```bash
pip install pandas
```

## Primi esercizi con pandas
### Esercizio 1
```python
import pandas

mydataset = {
  'cars': ["BMW", "Volvo", "Ford"],
  'passings': [3, 7, 2]
}

myvar = pandas.DataFrame(mydataset)

print(myvar)
```

Possiamo aggiungere righe e colonne a un dataframe.  
Per aggiungere righe dobbiamo aggiungere lo stesso numero di elementi alle liste di ogni una chiave.  
Per aggiungere una colonna abbiamo diverse alternative:
### Alternativa 1
Aggiungo direttamente una colonna al DataFrame:
```python
import pandas as pd

df = pd.DataFrame({
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]
})
df["citta"] = ["cesena", "rimini", "milano"]
print(df)
```
### Alternativa 2
Utilizzo una formula per generare un campo autocalcolato:
```python
import pandas as pd

df = pd.DataFrame({
    'cars': ["BMW", "Volvo", "Ford"],
    'passings': [3, 7, 2]
})
df["nextPassing"] = df["passings"] + 100
print(df)
```

### Alternativa 3
Usando il metodo ```assign()``` possiamo inserire anche più colonne con un solo comando:
```python
df2 = df.assign(
    eta_tra_10_anni = lambda x: x["eta"] + 10,
    maggiorenne = lambda x: x["eta"] >= 18
)
```

### Cancellazione di una colonna
```python
df = df.drop("colonna", axis=1)
```

### Calcolo di principali funzioni statistiche su un DataFrame
Assgnato un DataFrame possiamo applicare i metodi ```max()```, ```min()```, ```mean()``` per calcolare massimo, minimo e media divisi per colonna.   
Ad esempio con il codice seguente possiamo visualizzare un insieme di dati statistici:
```python
import pandas as pd

df = pd.DataFrame({
    "A": [10, 20, 30],
    "B": [5, 15, 25],
    "C": [7, 14, 21]
})
print(df)

print(df.min())
print(df.max())
print(df.mean())

print(df.describe())

print(df.min(axis=1))   #minimo per riga
print(df.max(axis=1))   #massimo ...
print(df.mean(axis=1))  #media ...
```

Il 25% indica il 25-esimo percentile, cioè il 25% dei dati è minore o uguale di quel valore. Ad esempio se il 25% fosse 30 vorrebbe dire che il 25% dei dati è inferiore a 30.
Analogamente per 50% e 75%.



## File CSV e analisi dei dati
https://www.w3schools.com/python/pandas/pandas_csv.asp   
Assegnato un file CSV possiamo generare il DataFrame corrispondente nel modo seguente:
```python
import pandas as pd
df = pd.read_csv("nomeFile.csv")
```
Una volta pronto il DataFrame possiamo iniziare a estrarre i dati:
```df.describe()```: visualizzazione di alcune statistiche del dataframe

Alcune delle attività più utili possono essere riassunte nella seguente tabella:
| Obiettivo          | Codice                   |
| ------------------ | ------------------------ |
| NaN in una colonna | `df['col'].isna().sum()` |
| NaN per colonna    | `df.isna().sum()`        |
| NaN totali         | `df.isna().sum().sum()`  |
| NaN per riga       | `df.isna().sum(axis=1)`  |
| Percentuale NaN    | `df.isna().mean()*100`   |

Una semplice attività di data cleaning è sostituire al posto dei valori NaN un valore valido, ad esempio il valore medio della colonna:
```python
df = df.copy()  #sempre da fare prima di una modifica strutturale per evitare comportamenti inaspettati
df['Calories'] = df['Calories'].fillna(df['Calories'].mean())
```

### Analisi della correlazione
Una volta che non abbiamo valori NaN all'interno del DataFrame possiamo studiare la correlazione fra alcune colonne.   
Ad esempio la correlazione fra ```Calories``` e ```Duration``` può essere calcolata come segue:  
```python
df[['Calories', 'Duration']].corr()
```
opure è frequente trovare il seguente modo per analizzare la correlazione fra due variabili:
```python
df['Calories'].corr(df['Duration'])
```
La correlazione può essere analizzata con un grafico:
```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data.csv")
sns.regplot(
    data=df,
    x='Duration',
    y='Calories'
)

plt.title("Correlazione Duration vs Calories")
plt.show()
```
## Clustering dei dati

```python
from sklearn.cluster import KMeans

X = df[['Duration','Pulse','Calories']]
kmeans = KMeans(n_clusters=3)
df['cluster'] = kmeans.fit_predict(X)


Visualizzo la dimensione del gruppo:
df['cluster'].value_counts()

Visualizzo il valore medio di ogni colonna ragguppando per cluster:
df.groupby('cluster').mean()

Visualizzo le righe di un cluster specifico:
df.query("cluster == 1")
```

Il numero corretto dei cluster può essere ottenuto con il metodo "Elbow".

