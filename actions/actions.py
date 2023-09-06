# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

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
        message = f"Hola, soy luis luis, para empezar te recomiendo el siguiente juego: {juego}, te gusta?"
        dispatcher.utter_message(text=message)
        return [SlotSet(key = "game", value = juego)]
    
class ActionDevolverJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        categoria1 = tracker.get_slot("categoria1")
        categoria2 = tracker.get_slot("categoria2")
        categoria3 = tracker.get_slot("categoria3")
        categorias = [categoria for categoria in [categoria1, categoria2, categoria3] if categoria]
        print(categorias)
        respuesta = devolverJuegos(categorias)
        if respuesta:
            juego= random.choice(respuesta)
            lastgame= tracker.get_slot("game")
            if lastgame == juego:
                mensaje = f"Perdon pero no tengo mas juegos con las categorias que me dijiste, voy a ignorar los de: {categoria3}"
                dispatcher.utter_message(text=mensaje)
                SlotSet(key="categoria3", value=None)
                categorias = [categoria for categoria in [categoria1, categoria2] if categoria]
                respuesta = devolverJuegos(categorias)
                juego= random.choice(respuesta)
                if lastgame == juego:
                    mensaje = f"Perdon pero voy a tener que a ignorar los de: {categoria2}"
                    dispatcher.utter_message(text=mensaje)
                    SlotSet(key="categoria2", value=None)
                    categorias = [categoria for categoria in [categoria1] if categoria]
                    respuesta = devolverJuegos(categorias)
                    juego= random.choice(respuesta)
                    if lastgame == juego:
                        mensaje = f"Perdon no tengo ningun juego parecido para recomendarte, te indico uno distinto pero bueno igualmente"
                        dispatcher.utter_message(text=mensaje)
                        SlotSet(key="categoria1", value=None)
                        respuesta = devolverJuegos([])
                        juego= random.choice(respuesta)
            message = f"Entonces te puedo recomendar el siguiente juego: {juego} que te parece?"
        else:
            message = "Lo siento, no se encontraron juegos para las categorías especificadas, podrias decirme otras categorias que te gusten o algun juego parecido?"
            SlotSet(key="categoria1", value=None)
            SlotSet(key="categoria2", value=None)
            SlotSet(key="categoria3", value=None)
            juego= tracker.get_slot("game")
        
        dispatcher.utter_message(text=message)

        return [SlotSet(key = "game", value = juego)]
   
class ActionSetearCategoriasLastGame(Action):
    def name(self) -> Text:
        return "action_set_categories_last_game"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juego = tracker.get_slot("game")
        print(juego)
        categorias= devolverCategorias(juego)
        print("Estoy aca")
        first_item = categorias[0]
        print(first_item)
        second_item = categorias[1]
        three_item = categorias[2]
        return [SlotSet(key="categoria1", value=first_item), SlotSet(key="categoria2", value=second_item), SlotSet(key="categoria3", value=three_item)]

class ActionSetearCategorias(Action):
    def name(self) -> Text:
        return "action_set_categories_entitie_game"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        juego = tracker.get_slot("usergame")
        categorias= devolverCategorias(juego)
        first_item = categorias[0]
        print(first_item)
        second_item = categorias[1]
        three_item = categorias[2]
        return [SlotSet(key="categoria1", value=first_item), SlotSet(key="categoria2", value=second_item), SlotSet(key="categoria3", value=three_item)]
    
