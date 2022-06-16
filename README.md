# The XianXia Project : Learn Chinese while reading novels !

To all avid readers of Chinese novels, have you ever dreamt to read in Chinese ? Well, if you are here, it means are ready to take the plunge. 
This modest app is designed to help you keep track of the new vocabulary you encounter. You can either assign words to the whole novel or to chapters to build small lists. 
Words are divided into 4 types : vocabulary, protagonist, place and artifact (the latter is especially for xianxia).

A web parser for pinyin is embedded to ease the indexing. Be patient as it may take a few seconds to process.

**Enjoy folks !**  **享受阅读!**

## The required packages :
This application is coded with Python 3.

- sqlite3 : `pip install pysqlite3`
- pyQt5 : `pip install pyqt5`
- requests : `pip install requests`
- beautifulsoup : `pip install beautifulsoup4`
- pyinstaller : `pip install pyinstaller` (To build the executable)

## Fonts :
The OpenSource fonts Sumi and CangLong are used. 

## Web-scraping :
The pinyin are scraped either from **omgchinese** or **yabla**. The meanings are from **omgchinese**.

## Build:
After installing the aforementioned packages. Execute the script *build.sh*.

If you want to clear the database, in the file `qt_window.py` make `debug = True` it will enable the "Reset DB" button.
You will have to re-build the executable though.

## Disclaimer:
This application is in no way meant to be used for storing sensitive data.
There is no encryption. It may be vulnerable to sql injection and so on...

