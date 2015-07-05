# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 13:47:17 2015

@author: Cathy
"""

import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

## parse ALEC page containing links to all model policies
models_main = requests.get("http://www.alec.org/model-legislation/")

## create BeautifulSoup object from the ALEC html page
soupm = BeautifulSoup(models_main.text, "html.parser")

## function to filter in find_all()   
def model_legislation(href):
    """ search for keywords in href to filter 
    Args:
        href (str): href value returned by find_all()
    Returns:
        bool: T if href is a non-empty string containing the pattern
    """
    return href and re.compile("model-legislation/").search(href)

## get all model legislation links
soupm_filtered = soupm.find_all("a", href = model_legislation)

## extract URLs from 'a' tags
links_list = [link.get('href') for link in soupm_filtered]
links_set = set(links_list)

def remove_whitespace_chars(s):
    """ Substitute \n and \xa0 (non-breaking space) with ' '
    Args:
        s (str): unicode string returned by get_text()
    Returns:
        str: string without \n and \xa0
    """
    return s.replace(u'\xa0', '').replace(u'\n', ' ')    

def scrape_bill(href):
    """ Scrape the text from the bill
    Args:
        href (str): url to model bill
    Returns:
        text (str): the scraped text (without html tags)
    """
    try:
        r = requests.get(href)
        only_tags_with_id_main = SoupStrainer(id="main")
        mainsoup = BeautifulSoup(r.text, "html.parser", 
                             parse_only = only_tags_with_id_main)
        text = mainsoup.get_text(' ', strip=True)
        return(text)
    except:
        return []

split_regex = r'\W+'

def simpleTokenize(string):
    """ A simple implementation of input string tokenization
    Args:
        string (str): input string
    Returns:
        list: a list of tokens
    """
    if string == ' ':
      return []
    else:
      tokens = re.split(split_regex, string)
      tokens = filter(None, tokens)
      tokens = [t.lower() for t in tokens]
      return tokens

import nltk
nltk.download()
from nltk.corpus import stopwords # Import the stop word list
#print(stopwords.words("english"))


def tokenize(string):
    """ An implementation of input string tokenization that excludes stopwords
    Args:
        string (str): input string
    Returns:
        list: a list of tokens without stopwords
    """
    tokens = simpleTokenize(string)
    return [t for t in tokens if t not in stopwords.words("english")]

