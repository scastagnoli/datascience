## Esempio analisi dati : analisi categoriale  

Possiamo condurre uno studio sul file https://servizisit.unionevallesavio.it/geonextservices/gnsvcopendata/csv/1/OD_MONUMENTI_SDO, ottenuto cercando su motore di ricerca Google la stringa "open data csv" e cercando i dati relativi a Cesena, dividendolo in tre blocchi:

1. **data cleaning**
2. **analisi statistica**
3. **predizione con machine learning**

# Studio pandas su dataset monumenti

## 1. Obiettivo dello studio

I passaggi saranno questi:

* puliamo il dataset
* individuiamo valori mancanti e anomalie
* facciamo statistiche descrittive
* analizziamo distribuzioni e frequenze
* costruiamo un modello di machine learning per prevedere il tipo di monumento

Nel file caricato risultano:

* **163 righe e 9 colonne**
    1. ```df.shape``` (non include la riga di intestazione)
    2. ```len(df)``` e ```len(df.columns)```
    3. ```df.info()```
* variabili testuali e numeriche
* diverse anomalie utili per un esercizio di data cleaning

---

## 2. Lettura del dataset

Il file è separato da `;`, quindi va letto così:

```python
import pandas as pd
import numpy as np

df = pd.read_csv("OD_MONUMENTI_SDO_20260329181119.csv", sep=";")

print(df.head())    #visualizzo le prime 10 righe. df.tail()
"""
Concetto di teoria: cosa vedo con print(df.head) e print(df.tail)?
Vedo il riferimento in memoria ai metodi head() e tail(): i metodi non vengono eseguiti.
"""
print(df.info())
print(df.shape) #come altro potrei visualizzare le dimensioni di df?
```

---

## 3. Comprensione iniziale dei dati

Le colonne sono:

* `OBJECTID`
* `SHAPE`
* `COD_ISTAT`
* `TIPO`
* `LOCALITA`
* `ANNO_COLLO`
* `NUM_DOCU`
* `UBICAZIONE`
* `OPERA`
Come posso fare per visualizzarle?
### Prime osservazioni utili

Dal dataset emergono subito questi punti:

* `SHAPE` è completamente vuota
* `COD_ISTAT` ha alcuni valori mancanti
* `ANNO_COLLO` contiene molti zeri, che probabilmente non rappresentano un vero anno
* le colonne testuali (`TIPO`, `LOCALITA`, `UBICAZIONE`, `OPERA`) sono molto interessanti per analisi e predizione

---

# 4. Data cleaning

## 4.1 Controllo dei valori mancanti

```python
print(df.isna().sum())  #visualizzo i valori NaN (null)
```

### Risultato atteso

* `SHAPE`: tutti mancanti
* `COD_ISTAT`: alcuni mancanti
* le altre colonne sono quasi complete

---

## 4.2 Rimozione di colonne inutili

Poiché `SHAPE` è interamente nulla, la eliminiamo:

```python
df = df.drop(columns=["SHAPE"])
```

---

## 4.3 Trattamento dei valori anomali in `ANNO_COLLO`

Nel dataset ci sono molti `0` in `ANNO_COLLO`.
Posso contare quanti `0` sono presenti nella colonna `ANNO_COLLO` come segue:
```python
print((df["ANNO_COLLO"] == 0).sum())
#il risultato è 47
#posso anche visualizzare i valori "buoni"
print((df["ANNO_COLLO"] != 0).sum())
#il risultato è 116. 116+47=163, stesso risultato di df.shape -> (163,9)
```
Visualizzo le righe che contengono `0` e alcune colonne in particolare:
```python
df.loc[df["ANNO_COLLO"] == 0, ["TIPO", "LOCALITA", "OPERA", "ANNO_COLLO"]]
#df.loc[condizione_righe, colonne_da_mostrare]
```

In un contesto storico-monumentale, `0` non è un anno valido, quindi conviene trattarlo come valore mancante:

```python
df["ANNO_COLLO"] = df["ANNO_COLLO"].replace(0, np.nan)
```

Controlliamo quanti erano (devono essere lo stesso numero calcolato quando c'erano ancora gli `0`...):

```python
print((df["ANNO_COLLO"].isna()).sum())
```

Nel file risultano **47 valori problematici** legati agli anni (come prima).

---

## 4.4 Imputazione dei valori mancanti

### `COD_ISTAT`
Visualizzo la colonna e quanti sono i valori non presenti:
```python
df["COD_ISTAT"] #tutta la colonna
print(df["COD_ISTAT"].isna().sum())  #visualizzo quanti sono i valori NaN (null)
df.loc[:, ["COD_ISTAT", "OPERA"]]   #visualizzo le colonne COD_ISTAT e OPERA
df.loc[df["COD_ISTAT"].isna()==False, ["COD_ISTAT", "OPERA"]]   #visualizzo le colonne COD_ISTAT e OPERA solo dove COD_ISAT non è nullo
#Come modifico il comando precedente per visualizzare solo le righe che hanno valore nullo in COD_ISTAT? (False->...)

```

Essendo un codice amministrativo, possiamo imputarlo con la **moda**:

```python
df["COD_ISTAT"] = df["COD_ISTAT"].fillna(df["COD_ISTAT"].mode()[0])
#metto [0] perchè potremmo avere più mode (quanto più valori hanno la stessa frequenza massima)
```

### `ANNO_COLLO`

Per analisi statistiche possiamo lasciare i `NaN`, mentre per il machine learning conviene imputarli.

---

## 4.5 Rimozione duplicati

```python
print("Duplicati:", df.duplicated().sum())
df = df.drop_duplicates()
```

---

## 4.6 Uniformazione testo

Molto utile ripulire le stringhe:

```python
text_cols = ["TIPO", "LOCALITA", "UBICAZIONE", "OPERA"]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.upper()
    #fa 3 cose: converte ogni elemento della colonna in stringa, elimina spazi all'inizio e alla fine, converte in maiuscolo
```

Questo aiuta a evitare problemi tipo `"Cesena"` e `"CESENA"` trattati come categorie diverse.

---

# 5. Analisi statistica

## 5.1 Statistiche descrittive

```python
print(df.describe(include="all"))   #visualizza tutte le colonne (all)
```

Per le variabili numeriche possiamo anche fare:

```python
print(df[["OBJECTID", "COD_ISTAT", "ANNO_COLLO", "NUM_DOCU"]].describe())
"""
| Campo    | Significato                 |
| -------- | --------------------------- |
| `count`  | numero di valori non nulli  |
| `unique` | numero di valori distinti   |
| `top`    | valore più frequente (moda) |
| `freq`   | quante volte compare `top`  |
"""
```

Visualizzo il numero di documenti diviso per località:
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.countplot(data=df, x="LOCALITA")

plt.title("Numero di documenti per località")
plt.xlabel("Località")
plt.ylabel("Numero documenti")

plt.xticks(rotation=45)
plt.show()
```

---

## 5.2 Distribuzione dei tipi di monumento

```python
print(df["TIPO"].value_counts())    #conto le frequenzecon cui compaiono gli elementi della colonna TIPO
df["TIPO"].value_counts(normalize=True).head(3) #come prima ma visualizzo i valori normalizzati
(df["TIPO"].value_counts(normalize=True).head(3) * 100).round(2).astype(str) + "%"  #visualizza i valori nel formato 12.34%
(df["LOCALITA"].value_counts(normalize=True).sort_values(ascending=False).head(3) *100).round(2).astype(str) + "%" #come prima ma permette di inserire l'opzione di visualizzazione in senso ascendente o discendente
```

Nel dataset i tipi più frequenti sono:

* **LAPIDE**
* **MONUMENTO**
* **SCULTURA**
* **BUSTO**
* **CIPPO**

Questa è già una prima analisi di frequenza molto utile.  
Del risultato ottenuto possiamo estrarre i primi tre (```head(3)```) o gli ultimi 3 (```(tail(3)```).  


---

## 5.3 Distribuzione per località

```python
print(df["LOCALITA"].value_counts().head(10))
```
***Attenzione***: se non applicato il criterio del paragrafo 4.6 il risultato non è corretto perchè le maiuscole e le minuscole sono trattate diversamente. Devo quindi applicare la sostituzione:
```python
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.upper()
```


Dal file, la località dominante è **CESENA**, seguita da altre frazioni/località con frequenze molto più basse.  
Posso visualizzare i risultati in ordine inverso:
```python

```

---

## 5.4 Analisi degli anni di collocazione

```python
print(df["ANNO_COLLO"].describe())
print("Mediana anno:", df["ANNO_COLLO"].median())
print("Media anno:", df["ANNO_COLLO"].mean())
```

Qui è meglio usare la **mediana**, perché gli anni mancanti o eventuali anomalie possono influenzare la media.

---

## 5.5 Crosstab: tipo per località

```python
tab = pd.crosstab(df["LOCALITA"], df["TIPO"])
print(tab.head())
```
Visualizza una ```tabella di contingenza```, cioè una LOCALITA per ogni riga e un TIPO per ogni colonna: l'incrocio rappresenta quanti monumenti di quel tipo sono presenti in quella località.  
Oppure una vista più leggibile con percentuali:

```python
tab_pct = (pd.crosstab(df["LOCALITA"], df["TIPO"], normalize="index") * 100).round(2) + "%")
```

---

# 6. Visualizzazioni utili

```python
import matplotlib.pyplot as plt

df["TIPO"].value_counts().plot(kind="bar", figsize=(10,5), title="Distribuzione dei tipi di monumento")
plt.show()

df["LOCALITA"].value_counts().head(10).plot(kind="bar", figsize=(10,5), title="Top 10 località")
plt.show()

df["ANNO_COLLO"].dropna().plot(kind="hist", bins=20, figsize=(10,5), title="Distribuzione degli anni di collocazione")
plt.show()
```

---

# 7. Predizione con machine learning

## Obiettivo predittivo

Una buona scelta qui è prevedere la colonna **`TIPO`** del monumento a partire da:

* `LOCALITA`
* `UBICAZIONE`
* `OPERA`
* `ANNO_COLLO`
* `COD_ISTAT`

È un problema di **classificazione multiclass**.

---

## 7.1 Preparazione del target

Nel dataset ci sono alcune classi molto rare. Conviene raggruppare quelle con pochi esempi in `"ALTRO"`:

```python
counts = df["TIPO"].value_counts()
df["TIPO_GRP"] = df["TIPO"].where(df["TIPO"].map(counts) >= 5, "ALTRO")
```

Questo migliora la robustezza del modello.

---

## 7.2 Costruzione della pipeline

Usiamo:

* **OneHotEncoder** per variabili categoriche
* **TF-IDF** per il testo
* **SimpleImputer** per valori mancanti
* **RandomForestClassifier** come modello

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

X = df[["LOCALITA", "UBICAZIONE", "OPERA", "ANNO_COLLO", "COD_ISTAT"]]
y = df["TIPO_GRP"]

preprocessor = ColumnTransformer([
    ("loc", OneHotEncoder(handle_unknown="ignore"), ["LOCALITA"]),
    ("ubi", TfidfVectorizer(max_features=100, ngram_range=(1,2)), "UBICAZIONE"),
    ("opera", TfidfVectorizer(max_features=150, ngram_range=(1,2)), "OPERA"),
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ]), ["ANNO_COLLO", "COD_ISTAT"])
])

model = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    ))
])

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print("Accuracy per fold:", scores)
print("Accuracy media:", scores.mean())
```

---

## 7.3 Risultato ottenuto sul tuo dataset

Con questa impostazione, sul file caricato si ottiene una **accuracy media di circa 0.93**.

Questo è un risultato buono, ma va letto correttamente:

* il dataset è piccolo
* alcune classi sono molto dominanti
* i campi testuali (`OPERA`, `UBICAZIONE`) contengono molte informazioni utili per riconoscere il tipo

Quindi il modello funziona bene, ma non va interpretato come modello “industriale”: è soprattutto un **ottimo esercizio didattico** di pipeline reale.

---

# 8. Interpretazione dei risultati

## Cosa abbiamo imparato dal cleaning

* alcune colonne possono essere eliminate (`SHAPE`)
* gli zeri possono rappresentare missing “mascherati”
* la pulizia del testo è essenziale
* i codici mancanti vanno gestiti in modo coerente

## Cosa abbiamo imparato dall’analisi statistica

* il tipo prevalente è **LAPIDE**
* la località dominante è **CESENA**
* gli anni di collocazione hanno distribuzione irregolare
* il dataset è sbilanciato su alcune classi

## Cosa abbiamo imparato dal machine learning

* anche con un dataset piccolo si può costruire una pipeline seria
* i campi testuali aiutano molto nella classificazione
* la predizione del **tipo** è più sensata della predizione dell’**anno**, perché l’anno ha molti valori mancanti e variabilità elevata

---

# 9. Versione finale compatta del progetto

Ecco una versione ordinata, pronta da studiare o adattare:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

# 1. Lettura
df = pd.read_csv("OD_MONUMENTI_SDO_20260329181119.csv", sep=";")

# 2. Cleaning
df = df.drop(columns=["SHAPE"])
df["ANNO_COLLO"] = df["ANNO_COLLO"].replace(0, np.nan)
df["COD_ISTAT"] = df["COD_ISTAT"].fillna(df["COD_ISTAT"].mode()[0])
df = df.drop_duplicates()

text_cols = ["TIPO", "LOCALITA", "UBICAZIONE", "OPERA"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.upper()

# 3. Statistica descrittiva
print(df.describe(include="all"))
print(df["TIPO"].value_counts())
print(df["LOCALITA"].value_counts().head(10))
print(df["ANNO_COLLO"].describe())

# 4. Grafici
df["TIPO"].value_counts().plot(kind="bar", figsize=(10,5), title="Distribuzione TIPO")
plt.show()

df["LOCALITA"].value_counts().head(10).plot(kind="bar", figsize=(10,5), title="Top Località")
plt.show()

df["ANNO_COLLO"].dropna().plot(kind="hist", bins=20, figsize=(10,5), title="Distribuzione ANNO_COLLO")
plt.show()

# 5. Target raggruppato
counts = df["TIPO"].value_counts()
df["TIPO_GRP"] = df["TIPO"].where(df["TIPO"].map(counts) >= 5, "ALTRO")

# 6. ML
X = df[["LOCALITA", "UBICAZIONE", "OPERA", "ANNO_COLLO", "COD_ISTAT"]]
y = df["TIPO_GRP"]

preprocessor = ColumnTransformer([
    ("loc", OneHotEncoder(handle_unknown="ignore"), ["LOCALITA"]),
    ("ubi", TfidfVectorizer(max_features=100, ngram_range=(1,2)), "UBICAZIONE"),
    ("opera", TfidfVectorizer(max_features=150, ngram_range=(1,2)), "OPERA"),
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ]), ["ANNO_COLLO", "COD_ISTAT"])
])

model = Pipeline([
    ("prep", preprocessor),
    ("clf", RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    ))
])

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print("Accuracy media:", scores.mean())
print("Fold:", scores)
```

---

# 10. Conclusione

Questo è un buon esempio di **studio pandas completo**, perché contiene:

* **data cleaning reale**
* **analisi statistica descrittiva**
* **visualizzazione**
* **pipeline di machine learning**
* **valutazione del modello**
