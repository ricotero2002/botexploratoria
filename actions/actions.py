# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

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

class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        return [ SessionStarted(), ActionExecuted("action_first"), ActionExecuted("action_listen")]
    
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
        fila = texto[texto['ID'] == Id]
        if not fila.empty: #tengo que cargar los slots
            print('Existia Valor')
            id_valor = fila['ID'].values[0]
            nombre_valor = fila['Nombre'].values[0]
            JuegosGustan_valor = ast.literal_eval(fila['JuegosGustan'].values[0])
            JuegosNoGustan_valor = ast.literal_eval(fila['JuegosNoGustan'].values[0])
            Categ_Gustan_valor = ast.literal_eval(fila['Categ_Gustan'].values[0])
            Categ_No_Gustan_valor = ast.literal_eval(fila['Categ_No_Gustan'].values[0])
            categorias = ast.literal_eval(fila['Categorias'].values[0])
            print(id_valor)
            print(nombre_valor)
            print(JuegosGustan_valor)
            print(JuegosNoGustan_valor)
            print(Categ_Gustan_valor)
            print(Categ_No_Gustan_valor)
            print(categorias)
        else: #tengo que crear el perfil
            print('No existia valor')
            nueva_fila = pd.DataFrame({'ID': [Id], 'Nombre': [user_name], 'JuegosGustan': [[]], 'JuegosNoGustan': [[]], 'Categ_Gustan': [[]], 'Categ_No_Gustan': [[]], 'Categorias': [[]]})
            # Concatenate the new row with the existing DataFrame
            texto = pd.concat([texto, nueva_fila], ignore_index=True)
            texto.to_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv', sep=';', index=False)
            JuegosGustan_valor = []
            JuegosNoGustan_valor = []
            categorias= []
        juegos= JuegosGustan_valor + JuegosNoGustan_valor
        ###################################################################
        respuesta = devolverJuegos(categorias)
        juego= random.choice(respuesta)
        imagen= devolverImagenes(juego)
        if nombre_valor:
            nombre= nombre_valor
        else:
            nombre=user_name
        message = f"Hola {nombre}, soy Luis Luis, mis amigos me llaman LuLu, para empezar te recomiendo el siguiente juego: {juego} y acordate que antes de irte te tenes que despedir"
        dispatcher.utter_message(text=message)
        image_path = f"{imagen}"
        print(image_path)
        dispatcher.utter_message(image=image_path)
        juegos.append(juego)

        return [SlotSet("id", Id), SlotSet("nombre", user_name), SlotSet("juegos", juegos), SlotSet("juegosGustan", JuegosGustan_valor), SlotSet("juegosNoGustan", JuegosNoGustan_valor), SlotSet("categorias", categorias)]
    
class ActionDevolverJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        categorias = tracker.get_slot("categorias")
        respuesta = devolverJuegos(categorias)
        juegos= tracker.get_slot("juegos")
        diferentesResultados= [item for item in respuesta if item not in juegos]
        juego=None
        image_path=None
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
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
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        if juego:
            juegos.append(juego)

        return [SlotSet("juegos", juegos)]
   
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
        diferentesResultados= [item for item in juegosParecidos if item not in juegosRecomendados]
        juego=None
        image_path=None
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
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
        return [SlotSet("juegos", juegosRecomendados)]

class ActionSetearCategorias(Action):
    def name(self) -> Text:
        return "action_setear_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados= tracker.get_slot("juegos")
        juegoAnterior= juegosRecomendados[-1]
        categorias= devolverCategorias(juegoAnterior)
        JuegosGustan= tracker.get_slot("juegosGustan")
        JuegosGustan.append(juegoAnterior)#juego que le gusto
        message = f"Me alegro que te haya gustado el juego {juegoAnterior}, lo tendre en cuenta entonces"
        dispatcher.utter_message(text=message)
        return [SlotSet("categorias", categorias), SlotSet("juegosGustan", JuegosGustan)] 

class ActionPreguntarCategorias(Action):
    def name(self) -> Text:
        return "action_preguntar_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados= tracker.get_slot("juegos")
        juegoAnterior= juegosRecomendados[-1]
        JuegosNoGustan= tracker.get_slot("juegosNoGustan")
        JuegosNoGustan.append(juegoAnterior)#juego que no le gusto
        categorias= devolverCategorias(juegoAnterior)
        imprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
        message = f"cual de las categorias del juego {juegoAnterior} no te gustaron? son las siguientes: {imprimir}"
        dispatcher.utter_message(text=message)
        return [SlotSet("juegosNoGustan", JuegosNoGustan)]
    
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
        return [SlotSet("categorias", categorias)]
    
class ActionDevolverJuegoEnBaseAJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego_en_base_a_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        latest_entities = tracker.latest_message.get('entities', [])
        juegos = [entity['value'] for entity in latest_entities if entity['entity'] == 'juego']
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
        return [SlotSet("juegos", juegosRecomendados)]

    
class ActionDevolverJuegoEnBaseACategoria(Action):
    def name(self) -> Text:
        return "action_devolver_juego_en_base_a_categoria"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        latest_entities = tracker.latest_message.get('entities', [])
        categorias = [entity['value'] for entity in latest_entities if entity['entity'] == 'categoria']
        categorias = [capitalize_first_char(item) for item in categorias]
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
        return [SlotSet("juegos", juegosRecomendados)]

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
        return [SlotSet("categorias", categoriasActuales)]

class ActionDevolverJuegoRandom(Action):
    def name(self) -> Text:
        return "action_devolver_juego_random"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        respuesta = devolverJuegos([])
        juegos= tracker.get_slot("juegos")
        diferentesResultados= [item for item in respuesta if item not in juegos]
        juego=None
        image_path=None
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego: {juego}"
            image_path = f"{imagen}"
        else:
            message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        if image_path:
            dispatcher.utter_message(image=image_path)
        if juego:
            juegos.append(juego)

        return [SlotSet("juegos", juegos)]

class ActionDevolverTodasLasCategorias(Action):
    def name(self) -> Text:
        return "action_devolver_todas_las_categorias"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        respuesta = devolverTodasLasCategorias()
        imprimir = ", ".join([f'"{categoria}"' for categoria in respuesta])
        message = f"Las categorias que conosco son: {imprimir}"
        dispatcher.utter_message(text=message)
        return []

class ActionGuardarPerfil(Action):
    def name(self) -> Text:
        return "action_guardar_Perfil"
    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        id= tracker.get_slot("id")
        nombre= tracker.get_slot("nombre")
        JuegosGustan= tracker.get_slot("juegosGustan")
        JuegosGustan = list(set(JuegosGustan)) #elimino repetidos
        JuegosNoGustan= tracker.get_slot("juegosNoGustan")
        JuegosNoGustan = list(set(JuegosNoGustan)) #elimino repetidos
        Categorias= tracker.get_slot("categorias")
        texto=pd.read_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv',sep=';')
        nueva_fila = {'ID': id, 'Nombre': nombre, 'JuegosGustan': JuegosGustan, 'JuegosNoGustan': JuegosNoGustan, 'Categ_Gustan': [], 'Categ_No_Gustan': [], 'Categorias': Categorias}
        print(texto)
        print(id)
        indice = texto.index[texto['ID'] == id].tolist() # Buscar el indice de la fila con el ID a reemplazar
        texto.loc[indice[0]] = nueva_fila # Reemplazar la fila en el DataFrame
        texto.to_csv('C:/Users/AGUSTIN/Documents/BotExploratoria/Perfiles/perfiles.csv', sep=';', index=False)     # Guardar el DataFrame actualizado de vuelta al archivo CSV
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
        return [SlotSet("nombre", nombre)]


