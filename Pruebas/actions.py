# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from operator import ge
import os
from asyncio import events
from cgitb import text
from typing import Any, Text, Dict, List
from urllib import response
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from swiplserver import PrologMQI
import random
import pandas as pd
import ast
import warnings
from sklearn.preprocessing import LabelEncoder,MultiLabelBinarizer
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
import graphviz
import joblib
import csv

def ExisteJuego(Juego) -> List[Text]:
    Juego=f"'{Juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"exist_juego({Juego}, Resultado)")
            lista = result[0]["Resultado"]
            print(result)
            # Convert the Prolog result to a Python list
            #result_list = [str(term) for term in result.("Resultado")]
    return lista

def ExisteCategoria(Categoria) -> List[Text]:
    Categoria=f'"{Categoria}"'
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"element_exists({Categoria}, Resultado)")
            lista = result[0]["Resultado"]
            print(result)
            # Convert the Prolog result to a Python list
            #result_list = [str(term) for term in result.("Resultado")]
    return lista

def devolverJuegos(categorias) -> List[Text]:
    # Convert Python list to Prolog list format, e.g., "[categoria1, categoria2, ...]"
    if not categorias:
        prolog_list= "[]"
    else:
        prolog_list = "[" + ", ".join([f'"{categoria}"' for categoria in categorias]) + "]"
    print(prolog_list)
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_juegos_con_categorias({prolog_list}, Resultado)")
            print(result)
            lista = result[0]["Resultado"]
            # Convert the Prolog result to a Python list
            #result_list = [str(term) for term in result.("Resultado")]
    return lista
   
def devolverCategorias(juego) -> List[Text]:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_categorias({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverPal_Claves(juego) -> List[Text]:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_Pal_Claves({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverDesarroladores(juego) -> Text:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_Desarrolador({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverImagenes(juego) -> Text:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_imagen({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverLink(juego) -> Text:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_link({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverSinopsis(juego) -> Text:
    quoted_word = f"'{juego}'"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_sinopsis({quoted_word}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def capitalize_first_char(text):
    words = text.split()
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def devolverTodasLasCategorias() -> List[Text]:
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"recuperar_todas_las_categorias(Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def imprimirJuegoUnico(juego) -> Text:
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            juego = f"'{juego}'"
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"imprimir_juego_unico({juego}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
    return lista

def devolverJuegosFormatoCSV(juegos) -> (pd.DataFrame, List[Text]):
    if not juegos:
        prolog_list= "[]"
    else:
        prolog_list = "[" + ", ".join([f"'{juegos}'" for juegos in juegos]) + "]"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query(f"imprimir_todos_los_juegos_excepto_nombres({prolog_list}, Resultado)")
            print("Resultado: ")
            print(result)
            lista = result[0]["Resultado"]
            print(lista)
            #------------------- probar
            nombres = []
            generos = []
            desarrollador = []
            palabras_claves = []

            # Itera sobre cada línea en result y extrae la información
            for linea in lista:
                partes = linea.split(';')
                nombres.append(partes[0])
                generos.append(partes[1])
                desarrollador.append(partes[2])
                palabras_claves.append(partes[3])

            # Crea el DataFrame a este le tengo que hacer todo el laburito
            df_testeo = pd.DataFrame({
                'nombre': nombres,
                'generos': generos,
                'desarrollador': desarrollador,
                'Palabrasclaves': palabras_claves
            })
            df_original = df_testeo
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


            # dataframe_resultante, lista_texto_resultante = devolverJuegosFormatoCSV(juegos)  / como llamar a la funcion

    return df_testeo, lista

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        return [ SessionStarted(), ActionExecuted("action_listen")]
    
class ActionPrimerJuego(Action):
    def name(self) -> Text:
        return "action_first"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        input_data=tracker.latest_message
        user_name=input_data["metadata"]["message"]["from"]["first_name"]
        Id=input_data["metadata"]["message"]["from"]["id"]
        ############ cargar perfil
        texto=pd.read_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv',sep=';')
        print(texto)
        habia_archivo= False
        fila = texto[texto['ID'] == Id]
        if not fila.empty: #tengo que cargar los slots
            habia_archivo = True
            print('Existia Valor')
            id_valor = fila['ID'].values[0]
            nombre_valor = fila['Nombre'].values[0]
            categorias = ast.literal_eval(fila['Categorias'].values[0])
            print(id_valor)
            print(nombre_valor)
            print(categorias)
            direccion = f'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrainUsuarios/data_{Id}.csv'
            df=pd.read_csv(direccion,sep=';')
            juegos = []
            for nombre in df['nombre']: #me traigo todos los juegos ya recomendados
                juegos.append(nombre)
            if len(juegos) > 7:
                usarArbol = True
            else:
                usarArbol = False
        else: #tengo que crear el perfil
            print('No existia valor')
            usarArbol = False
            nueva_fila = pd.DataFrame({'ID': [Id], 'Nombre': [user_name], 'Categorias': [[]]})
            # Concatenate the new row with the existing DataFrame
            texto = pd.concat([texto, nueva_fila], ignore_index=True)
            texto.to_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv', sep=';', index=False)
            # Crear un DataFrame vacío con columnas especificadas
            columnas = ['nombre', 'generos', 'desarrollador', 'Palabrasclaves', 'LeGusta']
            df = pd.DataFrame(columns=columnas)
            # Guardar el DataFrame en una dirección
            direccion = f'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrainUsuarios/data_{Id}.csv'
            df.to_csv(direccion, sep=';', index=False)
            categorias= []
            juegos = []
        ################################################################### ahora ver si uso el arbol o no
        if usarArbol: #osea true
            df_juegos, csv_juegos = devolverJuegosFormatoCSV(juegos)
            direccion = f'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrainUsuarios/x_{Id}.csv'
            x=pd.read_csv(direccion,sep=';')
            # necesito saber las features que faltan en el que vamos a predecir
            training_features = list(x.columns)

            # si falta alguno le pongo 0
            for feature in training_features:
                if feature not in df_juegos.columns:
                    df_juegos[feature] = 0

            # si tengo un nuevo dato que no estan en el modelo que entrene lo borro
            for feature in df_juegos.columns:
                if feature not in training_features:
                    if feature in df_juegos.columns:
                        df_juegos = df_juegos.drop(columns=[feature])
            df_juegos = df_juegos[training_features]
            #traigo arbol
            direccion = f"C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/arbol_{Id}.pkl"
            modelo = joblib.load(direccion)
            result = modelo.predict(df_juegos)
            print("predije esto pa")
            print(result)
            print("los nombres")
            print(csv_juegos)
            # me quedo con los juegos que predicen bien
            print(len(result))
            print(len(csv_juegos))
            j = 0
            for i in range(len(result)):
                if result[i] == 0:
                    csv_juegos.pop(j)
                else:
                    j += 1
                print(i)
                print(j)
            print(csv_juegos)
            print(len(csv_juegos))
            if len(csv_juegos) > 0:
                nro = random.randint(0, len(csv_juegos) - 1)
                juegocsv = csv_juegos.pop(nro)
                # Dividir la cadena usando la coma como delimitador
                partes = juegocsv.split(';')
                # Obtener el primer elemento de la lista
                juego = partes[0]
            else:
                usarArbol = False
                respuesta = devolverJuegos(categorias)
                juego= random.choice(respuesta) 
        else:
            respuesta = devolverJuegos(categorias)
            juego= random.choice(respuesta)
        
        if usarArbol:
            juegosActuales = [juegocsv]
        else:
            juegosActuales = []
            csv_juegos = []
            csv = imprimirJuegoUnico(juego)
            print("Aca papa")
            print(csv)
            juegosActuales.append(csv)
            print(csv_juegos)
        imagen= devolverImagenes(juego)
        if habia_archivo:
            nombre= nombre_valor
        else:
            nombre=user_name
        message = f"Hola {nombre}, soy Luis Luis, mis amigos me llaman LuLu, para empezar te recomiendo el siguiente juego: {juego} y acordate que antes de irte te tenes que despedir"
        dispatcher.utter_message(text=message)
        image_path = f"{imagen}"
        print(image_path)
        dispatcher.utter_message(image=image_path)
        juegos.append(juego)
        print(csv_juegos)
        tracker.slots["id"] = Id
        tracker.slots["nombre"] = user_name
        tracker.slots["juegos"] = juegos
        tracker.slots["usarArbol"] = usarArbol
        tracker.slots["categorias"] = categorias
        tracker.slots["juegosSesionActual"] = juegosActuales
        tracker.slots["juegosTipoCSV"] = csv_juegos
        tracker.slots["FueChau"] = False
        return []
    
class ActionDevolverJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        usarArbol = tracker.get_slot("usarArbol")
        juegos= tracker.get_slot("juegos")
        csv_juegos = tracker.get_slot("juegosTipoCSV")
        juegosSesionActual = tracker.get_slot("juegosSesionActual")
        if len(csv_juegos) == 0:
            usarArbol=False
        if usarArbol:
            nro = random.randint(0, len(csv_juegos) - 1)
            juegocsv = csv_juegos.pop(nro)
            partes = juegocsv.split(';')
            resultado = partes[0]
            juego = f"'{resultado}'"
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego: {juego},"
            image_path = f"{imagen}"
            juegosSesionActual.append(juegocsv)
        else:
            categorias = tracker.get_slot("categorias")
            respuesta = devolverJuegos(categorias)
            diferentesResultados= [item for item in respuesta if item not in juegos]
            juego=None
            image_path=None
            if diferentesResultados:
                juego= random.choice(diferentesResultados)
                csv = imprimirJuegoUnico(juego)
                juegosSesionActual.append(csv)
                imagen= devolverImagenes(juego)
                message = f"Entonces te puedo recomendar el siguiente juego: {juego},"
                image_path = f"{imagen}"
            else:
                categoriasIgnoradas= []
                while not diferentesResultados and categorias:     
                    last_element = categorias[-1]  # Get the last element
                    categoriasIgnoradas.append(last_element)
                    categorias.pop()  # Remove the last element from the list
                    respuesta = devolverJuegos(categorias)
                    diferentesResultados= [item for item in respuesta if item not in juegos]
                if diferentesResultados:
                    imprimir = ", ".join([f'"{categoria}"' for categoria in categoriasIgnoradas])
                    juego= random.choice(diferentesResultados)
                    imagen= devolverImagenes(juego)
                    image_path = f"{imagen}"
                    message = f"no tengo mas juego de los que te gustan a vos, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
                    csv = imprimirJuegoUnico(juego)
                    juegosSesionActual.append(csv)
                else:
                    message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        if juego:
            juegos.append(juego)
        tracker.slots["juegos"] = juegos
        tracker.slots["juegosSesionActual"] = juegosSesionActual
        tracker.slots["juegosTipoCSV"] = csv_juegos
        tracker.slots["FueChau"] = False
        return []
   
class ActionDevolverCategorias(Action):
    def name(self) -> Text:
        return "action_devolver_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegos= tracker.get_slot("juegos")
        juego= juegos[-1]
        categorias= devolverCategorias(juego)
        imprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
        message = f"las categorias del juego {juego} son: {imprimir}"
        dispatcher.utter_message(text=message)
        tracker.slots["FueChau"] = False
        return []

class ActionDevolverLink(Action):
    def name(self) -> Text:
        return "action_devolver_link"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegos= tracker.get_slot("juegos")
        juego= juegos[-1]
        link= devolverLink(juego)
        message = f"el link de compra del juego {juego} es: {link}"
        dispatcher.utter_message(text=message)
        tracker.slots["FueChau"] = False
        return []
    
class ActionDevolverSinopsis(Action):
    def name(self) -> Text:
        return "action_devolver_sinopsis"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegos= tracker.get_slot("juegos")
        juego= juegos[-1]
        link= devolverSinopsis(juego)
        message = f"la sinopsis del juego {juego} es: {link}"
        dispatcher.utter_message(text=message)
        tracker.slots["FueChau"] = False
        return []
    
class ActionDevolverJuegoParecido(Action):
    def name(self) -> Text:
        return "action_devolver_juego_parecido"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados= tracker.get_slot("juegos")
        juegoAnterior= juegosRecomendados[-1]
        categorias= devolverCategorias(juegoAnterior)
        juegosParecidos= devolverJuegos(categorias)
        juegosSesionActual = tracker.get_slot("juegosSesionActual")

        diferentesResultados= [item for item in juegosParecidos if item not in juegosRecomendados]
        juego=None
        image_path=None
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
            csv = imprimirJuegoUnico(juego)
            juegosSesionActual.append(csv)
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego que es parecido a {juegoAnterior}: {juego}"
            image_path = f"{imagen}"
        else:
            categoriasIgnoradas= []
            while not diferentesResultados and categorias:     
                last_element = categorias[-1]  # Get the last element
                categoriasIgnoradas.append(last_element)
                categorias.pop()  # Remove the last element from the list
                respuesta = devolverJuegos(categorias)
                diferentesResultados= [item for item in respuesta if item not in juegosRecomendados]
            if diferentesResultados:
                imprimir = ", ".join([f'"{categoria}"' for categoria in categoriasIgnoradas])
                juego= random.choice(diferentesResultados)
                csv = imprimirJuegoUnico(juego)
                juegosSesionActual.append(csv)
                imagen= devolverImagenes(juego)
                image_path = f"{imagen}"
                message = f"no tengo mas juegos parecidos a {juegoAnterior}, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        if juego:
            juegosRecomendados.append(juego)
        tracker.slots["juegos"] = juegosRecomendados
        tracker.slots["juegosSesionActual"] = juegosSesionActual
        tracker.slots["FueChau"] = False
        return []

class ActionSetearCategorias(Action):
    def name(self) -> Text:
        return "action_setear_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados = tracker.get_slot("juegosSesionActual")
        print("que paso ahora")
        print(juegosRecomendados)
        juegoAnterior= juegosRecomendados[-1]
        juegos= tracker.get_slot("juegos")
        juego= juegos[-1]
        categorias= devolverCategorias(juego)
        JuegosGustan= tracker.get_slot("juegosGustan")
        if juegoAnterior not in JuegosGustan:
            JuegosGustan.append(juegoAnterior) #juego que le gusto
        message = f"Me alegro que te haya gustado el juego {juego}, lo tendre en cuenta entonces"
        dispatcher.utter_message(text=message)
        tracker.slots["categorias"] = categorias
        tracker.slots["juegosGustan"] = JuegosGustan
        tracker.slots["FueChau"] = False
        return [] 

class ActionPreguntarCategorias(Action):
    def name(self) -> Text:
        return "action_preguntar_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados= tracker.get_slot("juegosSesionActual")
        juegoAnterior= juegosRecomendados[-1]
        JuegosNoGustan= tracker.get_slot("juegosNoGustan")
        if juegoAnterior not in JuegosNoGustan:
            JuegosNoGustan.append(juegoAnterior)#juego que no le gusto
        juegos= tracker.get_slot("juegos")
        juego= juegos[-1]
        categorias= devolverCategorias(juego)
        imprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
        message = f"cual de las categorias del juego {juego} no te gustaron? son las siguientes: {imprimir}"
        dispatcher.utter_message(text=message)
        tracker.slots["juegosNoGustan"] = JuegosNoGustan
        tracker.slots["FueChau"] = False
        return []
    
class ActionBorrarCategorias(Action):
    def name(self) -> Text:
        return "action_borrar_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get the entities from the last user message
        latest_entities = tracker.latest_message.get('entities', [])
        # Filter the entities based on the entity name
        categoriasNoLeGustan = [entity['value'] for entity in latest_entities if entity['entity'] == 'categoria']
        categoriasNoLeGustan = [capitalize_first_char(item) for item in categoriasNoLeGustan]
        for valor in categoriasNoLeGustan: #reviso que las categorias existan
            resultado= ExisteCategoria(valor)
            if resultado != "true":
                categoriasNoLeGustan.remove(valor)
        categoriasActuales= tracker.get_slot("categorias")
        categorias= [item for item in categoriasActuales if item not in categoriasNoLeGustan]
        if categoriasNoLeGustan:
            imprimir = ", ".join([f'"{categoria}"' for categoria in categoriasNoLeGustan])
            message = f"entonces las categorias que no te gustan son las siguientes: {imprimir}, lo voy a tener en cuenta"
        else:
            message = f"gracias por la data pero igual no conosco esas categorias jejeje"
        dispatcher.utter_message(text=message)
        tracker.slots["categorias"] = categorias
        tracker.slots["FueChau"] = False
        return []
    
class ActionDevolverJuegoEnBaseAJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego_en_base_a_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        latest_entities = tracker.latest_message.get('entities', [])
        juegos = [entity['value'] for entity in latest_entities if entity['entity'] == 'juego']
        juegosSesionActual = tracker.get_slot("juegosSesionActual")
        juegos = [capitalize_first_char(item) for item in juegos]
        juegosRecomendados= tracker.get_slot("juegos")
        juegosRecomendados = [capitalize_first_char(item) for item in juegosRecomendados]
        for valor in juegos: #reviso que las categorias existan
            resultado= ExisteJuego(valor)
            if resultado != "true":
                juegos.remove(valor)
        image_path=None
        if juegos:
            juego = juegos[-1]
            juegoBase=juego
            juegosRecomendados.append(juegoBase)
            categorias= devolverCategorias(juego)
            juegosParecidos= devolverJuegos(categorias)
            juegosPosibles= [item for item in juegosParecidos if item not in juegosRecomendados]
            juegoADecir=None
            if juegosPosibles:
                juegoADecir= random.choice(juegosPosibles)
                csv = imprimirJuegoUnico(juegoADecir)
                juegosSesionActual.append(csv)
                imagen= devolverImagenes(juegoADecir)
                message = f"Entonces te puedo recomendar el siguiente juego: {juegoADecir}, debido a su parecido con: {juego}"
                image_path = f"{imagen}"
            else:
                categoriasIgnoradas= []
                while not juegosPosibles and categorias:     
                    last_element = categorias[-1]  # Get the last element
                    categoriasIgnoradas.append(last_element)
                    categorias.pop()  # Remove the last element from the list
                    respuesta = devolverJuegos(categorias)
                    juegosPosibles= [item for item in respuesta if item not in juegosRecomendados]
                if juegosPosibles:
                    imprimir = ", ".join([f'"{categoria}"' for categoria in categoriasIgnoradas])
                    juego= random.choice(juegosPosibles)
                    csv = imprimirJuegoUnico(juego)
                    juegosSesionActual.append(csv)
                    imagen= devolverImagenes(juego)
                    image_path = f"{imagen}"
                    message = f"no tengo mas juegos parecidos a {juegoBase}, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
                else:
                    message = f"ya te recomende todos los juegos flaquito juga alguno"
            juegosRecomendados.append(juegoADecir)
            juegosRecomendados.remove(juegoBase)
        else:
            message = f"Disculpa no conosco este juego"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        tracker.slots["juegos"] = juegosRecomendados
        tracker.slots["juegosSesionActual"] = juegosSesionActual
        tracker.slots["FueChau"] = False
        return []

    
class ActionDevolverJuegoEnBaseACategoria(Action):
    def name(self) -> Text:
        return "action_devolver_juego_en_base_a_categoria"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        latest_entities = tracker.latest_message.get('entities', [])
        categorias = [entity['value'] for entity in latest_entities if entity['entity'] == 'categoria']
        categorias = [capitalize_first_char(item) for item in categorias]
        juegosSesionActual = tracker.get_slot("juegosSesionActual")
        categorias = list(set(categorias)) #elimino repetidos
        for valor in categorias: #reviso que las categorias existan
            resultado= ExisteCategoria(valor)
            if resultado != "true":
                categorias.remove(valor)
        image_path=None
        juegoADecir= None
        juegosRecomendados= tracker.get_slot("juegos")
        if categorias:
            categorias= categorias[:3] #limito categorias a 3
            juegosParecidos= devolverJuegos(categorias)
            juegosPosibles= [item for item in juegosParecidos if item not in juegosRecomendados]
            juegoADecir=None
            if juegosPosibles:
                Categoriasimprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
                juegoADecir= random.choice(juegosPosibles)
                csv = imprimirJuegoUnico(juegoADecir)
                juegosSesionActual.append(csv)
                imagen= devolverImagenes(juegoADecir)
                message = f"Entonces te puedo recomendar el siguiente juego: {juegoADecir}, debido a las categorias{Categoriasimprimir}"
                image_path = f"{imagen}"
            else:
                categoriasIgnoradas= []
                while not juegosPosibles and categorias:  
                    last_element = categorias[-1]  # Get the last element
                    categoriasIgnoradas.append(last_element)
                    categorias.pop()  # Remove the last element from the list
                    respuesta = devolverJuegos(categorias)
                    juegosPosibles= [item for item in respuesta if item not in juegosRecomendados]
                if juegosPosibles:
                    CategoriasBorradas = ", ".join([f'"{categoria}"' for categoria in categoriasIgnoradas])
                    CategoriasUsadas = ", ".join([f'"{categoria}"' for categoria in categorias])
                    juegoADecir= random.choice(juegosPosibles)
                    csv = imprimirJuegoUnico(juegoADecir)
                    juegosSesionActual.append(csv)
                    imagen= devolverImagenes(juegoADecir)
                    image_path = f"{imagen}"
                    message = f"no tengo mas con las categorias {CategoriasBorradas}, por lo que tome en cuenta las siguientes:{CategoriasUsadas} y te recomiendo en su lugar: {juegoADecir}"
                else:
                    message = f"ya te recomende todos los juegos flaquito juga alguno"
        else:
            message = f"Disculpa no conosco esa categoria"

        dispatcher.utter_message(text=message)
        if image_path: 
            dispatcher.utter_message(image=image_path)
        if juegoADecir:
            juegosRecomendados.append(juegoADecir)
        tracker.slots["juegos"] = juegosRecomendados
        tracker.slots["juegosSesionActual"] = juegosSesionActual
        tracker.slots["FueChau"] = False
        return []

class ActionPonerCategorias(Action):
    def name(self) -> Text:
        return "action_poner_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        latest_entities = tracker.latest_message.get('entities', [])
        categoriasEntidades = [entity['value'] for entity in latest_entities if entity['entity'] == 'categoria']
        categoriasEntidades = list(set(categoriasEntidades)) #elimino repetidos
        categoriasEntidades = [capitalize_first_char(item) for item in categoriasEntidades]
        categoriasActuales= tracker.get_slot("categorias")
        for valor in categoriasEntidades:
            resultado= ExisteCategoria(valor)
            if resultado != "true":
                categoriasEntidades.remove(valor)
        categorias= [item for item in categoriasEntidades if item not in categoriasActuales]
        if categorias:
            tamanioActuales=len(categoriasActuales)
            tamanioDif=len(categorias)
            if tamanioDif >3:
                tamanioDif=3
            indice=tamanioDif + tamanioActuales
            if indice > 3:
                indice=3
            while len(categoriasActuales) < indice: #pongo elementos vacios para poder hacer categoriasaActuales[i]
                categoriasActuales.append(None)
            print(tamanioActuales)
            print(tamanioDif)
            print(categoriasActuales)
            print(categorias)

            while (indice != 0) and (tamanioDif != 0):
                indice -= 1
                tamanioDif -= 1
                print(indice)
                print(tamanioDif)
                categoriasActuales[indice] = categorias[tamanioDif]
            message = f"voy a tener encuenta que te gustan esas categorias entonces"
        else:
            message = f"Disculpa no conosco esa categoria o ya se que te gusta nose una de 2"
        print(categoriasEntidades)
        print(categoriasActuales)            
        dispatcher.utter_message(text=message)
        tracker.slots["categorias"] = categoriasActuales
        tracker.slots["FueChau"] = False
        return []

class ActionDevolverJuegoRandom(Action):
    def name(self) -> Text:
        return "action_devolver_juego_random"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        respuesta = devolverJuegos([])
        juegos= tracker.get_slot("juegos")
        juegosSesionActual = tracker.get_slot("juegosSesionActual")
        diferentesResultados= [item for item in respuesta if item not in juegos]
        juego=None
        image_path=None
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego: {juego}"
            image_path = f"{imagen}"
            csv = imprimirJuegoUnico(juego)
            juegosSesionActual.append(csv)
        else:
            message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        if juego:
            juegos.append(juego)
        tracker.slots["juegos"] = juegos
        tracker.slots["juegosSesionActual"] = juegosSesionActual
        tracker.slots["FueChau"] = False
        return []

def guardar_perfil(id, nombre, Categorias, JuegosGustan, JuegosNoGustan):
    # Guardar perfil
    texto = pd.read_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv', sep=';')
    nueva_fila = {'ID': id, 'Nombre': nombre, 'Categorias': Categorias}
    indice = texto.index[texto['ID'] == id].tolist()
    texto.loc[indice[0]] = nueva_fila
    texto.to_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv', sep=';', index=False)

    # Guardar juegos que gustan y no gustan
    direccion = f'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrainUsuarios/data_{id}.csv'
    df = pd.read_csv(direccion, sep=';')
    for juegoGusta in JuegosGustan:
        partes = juegoGusta.split(';')
        nombre = partes[0]
        generos = partes[1]
        desarrollador = partes[2]
        Palabrasclaves = partes[3]
        nueva_fila = pd.Series({'nombre': nombre, 'generos': generos, 'desarrollador': desarrollador, 'Palabrasclaves': Palabrasclaves, 'LeGusta': 1})
        df.loc[len(df.index)] = nueva_fila

    for juegoNoGusta in JuegosNoGustan:
        partes = juegoNoGusta.split(';')
        nombre = partes[0]
        generos = partes[1]
        desarrollador = partes[2]
        Palabrasclaves = partes[3]
        nueva_fila = pd.Series({'nombre': nombre, 'generos': generos, 'desarrollador': desarrollador, 'Palabrasclaves': Palabrasclaves, 'LeGusta': 0})
        df.loc[len(df.index)] = nueva_fila

    df.to_csv(direccion, sep=';', index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    # Generar el árbol
    df = df.drop('nombre', axis='columns')
    df['generos'] = df['generos'].str.split(',')
    df['Palabrasclaves'] = df['Palabrasclaves'].str.split(',')

    generos = MultiLabelBinarizer()
    Palabrasclaves = MultiLabelBinarizer()
    desarrollador = LabelEncoder()

    generos_encoded = generos.fit_transform(df['generos'])
    Palabrasclaves_encoded = Palabrasclaves.fit_transform(df['Palabrasclaves'])
    desarrollador_encoded = desarrollador.fit_transform(df['desarrollador'])

    generos_df = pd.DataFrame(generos_encoded, columns=generos.classes_)
    Palabrasclaves_df = pd.DataFrame(Palabrasclaves_encoded, columns=Palabrasclaves.classes_)
    desarrollador_df = pd.DataFrame(desarrollador_encoded, columns=['desarrollador'])

    df = df.drop(columns=['generos', 'Palabrasclaves', 'desarrollador'])
    df = pd.concat([df, generos_df, Palabrasclaves_df, desarrollador_df], axis=1)
    df = pd.get_dummies(data=df, drop_first=True)

    y = df['LeGusta']
    x = df.drop('LeGusta', axis='columns')

    modelo = DecisionTreeClassifier(max_depth=5)
    modelo.fit(x,y)

    direccion = f"C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/ArbolesPersonalisados/arbol_{id}.pkl"
    joblib.dump(modelo, direccion)
    direccion = f'C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/DataTrainUsuarios/x_{id}.csv'
    x.to_csv(direccion, sep=';', index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    return 

class ActionGuardarPerfil(Action):
    def name(self) -> Text:
        return "action_guardar_Perfil"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        #guardo perfil
        id= tracker.get_slot("id")
        nombre= tracker.get_slot("nombre")
        Categorias= tracker.get_slot("categorias")
        #guardo juegos que gustan y no
        JuegosGustan= tracker.get_slot("juegosGustan")
        JuegosNoGustan= tracker.get_slot("juegosNoGustan")
        guardar_perfil(id,nombre,Categorias,JuegosGustan,JuegosNoGustan)
        tracker.slots["FueChau"] = True
        return []
    
class ActionCambiarNombre(Action):
    def name(self) -> Text:
        return "action_cambiar_nombre"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        latest_entities = tracker.latest_message.get('entities', [])
        nuevoNombre = [entity['value'] for entity in latest_entities if entity['entity'] == 'username']
        if nuevoNombre:
            nombre=nuevoNombre
        else:
            nombre= tracker.get_slot("nombre")
        message = f"Bueno entonces te voy a llamar {nombre}"
        dispatcher.utter_message(text=message)
        tracker.slots["nombre"] = nombre
        tracker.slots["FueChau"] = False
        return []

