# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os
import urllib.request
import re



class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Language %s belongs to the Family %s\n with Genus as %s\n and has ISO code %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Sorry! We don't have records for the language %s" % query_lang)

        return []



class ActionLanguageSong(Action):

    def name(self) -> Text:
        return "action_lang_song"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        entities = list(tracker.get_latest_entity_values("language"))

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_lang+"+song")
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            out_url = "Enjoy some great %s songs:  \n https://www.youtube.com/watch?v=%s \n  https://www.youtube.com/watch?v=%s \n   https://www.youtube.com/watch?v=%s " %( query_lang, video_ids[0], video_ids[1], video_ids[2])
            

            if len(out_url) > 0:
                dispatcher.utter_message(text = out_url)
            else:
                dispatcher.utter_message(text = "Sorry! We don't have records for the language %s" % query_lang)

        return []


class ActionLanguageReply(Action):

    def name(self) -> Text:
        return "action_lang_reply"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))

        data_path2 = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "examples.csv")
        wals_data2 = pd.read_csv(data_path2)

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = query_lang.lower().capitalize()
            print(query_lang)
            
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
            if len(out_row) > 0:
                out_row = out_row[0]
                lang_code = out_row["ISO_codes"]
                out_row2 = wals_data2[wals_data2["Language_ID"] == lang_code].to_dict("records")
                if len(out_row2) >0:
                    out_row2 = out_row2[0]
                    out_text = out_row2["Primary_Text"]
                    dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Sorry! We don't have records for the language %s" % query_lang)

        return []