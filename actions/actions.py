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
import requests
import json

def google_translate(word):
	from google_trans_new import google_translator
	translator = google_translator()
	return translator.translate(word, lang_src='de', lang_tgt='en')

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
			query_lang = str(google_translate(query_lang))
			if len(query_lang.split())>1:
				query_lang=query_lang.split()[-1]
			query_lang = query_lang.lower().capitalize().strip()
			#print(query_lang, 'translated')
			out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
			#print(out_row)
			if out_row:
				out_row = out_row[0]
				out_text = "Die Sprache %s gehört zur Familie %s \nmit der Gattung %s \nund hat ISO-Code %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
				dispatcher.utter_message(text = out_text)
			else:
				dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für die Sprache` %s" % query_lang)

				return []

class ActionLanguageByCountry(Action):

	def name(self) -> Text:
		return "action_lang_by_country"

	def run(self, dispatcher: CollectingDispatcher,
	    tracker: Tracker,
	    domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "country_lang.csv")
		wals_data_lang = pd.read_csv(data_path)
		entities = list(tracker.get_latest_entity_values("country"))
		#print("intent found")
		if len(entities) > 0:
			query_country = entities.pop()
			query_country = str(google_translate(query_country))
			if len(query_country.split()) > 1:
				query_country = query_country.split()[-1]
			query_country = query_country.lower().capitalize().strip()
			#print("entity found")
			# filtered = wals_data_lang[wals_data_lang["macroarea"] == query_country].to_dict("records")
			# print("entity found")
			# out_list = []
			# for record in filtered:
			# 	out_list.append(record["ascii_name"])
			#
			# if len(out_list) < 5 and len(out_list) > 0:
			# 	out_str = ", ".join(out_list[:5])
			out_str = wals_data_lang[wals_data_lang["Country"] == query_country]["Languages"]
			if len(out_str) > 0:
				out_str = out_str.values[0]

			if len(out_str) > 0:
			    dispatcher.utter_message(text = "Einige der in {} gesprochenen Sprachen sind: {}".format(query_country, out_str))
			else:#Wir entschuldigen uns. Amerika existiert nicht in unserer Datenbank.
			    dispatcher.utter_message(text = "Wir entschuldigen uns. %s existiert nicht in unserer Datenbank. " % query_country)

		return []


class ActionLocationSearch(Action):

	def name(self) -> Text:
		return "action_loc_search"

	def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
		wals_data = pd.read_csv(data_path)
		entities = list(tracker.get_latest_entity_values("language"))
		if len(entities) > 0:
			query_lang = entities.pop()
			query_lang=google_translate(query_lang)
			if len(query_lang.split()) > 1:
				query_lang = query_lang.split()[-1]
			query_lang = query_lang.lower().capitalize().strip()
			#print(query_lang)
			out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
			if len(out_row) > 0:
				out_row = out_row[0]
				out_text = "Die Sprache %s wird mit \n Längengrad:  %s\n Längengrad: %s\n gesprochen \n" % (out_row["Name"], out_row["Latitude"], out_row["Longitude"])
				dispatcher.utter_message(text = out_text)
			else:
				dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für die Sprache` %s " % query_lang)

		return []


class ActionAreaSearch(Action):

	def name(self) -> Text:
		return "action_area_search"

	def run(self, dispatcher: CollectingDispatcher,
		tracker: Tracker,
		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

		data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages-by-country.csv")
		wals_data = pd.read_csv(data_path)
		entities = list(tracker.get_latest_entity_values("language"))

		if len(entities) > 0:
			query_lang = entities.pop()
			query_lang=google_translate(query_lang)
			if len(query_lang.split()) > 1:
				query_lang = query_lang.split()[-1]
			query_lang = query_lang.lower().strip()

			out_row = wals_data[wals_data["ascii_name"] == query_lang].to_dict("records")
			if len(out_row) > 0:
				out_row = out_row[0]
				out_text = "Language %s is spoken at macroarea : %s\n" % (out_row["ascii_name"], out_row["macroarea"])
				dispatcher.utter_message(text = out_text)
			else:
				dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für Makrobereich von %s " % query_lang)

		return []


# class ActionLanguageSong(Action):
#
# 	def name(self) -> Text:
# 		return "action_lang_song"
#
# 	def run(self, dispatcher: CollectingDispatcher,
# 		tracker: Tracker,
# 		domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
# 		entities = list(tracker.get_latest_entity_values("language"))
# 		print('here')
# 		if len(entities) > 0:
# 			query_lang = entities.pop()
# 			query_lang = str(google_translate(query_lang))
# 			query_lang = query_lang.lower().strip().capitalize()
# 			print(query_lang)
# 			html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query_lang+"+song")
# 			video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
# 			out_url = "Genieße einige großartige %s Songs:  \n https://www.youtube.com/watch?v=%s \n  https://www.youtube.com/watch?v=%s \n   https://www.youtube.com/watch?v=%s " %( query_lang, video_ids[0], video_ids[1], video_ids[2])
#
# 			if len(out_url) > 0:
# 				dispatcher.utter_message(text = out_url)
# 			else:
# 				dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für die Sprache %s" % query_lang)
#
# 		return []


# class ActionLanguageReply(Action):
#
#     def name(self) -> Text:
#         return "action_lang_reply"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
#         wals_data = pd.read_csv(data_path)
#         entities = list(tracker.get_latest_entity_values("language"))
#
#         data_path2 = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "examples.csv")
#         wals_data2 = pd.read_csv(data_path2)
#
#         if len(entities) > 0:
#             query_lang = entities.pop()
#             query_lang = query_lang.lower().capitalize()
#             print(query_lang)
#
#             out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
#             if len(out_row) > 0:
#                 out_row = out_row[0]
#                 lang_code = out_row["ISO_codes"]
#                 out_row2 = wals_data2[wals_data2["Language_ID"] == lang_code].to_dict("records")
#                 if len(out_row2) >0:
#                     out_row2 = out_row2[0]
#                     out_text = out_row2["Primary_Text"]
#                     dispatcher.utter_message(text = out_text)
#             else:
#                 dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für die Sprache %s" % query_lang)
#
#         return []
