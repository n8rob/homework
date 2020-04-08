#!/usr/bin/env python
# coding: utf-8

# In[22]:


get_ipython().system('pip install --upgrade selenium')
get_ipython().system('pip install wordcloud')


# In[195]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import re
# import pickle as pkl
import time

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[196]:


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('window-size=200,200')


# In[ ]:


# browser = webdriver.Chrome()
# try:
#     browser.get("https://arxiv.org")
#     # Go to the search bar 
#     try:
#         search_bar = browser.find_element_by_tag_name('input')
#         search_bar.clear()
#         search_bar.send_keys(search_query)
#         # Now return using keys library
#         search_bar.send_keys(Keys.RETURN)
#     except NoSuchElementException:
#         print("Could not find the search bar!")
#         raise
#     # Now we gotta change the number of results to 200
#     option = browser.find_element_by_xpath("//option[@value='200']")
#     option.click()
#     go = browser.find_element_by_xpath("//button[@class='button is-small is-link']")
#     go.click()
#     # Now we want to add things to the list of urls 
#     list_urls = []
#     link_regex = re.compile(r'arXiv:\d+?')
#     try:
#         page_source = requests.get(browser.current_url).text
#         soup = BeautifulSoup(page_source, "html.parser")
#         for a in soup.find_all(string=link_regex,href=True):
#             list_urls.append(a["href"])
#             if len(list_urls) > 100:
#                 break
#             # Now find the 'Next' button and push it!!!
#     except:
#         raise

# finally:
#     browser.close()


# # This is where the functions begin

# In[ ]:





# In[164]:


# helper fcn
def sel_open(url,seconds=5):
    browser = webdriver.Chrome(executable_path="C:\\Users\\n8rro\\Downloads\\chromedriver_win32\\chromedriver")
    try:
        browser.get(url)
        time.sleep(seconds)
    finally:
        browser.close()


# In[ ]:





# In[179]:


def display_wordcloud(text):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(stopwords=[],background_color="white").generate(text)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    
def display_sent(sentence):  
    plt.title(sentence,fontsize="300")
    plt.show()


# In[ ]:


display_sent("Mi perro está aquí")


# In[ ]:





# In[ ]:





# In[163]:


def get_image(phrase, lang="en"):
    
    plus_phrase = phrase.replace(" ","+")
    if lang == "en" or lang.lower() == "english":
        search_url = "https://www.google.com/search?tbm=isch&sxsrf=ALeKk00i-4r1DEiog7GhbpukRkzk53ci-w%3A1585891813236&source=hp&biw=1366&bih=625&ei=5cmGXoW6DIbP0PEPuMW74AE&q={}&oq={}&gs_lcp=CgNpbWcQAzoHCCMQ6gIQJzoECCMQJzoFCAAQgwE6AggAOgYIABAFEB46BggAEAgQHjoECAAQGDoECAAQHlD-IliKRmCMSGgCcAB4AIABuAGIAfARkgEEMjEuNJgBAKABAaoBC2d3cy13aXotaW1nsAEK&sclient=img&ved=0ahUKEwjFwLaxw8voAhWGJzQIHbjiDhwQ4dUDCAY&uact=5".format(plus_phrase, plus_phrase)
    elif lang == "es" or lang.lower() == "spanish" or lang.lower() == "español":
        search_url = "https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk02XwkOdX6xClg0rqvz73Ntjpspk2w%3A1585968305626&source=hp&biw=1366&bih=625&ei=sfSHXpr8I8PG-gSV87CICg&q={}&oq={}&gs_lcp=CgNpbWcQARgAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADoECCMQJzoFCAAQgwFKJggXEiIwZzEyNGc3NGcxMDFnMTMxZzg3Zzc1ZzkwZzc0ZzczZzk5ShkIGBIVMGcxZzFnMWcxZzFnMWcxZzFnMWczUI8oWO5MYIxZaAFwAHgAgAF6iAGyB5IBBDExLjGYAQCgAQGqAQtnd3Mtd2l6LWltZw&sclient=img".format(plus_phrase, plus_phrase)
    elif lang == "fr" or lang.lower() == "french" or lang.lower() == "français":
        search_url = "https://www.google.com/search?hl=en&tbm=isch&sxsrf=ALeKk020EPD2iQJxyFM5ed8qwjJwLsur9Q%3A1585968678717&source=hp&biw=1366&bih=625&ei=JvaHXoadKeWz0PEP8qWmgAQ&q={}&oq={}&gs_lcp=CgNpbWcQARgAMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATMgQIABATOgcIIxDqAhAnOgQIIxAnOgIIADoFCAAQgwE6BggAEAgQHjoECAAQHjoGCAAQBRAeSisIFxInMGcyMjZnMTIwZzExOGcxMzJnODVnNzlnMTk0ZzEyMWcxMDZnMTQyShkIGBIVMGcxZzFnMWcyZzJnMWcxZzFnMWcxUOwOWPwoYP9JaARwAHgAgAHRAYgB3wqSAQU2LjUuMZgBAKABAaoBC2d3cy13aXotaW1nsAEK&sclient=img".format(plus_phrase, plus_phrase)
    
    try:
        test_for_url = search_url
    except:
        print("Language not supported")
        raise
    
    search_page_source = requests.get(search_url).text
    img_soup = BeautifulSoup(search_page_source, "html.parser")
    img_link = img_soup.find_all(name="img",src=True)[1]['src']
    sel_open(img_link)


# In[199]:


get_image("chien",lang='fr')


# In[106]:





# In[190]:


def translate(phrase, orig_lang="en", target_lang="fr"):
    # construct phrase to google search
    lang_dict = {"en":"english","fr":"french","es":"spanish"}
    if orig_lang == "en":
        url_phrase = "translate+"+phrase.replace(" ","+")+"+to+"+lang_dict[target_lang]
    else:
        url_phrase = "translate+"+phrase.replace(" ","+")+"+from+"+lang_dict[orig_lang]+"+to+"+lang_dict[target_lang]
    
    tr_url = "https://www.google.com/search?rlz=1C1SQJL_enUS777US777&sxsrf=ALeKk00sSJFO4FvyXRfr6jkFmHQi-FbZRg%3A1585969344675&ei=wPiHXs3zKJXi-gSFkKDwDQ&q={}&oq={}&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoGCAAQBxAeOgcIABAUEIcCOgIIADoECAAQHjoGCAAQBRAeOgYIABAIEB46BQgAEM0CSgkIFxIFMTItODZKCQgYEgUxMi0xMVCQdliAggFg6oYBaABwAngAgAFziAH8CpIBBDExLjSYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwjN06eb5M3oAhUVsZ4KHQUICN4Q4dUDCAw&uact=5".format(url_phrase,url_phrase)

    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\\Users\\n8rro\\Downloads\\chromedriver_win32\\chromedriver")
    try:
        browser.get(tr_url)
        time.sleep(1)
        tr_page_source = requests.get(browser.current_url).text
    finally:
        browser.close()
    
    tr_soup = BeautifulSoup(tr_page_source, "html.parser")
    index = tr_page_source.find("tu as mang")
    # tr_page_source[index-600:index+300]
    transln = tr_soup.find(class_="BNeawe iBp4i AP7Wnd").text
    
    return transln


# In[201]:


translated_phrase = translate("estoy aquí",orig_lang="es",target_lang="fr")
display_sent(translated_phrase)


# In[ ]:





# In[181]:


def display_wordnet(word):
    sel_open("http://conceptnet.io/c/en/{}".format(word))


# In[182]:


display_wordnet("fugitive")


# In[ ]:





# ## This is where the interface does its magic

# In[ ]:




