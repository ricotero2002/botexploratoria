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
        categorias = []
        respuesta = devolverJuegos(categorias)
        juego= random.choice(respuesta)
        imagen= devolverImagenes(juego)
        message = f"Hola, soy luis luis, para empezar te recomiendo el siguiente juego: {juego}, te gusta?"
        dispatcher.utter_message(text=message)
        image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
        dispatcher.utter_message(image=image_path)
        juegos= []
        juegos.append(juego)

        return [SlotSet("juegos", juegos)]
    
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
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego: {juego}"
            image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
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
                image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
                message = f"no tengo mas juego de los que te gustan a vos, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        dispatcher.utter_message(image=image_path)
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
        if diferentesResultados:
            juego= random.choice(diferentesResultados)
            imagen= devolverImagenes(juego)
            message = f"Entonces te puedo recomendar el siguiente juego que es parecido a {juegoAnterior}: {juego}"
            image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
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
                image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
                message = f"no tengo mas juegos parecidos a {juegoAnterior}, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        dispatcher.utter_message(image=image_path)
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
        message = f"Me alegro que te haya gustado el juego {juegoAnterior}, lo tendre en cuenta entonces"
        dispatcher.utter_message(text=message)
        return [SlotSet("categorias", categorias)]

class ActionPreguntarCategorias(Action):
    def name(self) -> Text:
        return "action_preguntar_categorias"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juegosRecomendados= tracker.get_slot("juegos")
        juegoAnterior= juegosRecomendados[-1]
        categorias= devolverCategorias(juegoAnterior)
        imprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
        message = f"cual de las categorias del juego {juegoAnterior} no te gustaron? son las siguientes: {imprimir}"
        dispatcher.utter_message(text=message)
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
        categoriasActuales= tracker.get_slot("categorias")
        categorias= [item for item in categoriasActuales if item not in categoriasNoLeGustan]
        imprimir = ", ".join([f'"{categoria}"' for categoria in categoriasNoLeGustan])
        message = f"entonces las categorias que no te gustan son las siguientes: {imprimir}, lo voy a tener en cuenta"
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
        juego = juegos[-1]
        categorias= devolverCategorias(juego)
        juegosParecidos= devolverJuegos(categorias)
        juegosRecomendados= tracker.get_slot("juegos")
        juegosPosibles= [item for item in juegosParecidos if item not in juegosRecomendados]
        juegoADecir=None
        if juegosPosibles:
            juegoADecir= random.choice(juegosPosibles)
            imagen= devolverImagenes(juegoADecir)
            message = f"Entonces te puedo recomendar el siguiente juego: {juegoADecir}, debido a su parecido con: {juego}"
            image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
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
                image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
                message = f"no tengo mas juegos parecidos a {juego}, tuve que ignorar las siguientes categorias: {imprimir}, que tal este para cambiar un poco: {juego}"
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"
            
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(image=image_path)
        juegosRecomendados.append(juegoADecir)
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
        categorias= categorias[:3]
        juegosParecidos= devolverJuegos(categorias)
        juegosRecomendados= tracker.get_slot("juegos")
        juegosPosibles= [item for item in juegosParecidos if item not in juegosRecomendados]
        juegoADecir=None
        if juegosPosibles:
            Categoriasimprimir = ", ".join([f'"{categoria}"' for categoria in categorias])
            juegoADecir= random.choice(juegosPosibles)
            imagen= devolverImagenes(juegoADecir)
            message = f"Entonces te puedo recomendar el siguiente juego: {juegoADecir}, debido a las categorias{Categoriasimprimir}"
            image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
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
                image_path = os.path.join("C:\\Users\\AGUSTIN\\Documents\\BotExploratoria\\Imagenes", imagen)
                message = f"no tengo mas con las categorias {CategoriasBorradas}, por lo que tome en cuenta las siguientes:{CategoriasUsadas} y te recomiendo en su lugar: {juegoADecir}"
            else:
                message = f"ya te recomende todos los juegos flaquito juga alguno"

        dispatcher.utter_message(text=message)
        dispatcher.utter_message(image=image_path)
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
        categorias= [item for item in categoriasEntidades if item not in categoriasActuales]
        if categorias:
            tamanioActuales=len(categoriasActuales)
            tamanioDif=len(categorias)
            if tamanioDif >3:
                tamanioDif=3
            if tamanioActuales != 3 :
                tamanioActuales = tamanioActuales + 1
            #primero saco las categorias distintas y despues las voy agregando desde atras para adelante(considerando mas importante las primeras)
            print(tamanioActuales)
            print(tamanioDif)
            print(categoriasActuales)
            print(categorias)
            for i in range(tamanioActuales-1, tamanioActuales - tamanioDif -1, -1):
                print(i)
                print(tamanioDif - (tamanioActuales - i))
                categoriasActuales[i] = categorias[tamanioDif - (tamanioActuales - i)]
        print(categoriasEntidades)
        print(categoriasActuales)
        message = f"voy a tener encuenta que te gustan esas categorias entonces"
            
        dispatcher.utter_message(text=message)
        return [SlotSet("categorias", categoriasActuales)]

    
