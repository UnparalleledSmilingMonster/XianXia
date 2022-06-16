import requests
from bs4 import BeautifulSoup



def yabla_scraper(hanzi):
    url="https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define="+hanzi
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    result = soup.find(id="search_results")
    pinyin = result.find("span", class_="pinyin").text

    return pinyin

def omgchinese_pinyin_scraper(hanzi):
    url = "https://www.omgchinese.com/dictionary/?q=" + hanzi + "&qt=0"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    result = soup.find("div", {"class": "pinyin"})
    pinyin = result.find("pinyin-color")["pinyin"] 
    
    return pinyin
    
    
    
def omgchinese_meaning_scraper(hanzi):
    url = "https://www.omgchinese.com/dictionary/?q=" + hanzi + "&qt=0"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    result = soup.find("span", {"class": "uu-mslash"})
    meaning = result.text
    
    return meaning
    
    

