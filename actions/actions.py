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


class ActionIniciar(Action):
    def name(self) -> Text:
        return "action_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        categorias = []
        respuesta = devolverJuegos(categorias)

        if respuesta:
            message = f"Hola, soy el bot de los juegitos. Te recomiendo para empezar los siguientes juegos: {', '.join(respuesta)}"
        else:
            message = "Lo siento, no se encontraron juegos para las categorías especificadas."
        
        dispatcher.utter_message(text=message)

        return []
    
class ActionDevolverJuego(Action):
    def name(self) -> Text:
        return "action_devolver_juego"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:


        
        categorias = ["categoria1", "categoria2", "categoria3"]
        result=devolverJuegos(categorias)
        if respuesta:
            game_list = "\n".join(respuesta)
            message = f"Hola, soy el bot de los juegitos. Te recomiendo para empezar los siguientes juegos:\n{game_list}"
        else:
            message = "Lo siento, no se encontraron juegos para las categorías especificadas."
        
        dispatcher.utter_message(text=message)

        return []

def devolverJuegos(categorias) -> List[Text]:
    # Convert Python list to Prolog list format, e.g., "[categoria1, categoria2, ...]"
    #prolog_list = "[" + ", ".join([f'"{categoria}"' for categoria in categorias]) + "]"
    #print(prolog_list)
    lista = "['Accion', 'Aventura']"
    with PrologMQI(port=8000) as mqi:
        with mqi.create_thread() as prolog_thread:
            prolog_thread.query("consult('C:/Users/AGUSTIN/Documents/BotExploratoria/actions/juegos.pl')")
            result = prolog_thread.query("recuperar_juegos_con_categorias(lista, Resultado)")
            print(result)
            lista = result[0]["Resultado"]
            # Convert the Prolog result to a Python list
            #result_list = [str(term) for term in result.("Resultado")]
    return lista
   
class ActionSetearCategorias(Action):
    def name(self) -> Text:
        return "action_set_categories"
    def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        

        return []