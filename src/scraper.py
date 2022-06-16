import requests
from bs4 import BeautifulSoup



def yabla_scraper(hanzi):
    url="https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define="+hanzi
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(id="search_results")
    pinyin = results.find("span", class_="pinyin").text
    print(pinyin)
    return pinyin


#yabla_scraper("生活")

def omgchinese_scraper(hanzi):
    url = "https://www.omgchinese.com/dictionary/?q=" + hanzi + "&qt=0"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    results = soup.find(id="search_results")
    
    
    
omgchinese_scraper("生活")
