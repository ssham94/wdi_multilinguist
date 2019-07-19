import requests
import json
from random import randint

class Multilinguist:
  """This class represents a world traveller who knows 
  what languages are spoken in each country around the world
  and can cobble together a sentence in most of them
  (but not very well)
  """

  translatr_base_url = "http://bitmakertranslate.herokuapp.com"
  countries_base_url = "https://restcountries.eu/rest/v2/name"
  #{name}?fullText=true
  #?text=The%20total%20is%2020485&to=ja&from=en

  def __init__(self):
    """Initializes the multilinguist's current_lang to 'en'
    
    Returns
    -------
    Multilinguist
        A new instance of Multilinguist
    """
    self.current_lang = 'en'

  def language_in(self, country_name):
    """Uses the RestCountries API to look up one of the languages
    spoken in a given country

    Parameters
    ----------
    country_name : str
         The full name of a country.

    Returns
    -------
    bool 
        2 letter iso639_1 language code.
    """
    params = {'fullText': 'true'}
    response = requests.get(f"{self.countries_base_url}/{country_name}", params=params)
    json_response = json.loads(response.text)
    return json_response[0]['languages'][0]['iso639_1']

  def travel_to(self, country_name):
    """Sets current_lang to one of the languages spoken
    in a given country

    Parameters
    ----------
    country_name : str
        The full name of a country.

    Returns
    -------
    str
        The new value of current_lang as a 2 letter iso639_1 code.
    """
    local_lang = self.language_in(country_name)
    self.current_lang = local_lang
    return self.current_lang

  def say_in_local_language(self, msg):
    """(Roughly) translates msg into current_lang using the Transltr API

    Parameters
    ----------
    msg : str
        A message to be translated.

    Returns
    -------
    str
        A rough translation of msg.
    """
    params = {'text': msg, 'to': self.current_lang, 'from': 'en'}
    response = requests.get(self.translatr_base_url, params=params)
    json_response = json.loads(response.text)
    return json_response['translationText']

class MathGenius(Multilinguist):
  def report_total(self, num_list):
    total = sum(i for i in num_list)
    translated = self.say_in_local_language("The total is:")
    return f"{translated} {total}"

class QuoteCollector(Multilinguist):
  def __init__(self):
    self.quote_list = []
  
  def add_quote(self, new_quote):
    self.quote_list.append(new_quote)
  
  def say_random_quote(self):
    random_num = randint(0,len(self.quote_list)-1)
    return self.say_in_local_language(self.quote_list[random_num])

# Testing out the multilinguist class
test = Multilinguist()
test.travel_to('Italy')
print(test.say_in_local_language('Hello'))
print("")

# Trying out examples given
me = MathGenius()
print(me.report_total([23,45,676,34,5778,4,23,5465])) # The total is 12048
me.travel_to("India")
print(me.report_total([6,3,6,68,455,4,467,57,4,534])) # है को कुल 1604
me.travel_to("Italy")
print(me.report_total([324,245,6,343647,686545])) # È Il totale 1030767
print("")

# Creating new quote collector and adding 3 quotes
you = QuoteCollector()
you.add_quote("I'm going to make him an offer he can't refuse.")
you.add_quote("May the Force be with you.")
you.add_quote("Bond. James Bond.")

# Testing to see that they have been added correctly
print(you.quote_list)
print("")

# Testing the say random quote function
you.travel_to("Mexico")
print(you.say_random_quote())
you.travel_to("France")
print(you.say_random_quote())
you.travel_to("Japan")
print(you.say_random_quote())
