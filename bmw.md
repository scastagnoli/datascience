## Esempio analisi dati 
Sorgente dati: https://www.kaggle.com/datasets/mhassansaboor/bmw-stock-data-1996-2024

### Caricamento dati e prime analisi
```python
import pandas as pd
df = pd.read_csv("bmw_global_sales_2018_2025.csv")

#visualizzo le prime righe del dataframe
print(df.head())

#visualizzo la struttura del dataframe
print(df.info())

#visualizzo le statistiche di base
print(df.describe(include='all'))

#visualizzo una sintesi dei valori NaN
print(df.isnull().sum())

#visualizzo evenutuali righe completamente vuote
empty_rows = df.isnull().all(axis=1)

#cancello le righe completamente vuote
df = df.dropna(how='all')
#se non specificassimo 'all' il valore di default sarebbe 'any', cioè la riga verrebbe cancellata anche se solo uno dei valori della riga fosse NaN

#sostituisco i valori NaN con la mediana

#l'uso della mediana al posto della media è vantaggioso per le seguenti ragioni:
#   1 - è meno influenzata dai valori estremi e outlier (valori che si discostano molto dalla norma del dataset)
#   2 - la distribuzione rimane più stabile perchè non inseriamo un valore "artificiale" come può accadere con la media, ma inseriamo un valore del dataset, quindi abbiamo meno distorsioni e errori sistematici (bias)
df['Revenue_EUR'] = df['Revenue_EUR'].fillna(df['Revenue_EUR'].median())
#ancora meglio nel nostro caso sarebbe usare la mediana per gruppo
df['Revenue_EUR'] = df.groupby('Region')['Revenue_EUR'].transform(
    lambda x: x.fillna(x.median())
)

#rimuovo i duplicati
df = df.drop_duplicates()

#individuazione degli outlier
Q1 = df['Units_Sold'].quantile(0.25)
Q3 = df['Units_Sold'].quantile(0.75)
IQR = Q3 - Q1   #calcolo l'intervallo interquartile
#applico la regola di Tukey per individuare gli outlier: 
#Q1 - 1.5 * IQR   # limite inferiore
#Q3 + 1.5 * IQR   # limite superiore
#costruisco una maschera booleana che identifica i valori non outlier (validi)
df = df[
    (df['Units_Sold'] >= Q1 - 1.5 * IQR) & 
    (df['Units_Sold'] <= Q3 + 1.5 * IQR)
    ]

#Esempio semplice  di individuazione degli outlier:
import pandas as pd

# Dati di esempio
sales = pd.Series([10, 12, 13, 14, 15, 16, 100])

# Quartili
Q1 = sales.quantile(0.25)
Q3 = sales.quantile(0.75)
IQR = Q3 - Q1

# Limiti Tukey
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Maschera (True = valore normale, False = outlier)
mask = (sales >= lower_bound) & (sales <= upper_bound)

# Risultati
print("Valori originali:\n", sales)
print("\nQ1:", Q1, "Q3:", Q3, "IQR:", IQR)
print("Limiti:", lower_bound, "-", upper_bound)

print("\nMaschera (True = ok, False = outlier):\n", mask)

print("\nValori filtrati (senza outlier):\n", sales[mask])
print("\nOutlier:\n", sales[~mask])
#Fine esempio semplice

#Analisi statistiche
df['Units_Sold'].describe()

#vendite (unità vendute) raggruppate per anno
sales_by_year = df.groupby('Year')['Units_Sold'].sum()
print(sales_by_year)

#vendite per regione
sales_by_region = df.groupby('Region')['Units_Sold'].sum().sort_values(ascending=False)

#vendite per modello
sales_by_model = df.groupby('Model')['Units_Sold'].sum().sort_values(ascending=False)

#crescita anno su anno
sales_by_year = sales_by_year.sort_index()
#sort_index() usa come indice Year perchè abbiamo fatto groupby('Year')
growth = sales_by_year.pct_change() * 100
#spiegazione di pct_change()
#calcola il rapporto (x(t)-x(t-1))/x(t-1)
#diff() calcolerebbe la differenza assoluta
import pandas as pd

sales_by_year = pd.Series(
    [100, 120, 90, 150],
    index=[2018, 2019, 2020, 2021]
)

growth = sales_by_year.pct_change()
print(growth)
#fine spiegazione pct_change()

print(growth)

#studio le correlazioni
import seaborn as sns
import matplotlib.pyplot as plt

corr = df.corr(numeric_only=True)

sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

#grafico 1
sns.lineplot(data=df, x='Year', y='Units_Sold', estimator='sum')
#estimator è la funzione di aggregazione che applichiamo ai dati raggruppati per Year
plt.title("Trend Vendite Globali")
plt.show()

#grafico 2
sns.lineplot(data=df, x='Year', y='Units_Sold', hue='Region', estimator='sum', errorbar=None)
plt.title("Vendite per Regione nel Tempo")
plt.show()

```

