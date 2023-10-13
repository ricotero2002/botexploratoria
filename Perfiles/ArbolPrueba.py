import pandas as pd
import warnings
from sklearn.preprocessing import LabelEncoder,MultiLabelBinarizer
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import graphviz
import joblib

warnings.filterwarnings("ignore", category=UserWarning)

df = pd.read_csv("C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrain.csv")

print(df.head())

df = df.drop('nombre', axis='columns')

# se paro los que son listas
df['generos'] = df['generos'].str.split(',')
df['Palabrasclaves'] = df['Palabrasclaves'].str.split(',')

#hago un one-hot para los que son listas
generos = MultiLabelBinarizer()
Palabrasclaves = MultiLabelBinarizer()
desarrollador = LabelEncoder()
generos_encoded = generos.fit_transform(df['generos'])
Palabrasclaves_encoded = Palabrasclaves.fit_transform(df['Palabrasclaves'])
desarrollador_encoded = desarrollador.fit_transform(df['desarrollador'])

#los paso al data frame
generos_df = pd.DataFrame(generos_encoded, columns=generos.classes_)
Palabrasclaves_df = pd.DataFrame(Palabrasclaves_encoded, columns=Palabrasclaves.classes_)
desarrollador_df = pd.DataFrame(desarrollador_encoded, columns=['desarrollador'])

# Elimino las columnas originales
df = df.drop(columns=['generos', 'Palabrasclaves', 'desarrollador'])

#concateno al data frame
df = pd.concat([df, generos_df, Palabrasclaves_df, desarrollador_df], axis=1)

#hago el onehot de el dataframe

df = pd.get_dummies(data=df, drop_first=True)
print(df)

#lo preparo para el arbol
y = df['LeGusta']
x = df.drop('LeGusta', axis='columns')

print(x.info())

#hago el arbol
modelo = DecisionTreeClassifier(max_depth=5)
modelo.fit(x,y)
print(modelo.score(x,y))


#agarro la data a consultar

df_testeo = pd.read_csv("C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTesteo.csv")

df_testeo = df_testeo.drop('nombre', axis='columns')

# se paro los que son listas
df_testeo['generos'] = df_testeo['generos'].str.split(',')
df_testeo['Palabrasclaves'] = df_testeo['Palabrasclaves'].str.split(',')

#hago un one-hot para los que son listas
generos_testeo = MultiLabelBinarizer()
Palabrasclaves_testeo = MultiLabelBinarizer()
desarrollador_testeo = LabelEncoder()
generos_testeo_encoded = generos_testeo.fit_transform(df_testeo['generos'])
Palabrasclaves_testeo_encoded = Palabrasclaves_testeo.fit_transform(df_testeo['Palabrasclaves'])
desarrollador_testeo_encoded = desarrollador_testeo.fit_transform(df_testeo['desarrollador'])

#los paso al data frame
generos_testeo_df = pd.DataFrame(generos_testeo_encoded, columns=generos_testeo.classes_)
Palabrasclaves_testeo_df = pd.DataFrame(Palabrasclaves_testeo_encoded, columns=Palabrasclaves_testeo.classes_)
desarrollador_testeo_df = pd.DataFrame(desarrollador_testeo_encoded, columns=['desarrollador'])

# Elimino las columnas originales
df_testeo = df_testeo.drop(columns=['generos', 'Palabrasclaves', 'desarrollador'])

#concateno al data frame
df_testeo = pd.concat([df_testeo, generos_testeo_df, Palabrasclaves_testeo_df, desarrollador_testeo_df], axis=1)

#hago el onehot de el dataframe

df_testeo = pd.get_dummies(data=df_testeo, drop_first=True)
print(df_testeo)

# necesito saber las features que faltan en el que vamos a predecir
training_features = list(x.columns)

# si falta alguno le pongo 0
for feature in training_features:
    if feature not in df_testeo.columns:
        df_testeo[feature] = 0

# si tengo un nuevo dato que no estan en el modelo que entrene lo borro
for feature in df_testeo.columns:
    if feature not in training_features:
        if feature in df_testeo.columns:
            df_testeo = df_testeo.drop(columns=[feature])

#predigo para esta nueva data
df_testeo = df_testeo[training_features]
result = modelo.predict(df_testeo)

for i in range(len(result)):
    print(i) #va de 0 a tamaño - 1
    print(result[i]) 

#lo grafico
dot_data = tree.export_graphviz(modelo, out_file=None, 
                        feature_names=x.columns.tolist(), 
                        class_names=df['LeGusta'].astype(str).unique().tolist(),
                        filled=True, rounded=True, 
                        special_characters=True)

graph = graphviz.Source(dot_data)
graph.render("arbolPreview")

# Guardar el modelo
joblib.dump(modelo, 'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/modelo_arbol_prueba.pkl')
# gaurdar transformaciones
joblib.dump(generos, 'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/generos_prueba.joblib')
joblib.dump(Palabrasclaves, 'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/Palabrasclaves_prueba.joblib')
joblib.dump(desarrollador, 'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/desarrollador_prueba.joblib')


# Cargar el modelo
# modelo = joblib.load('modelo_arbol.joblib')
# generos = joblib.load('generos_transformador.joblib')
# Palabrasclaves = joblib.load('Palabrasclaves_transformador.joblib')
# desarrollador = joblib.load('desarrollador_transformador.joblib')
# Aplicar transformaciones a las columnas para que queden iguales si tengo que actualizar el modelo
#df_testeo['generos'] = generos.transform(df_testeo['generos'])
#df_testeo['Palabrasclaves'] = Palabrasclaves.transform(df_testeo['Palabrasclaves'])
#df_testeo['desarrollador'] = desarrollador.transform(df_testeo['desarrollador'])