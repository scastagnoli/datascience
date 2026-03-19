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
Assgnato un DataFrame possiamo applicare i metodi `max()`, `min()`, `mean()` per calcolare massimo, minimo e media divisi per colonna.   
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
`df.describe()`: visualizzazione di alcune statistiche del dataframe

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
La seguente tabella riporta una serire di metodi alternativi (compreso la sostituzione di NaN con la media):
| Metodo                       | Frammento di codice                                                                                                                                                                     | Quando è preferibile                                                    | Note                                                  |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------- |
| Eliminare le righe mancanti  | `df = df.dropna(subset=['Calories'])`                                                                                                                                                   | Quando i `NaN` sono pochi e non vuoi introdurre stime artificiali       | Semplice e pulito, ma perdi osservazioni              |
| Sostituzione con media       | `df['Calories'] = df['Calories'].fillna(df['Calories'].mean())`                                                                                                                         | Quando vuoi una soluzione rapida e i dati sono abbastanza simmetrici    | Può ridurre la varianza e appiattire la distribuzione |
| Sostituzione con mediana     | `df['Calories'] = df['Calories'].fillna(df['Calories'].median())`                                                                                                                       | Quando ci sono outlier o distribuzione asimmetrica                      | Più robusta della media                               |
| Forward fill                 | `df['Calories'] = df['Calories'].ffill()`                                                                                                                                               | Quando i dati sono ordinati e il valore precedente è una buona stima    | Tipico di serie temporali o sensori                   |
| Backward fill                | `df['Calories'] = df['Calories'].bfill()`                                                                                                                                               | Quando il valore successivo è più informativo del precedente            | Anche questo tipico di dati sequenziali               |
| Interpolazione lineare       | `df['Calories'] = df['Calories'].interpolate()`                                                                                                                                         | Quando i valori cambiano in modo continuo e graduale                    | Buona scelta per misure numeriche ordinate            |
| Valore costante              | `df['Calories'] = df['Calories'].fillna(0)`                                                                                                                                             | Solo se `0` ha senso reale nel dominio del dato                         | Nel tuo dataset in genere non è una buona idea        |
| Regressione su altre colonne | `mask = df['Calories'].isna(); model.fit(df.loc[~mask, ['Duration','Pulse']], df.loc[~mask, 'Calories']); df.loc[mask, 'Calories'] = model.predict(df.loc[mask, ['Duration','Pulse']])` | Quando esistono variabili fortemente correlate con la colonna mancante  | Nel tuo caso è una delle opzioni migliori             |
| KNN Imputation               | `from sklearn.impute import KNNImputer; imputer = KNNImputer(n_neighbors=5); df[['Duration','Pulse','Calories']] = imputer.fit_transform(df[['Duration','Pulse','Calories']])`          | Quando vuoi usare osservazioni simili per stimare i mancanti            | Utile su dataset più grandi                           |
| Imputazione per gruppo       | `df['Calories'] = df['Calories'].fillna(df.groupby('Duration')['Calories'].transform('median'))`                                                                                        | Quando i dati hanno gruppi naturali e vuoi imputare in modo contestuale | Utile se hai categorie o classi ben definite          |


Nella sostituzione possiamo tenere conto anche solo del valore precedente e di quello successivo: possiamo avere diversi casi applicativi:
| Metodo                                      | Codice                                                                           | Come funziona                                                                          | Quando usarlo                               | Limiti                                        |
| ------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------- |
| Interpolazione lineare (default)            | `df['Calories'] = df['Calories'].interpolate()`                                  | Stima il valore tra due punti con una retta (media pesata tra precedente e successivo) | Dati continui e ordinati (tempo, misure)    | Non adatto a dati discontinui                 |
| Media tra precedente e successivo (manuale) | `df.loc[mask,'Calories'] = (df['Calories'].shift(1)+df['Calories'].shift(-1))/2` | Media semplice dei due vicini                                                          | Caso base, dati regolari e equispaziati     | Non gestisce bene più NaN consecutivi         |
| Interpolazione con direzione (solo forward) | `df['Calories'].interpolate(limit_direction='forward')`                          | Usa solo valori precedenti                                                             | Serie temporali dove il passato è rilevante | Perde informazione futura                     |
| Interpolazione con entrambe le direzioni    | `df['Calories'].interpolate(limit_direction='both')`                             | Usa valori prima e dopo (anche ai bordi)                                               | Quando hai NaN all’inizio o fine            | Può introdurre stime meno affidabili ai bordi |
| Interpolazione su più NaN consecutivi       | `df['Calories'].interpolate()`                                                   | Distribuisce i valori lungo la linea tra due estremi                                   | Gap brevi e continui                        | Gap lunghi → stima poco affidabile            |
| Interpolazione con indice (time-based)      | `df.interpolate(method='time')`                                                  | Usa distanza temporale reale tra punti                                                 | Serie temporali con timestamp               | Richiede indice datetime                      |
| Interpolazione polinomiale                  | `df['Calories'].interpolate(method='polynomial', order=2)`                       | Usa una curva invece di una retta                                                      | Trend non lineari                           | Rischio overfitting                           |
| Interpolazione spline                       | `df['Calories'].interpolate(method='spline', order=2)`                           | Curva più flessibile                                                                   | Dati smooth e complessi                     | Più complesso e meno interpretabile           |
| Interpolazione + riempimento bordi          | `df['Calories'] = df['Calories'].interpolate().bfill().ffill()`                  | Interpola e poi riempie i bordi                                                        | Quando hai NaN all’inizio/fine              | Può introdurre bias ai bordi                  |


Lo script seguente è molto utile per mettere a confronto il comportamento di diversi tipi di imputazioni che potrei utilizzare:
```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('data.csv')

mask = df['Calories'].isna()

# --- MODELLI ---

# Mean
mean_values = df['Calories'].fillna(df['Calories'].mean())[mask]

# Interpolation
interp_values = df['Calories'].interpolate()[mask]

# Regressione lineare
X_train = df.loc[~mask, ['Duration','Pulse']]
y_train = df.loc[~mask, 'Calories']

lin = LinearRegression().fit(X_train, y_train)
lin_values = lin.predict(df.loc[mask, ['Duration','Pulse']])

# Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=0)
rf.fit(X_train, y_train)
rf_values = rf.predict(df.loc[mask, ['Duration','Pulse']])

# --- TABELLA PRINCIPALE (solo NaN) ---

comparison = pd.DataFrame({
    'Duration': df.loc[mask, 'Duration'],
    'Pulse': df.loc[mask, 'Pulse'],
    'Mean': mean_values,
    'Interpolation': interp_values,
    'Linear Regression': lin_values,
    'Random Forest': rf_values
}).round(2)

print("\n=== Confronto imputazioni ===")
print(comparison)

# --- CONTESTO: righe precedente + NaN + successiva ---

rows_to_show = []

for idx in df.index[mask]:
    for i in [idx-1, idx, idx+1]:
        if i in df.index:
            row = df.loc[i].copy()
            
            # etichetta il tipo di riga
            if i == idx:
                row['Type'] = 'NaN'
            elif i == idx-1:
                row['Type'] = 'Prev'
            else:
                row['Type'] = 'Next'
            
            row['Index'] = i
            rows_to_show.append(row)

context_df = pd.DataFrame(rows_to_show)

# riordino colonne
cols = ['Index', 'Type'] + [c for c in context_df.columns if c not in ['Index','Type']]
context_df = context_df[cols]

print("\n=== Contesto (Prev / NaN / Next) ===")
print(context_df)
```

### Analisi della correlazione
Una volta che non abbiamo valori NaN all'interno del DataFrame possiamo studiare la correlazione fra alcune colonne.   
Ad esempio la correlazione fra `Calories` e `Duration` può essere calcolata come segue:  
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
### Clustering dei dati
Possiamo utilizzare una funzione di machine-learning per raggruppare dati di colonne specificate che presentano dati "simili" (necessario eseguire il comando  `pip install scikit-learn`):
```python
from sklearn.cluster import KMeans

X = df[['Duration','Pulse','Calories']]
kmeans = KMeans(n_clusters=3)
df['cluster'] = kmeans.fit_predict(X)

#Visualizzo la dimensione del gruppo:
df['cluster'].value_counts()

#Visualizzo il valore medio di ogni colonna ragguppando per cluster:
df.groupby('cluster').mean()

#Visualizzo le righe di un cluster specifico:
df.query("cluster == 1")
```

Il numero corretto dei cluster può essere ottenuto con il metodo "Elbow".

### Esempi avanzati di grafici seaborn
