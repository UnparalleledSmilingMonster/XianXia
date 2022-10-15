import sys  
import os
from db_handle import Database
from scraper import omgchinese_pinyin_scraper, omgchinese_meaning_scraper

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTextEdit 
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase



debug  = False

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    background_path = os.path.join(application_path, "./data/cover.jpeg" )
    font_sumi_path = os.path.join(application_path, "./fonts/Sumi.otf" )
    font_canglong_path = os.path.join(application_path, "./fonts/Long_Cang/LongCang-Regular.ttf" )
elif __file__:
    application_path = os.path.dirname(__file__)            
    background_path = os.path.join(application_path, "../data/cover.jpeg")
    font_sumi_path = os.path.join(application_path, "../fonts/Sumi.otf" )
    font_canglong_path = os.path.join(application_path, "../fonts/Long_Cang/LongCang-Regular.ttf" )



class MainWindow(QWidget):

    

    def __init__(self):
        super().__init__()
        self.database = Database()
        self.layout = QGridLayout(self) 
        self.buffer_int = -1
        self.cancel = False
        self.fonts = QFontDatabase.addApplicationFont(font_sumi_path)
        self.set_window()
        self.define_widgets()     
        
        
    def set_window(self):
        self.setWindowTitle("The XianXia Project")
        self.setGeometry(200, 200, 600, 700)     
        self.setFixedWidth(600)
        self.setFixedHeight(700)  


    def define_widgets(self):
    
        app_title = QLabel("THE XIANXIA PROJECT", parent=self)
        app_title.setFont(QFont('Sumi',50))
        self.layout.addWidget(app_title, 0, 0, 1, -2)
    
        button_load = QPushButton("Load Novel", parent = self)
        button_load.clicked.connect(self.load)
        self.layout.addWidget(button_load, 1,1)

        button_new_novel = QPushButton("New Novel Entry", parent = self)
        button_new_novel.clicked.connect(self.new_novel)
        self.layout.addWidget(button_new_novel, 2,1)
        
        
        button_quit = QPushButton("Quit", parent = self)
        button_quit.clicked.connect(self.close)
        self.layout.addWidget(button_quit, 4,2)
        
        
       
        button_reset = QPushButton("Reset DB", parent = self)
        button_reset.clicked.connect(self.reset)
        self.layout.addWidget(button_reset, 4,0)
        button_reset.setEnabled(debug)
        
        self.setLayout(self.layout)

    
    def load(self):
        self.ld_window = LoadWindow(self, self.database)
        self.ld_window.show()
        self.ld_window.novel_list()
        loop = QEventLoop()
        self.ld_window.setAttribute(Qt.WA_DeleteOnClose)
        self.ld_window.destroyed.connect(loop.quit)
        loop.exec()
         
        if not self.cancel :
            self.hide()
            self.novel_win = NovelWindow(self, self.database, self.buffer_int)    
            self.novel_win.show()
            
        self.cancel = False


    def new_novel(self):
        self.nn_window = NewNovelWindow(self, self.database)
        self.nn_window.show()
        self.nn_window.create_novel()
        loop = QEventLoop()
        self.nn_window.setAttribute(Qt.WA_DeleteOnClose)
        self.nn_window.destroyed.connect(loop.quit)
        loop.exec()

        if not self.cancel :    
            self.hide()        
            self.novel_win = NovelWindow(self, self.database, self.buffer_int)
            self.novel_win.show()
            
        self.cancel = False
    
     
    def reset(self):
        self.database.reset()
        self.database = Database()

       
        
############################################################################


class LoadWindow(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.database = db
        self.parent = parent
        self.layout = QGridLayout(self) 
        self.set_window()
       
        

    def set_window(self):
        self.setWindowTitle("XianXia")
        self.setGeometry(350, 550, 500, 300)
        self.setFixedWidth(500)
        self.setFixedHeight(300) 
        


    def novel_list(self):
        L = self.database.novel_list()
        
        ok = QPushButton("Select novel", parent = self)
        ok.clicked.connect(self.forward)
        
        previous= QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        
        self.novel_dropout = QComboBox(parent = self)
        self.novel_dropout.addItems([elt[1] for elt in L])
        self.layout.addWidget(self.novel_dropout, 0 ,0, 1 ,-2)
        
        self.layout.addWidget(ok , 2 , 2)
        self.layout.addWidget(previous, 2 , 0)
        
        self.setLayout(self.layout)
        
    def forward(self):
        if self.novel_dropout.currentIndex()  != -1:
            novel  = self.database.novel_list()[self.novel_dropout.currentIndex()][0]
            self.parent.buffer_int = novel
            self.close()
        
    def cancel(self):
        self.parent.cancel = True
        self.close()




#########################################################################

class NewNovelWindow(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.layout = QGridLayout(self)
        self.database = db
        self.parent = parent
        self.set_window()

    def set_window(self):
        self.setWindowTitle("XianXia")
        self.setGeometry(350, 550, 500, 300)
        self.setFixedWidth(500)
        self.setFixedHeight(300) 


    def create_novel(self):
        text = QLabel(text ="Name of the new novel : ", parent = self)
        self.layout.addWidget(text, 0 ,0)

        self.text_input = QLineEdit(parent = self)
        self.layout.addWidget(self.text_input, 0 ,1, 1,-1)


        ok = QPushButton("New Entry", parent = self)
        ok.clicked.connect(self.forward)
        self.layout.addWidget(ok, 1 ,2)

        previous = QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        self.layout.addWidget(previous, 1 ,0)

    def cancel(self):
        self.parent.cancel = True
        self.close()

    def forward(self):
        novel = self.text_input.text()
        if novel == "":
            QMessageBox.about(self, "Warning", "No name provided.")
        else :   
            self.parent.buffer_int = self.database.create_novel(novel)
            QMessageBox.about(self, "Success !", "Novel entry " + novel + " created.")
            self.close()


#########################################################################

class NovelWindow(QWidget):
    def __init__(self, parent, db, novel_id ):
        super().__init__()
        self.parent = parent
        self.database = db
        self.novel_id = novel_id
        self.novel = self.database.novel_name(self.novel_id)[0]
        self.layout = QGridLayout(self)
        self.fonts = QFontDatabase.addApplicationFont(font_canglong_path)
        self.text_font = QFont()
        self.text_font.setPointSize(14)
        self.word_types = ["vocabulary", "protagonist", "place", "artifact"]
        self.set_window()
        self.define_widgets()
      
        
        
    def set_window(self):
        self.setWindowTitle(self.novel)
        self.setGeometry(200, 200, 800, 900)
        self.setFixedWidth(800)
        self.setFixedHeight(900) 

    def define_widgets(self):        
        
        label_novel = QLabel(self.novel, parent = self)
        label_novel.setFont(QFont('LongCang', 40))
        self.layout.addWidget(label_novel,0 ,1,1,2, alignment=Qt.AlignCenter)
        
        
        button_chap = QPushButton("Go to", parent = self)
        button_chap.clicked.connect(self.go_to_chapter)
        self.layout.addWidget(button_chap, 1, 0)
        
        L = ["Chapter " + str(i) for i in range(1, self.number_chapters()+1)]
        self.chapters_dropout = QComboBox(parent = self)
        self.chapters_dropout.setGeometry(100 , 10 , 150 , 30)
        self.chapters_dropout.addItems(L)
        self.layout.addWidget(self.chapters_dropout, 1 ,1)
       
        button_chap = QPushButton("New Chapter", parent = self)
        button_chap.clicked.connect(self.new_chapter)
        self.layout.addWidget(button_chap, 1, 2)        
        
        
        button_vocab = QPushButton(text = "Show vocabulary", parent = self)
        button_vocab.clicked.connect(lambda : self.vocab(self.word_types[0]))
        self.layout.addWidget(button_vocab, 2 ,0)
        
        button_chararacters = QPushButton(text = "Show protagonists", parent = self)
        button_chararacters.clicked.connect(lambda : self.vocab(self.word_types[1]))
        self.layout.addWidget(button_chararacters, 2 ,1)
        
        button_places = QPushButton(text = "Show places", parent = self)
        button_places.clicked.connect(lambda : self.vocab(self.word_types[2]))
        self.layout.addWidget(button_places, 2 ,2)
        
        button_artifacts = QPushButton(text = "Show artifacts", parent = self)
        button_artifacts.clicked.connect(lambda : self.vocab(self.word_types[3]))
        self.layout.addWidget(button_artifacts, 2 ,3)
       
        label_hanzi = QLabel(self.tr("汉字"))
        self.form_hanzi = QLineEdit(self)
        label_hanzi.setBuddy(self.form_hanzi)
        self.layout.addWidget(self.form_hanzi, 5, 0)
        self.layout.addWidget(label_hanzi, 4, 0)
        
        label_pinyin = QLabel(self.tr("Pinyin"))
        self.form_pinyin = QLineEdit(self)
        label_pinyin.setBuddy(self.form_pinyin)
        self.layout.addWidget(self.form_pinyin, 5, 1)
        self.layout.addWidget(label_pinyin, 4, 1)
        
        label_meaning = QLabel(self.tr("Meaning"))
        self.form_meaning = QLineEdit(self)
        label_meaning.setBuddy(self.form_meaning)
        self.layout.addWidget(self.form_meaning, 5, 2)
        self.layout.addWidget(label_meaning, 4, 2)
        
        label_type = QLabel(self.tr("Type"))
        self.dropout_type = QComboBox(self)
        self.dropout_type.addItems(self.word_types)
        label_type.setBuddy(self.dropout_type)
        self.layout.addWidget(self.dropout_type, 5, 3)
        self.layout.addWidget(label_type, 4, 3)        
  
        
        self.box_autofill = QPushButton("Pinyin autofill", parent = self)
        self.box_autofill.clicked.connect(self.pinyin_autofill)        
        self.layout.addWidget(self.box_autofill, 6 ,1 )
        
        self.button_suggest = QPushButton("Suggest meaning", parent = self)
        self.button_suggest.clicked.connect(self.suggest_meaning)
        self.layout.addWidget(self.button_suggest, 6 ,2)     
          
        button_new_word = QPushButton("New Word", parent = self)
        button_new_word.clicked.connect(self.new_word)
        self.layout.addWidget(button_new_word, 6, 3)       

        self.word_ukw = QLineEdit(parent = self)
        self.layout.addWidget(self.word_ukw, 7, 0)
        
        button_search = QPushButton("Search word", parent = self)
        button_search.clicked.connect(self.search_word)        
        self.layout.addWidget(button_search, 7, 1)
        
        button_alike= QPushButton("Try match", parent = self)
        button_alike.clicked.connect(self.words_like)        
        self.layout.addWidget(button_alike, 7, 2)


        button_quit = QPushButton("Leave", parent = self)
        button_quit.clicked.connect(self.menu)
        self.layout.addWidget(button_quit, 8,3)
        
        self.text_field = QTextEdit(self)
        self.text_field.setFont(self.text_font)
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field, 9, 0, 1, -3)
        
        columns = self.layout.columnCount() 
        for i in range(columns):
            self.layout.setColumnMinimumWidth(i, self.width() // columns )
        self.setLayout(self.layout)
    
    def menu(self):
        self.parent.show()
        self.close()
        
        
    def number_chapters(self):
        return self.database.number_chapters(self.novel_id)[0]
    
    def go_to_chapter(self):
        chapter = self.chapters_dropout.currentText().split(" ")
        if len(chapter) ==2:
            self.chapter_win = ChapterWindow(self, self.database, self.novel_id, chapter[1])
            self.chapter_win.show()
            self.hide()
            self.chapter_win.setAttribute(Qt.WA_DeleteOnClose)
            loop = QEventLoop()
            self.chapter_win.destroyed.connect(loop.quit)
            loop.exec()
            self.reload_chapters()
            self.show()
    
     
    def vocab(self, word_type):
        self.text_field.clear()
        rows = self.database.get_vocab(self.novel_id, word_type)    
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insertPlainText( hanzi + " : " + pinyin + " : " + meaning + " \n")

    
    def new_chapter(self):
        chapter = self.number_chapters() + 1
        self.chapter_win = ChapterWindow(self, self.database, self.novel_id, chapter)
        self.chapter_win.show()
        self.hide()


    
    def search_word(self):
        self.text_field.clear()
        res = self.database.search_word(self.novel_id, self.word_ukw.text())
        if res == None : 
            self.text_field.insertPlainText( "No occurence of " + self.word_ukw.text() + " \n")
            self.words_like()
                      
            
        else : self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        self.word_ukw.clear()
    
   
    def words_like(self):
        self.text_field.clear()
        self.text_field.insertPlainText( "Words alike : \n")
        alike = []
        for elt in self.word_ukw.text():
            alike += self.database.similarities(self.novel_id, elt)
        alike = set(alike)
        for word in alike:
            self.text_field.insertPlainText( word[0] + " : "  + word[1] + " : " + word[2] + "\n") 
        self.word_ukw.clear()    
    
    
    
    
    def reload_chapters(self):
        self.chapters_dropout.clear()
        self.chapters_dropout.addItems(["Chapter " + str(i) for i in range(1, self.number_chapters()+1)])
    
        
    def new_word(self):
        hanzi = self.form_hanzi.text()
        pinyin = self.form_pinyin.text()
        meaning = self.form_meaning.text()
        word_type = self.dropout_type.currentText()
        self.form_hanzi.clear()
        self.form_pinyin.clear()
        self.form_meaning.clear()
        
        if hanzi != "":
            if not(self.database.exists(self.novel_id, hanzi)):            
                self.database.new_word(self.novel_id, hanzi, pinyin , meaning, word_type)            
            else : 
                self.text_field.clear()
                res = self.database.search_word(self.novel_id, hanzi)     
                self.text_field.insertPlainText("Word already exists ! \n")      
                self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
            
        else : QMessageBox.about(self, "Error", "Empty word.")
        
    def pinyin_autofill(self):
        hanzi = self.form_hanzi.text()
        self.form_pinyin.setText(omgchinese_pinyin_scraper(hanzi))
        
    def suggest_meaning(self):
        self.text_field.clear()
        hanzi = self.form_hanzi.text()
        self.text_field.insertPlainText(omgchinese_meaning_scraper(hanzi))
        
    
########################################################################

class ChapterWindow(QWidget):
    def __init__(self, parent, db, novel_id, chapter ):
        super().__init__()
        self.parent = parent
        self.database = db
        self.novel_id = novel_id
        self.novel = self.database.novel_name(self.novel_id)
        self.chapter = chapter
        self.text_font = QFont()
        self.text_font.setPointSize(14)
        self.layout = QGridLayout(self)
        self.word_types = ["vocabulary", "protagonist", "place", "artifact"]
        self.set_window()
        self.define_widgets()
        

    def set_window(self):
        self.setWindowTitle("Chapter " + str(self.chapter))
        self.setGeometry(200, 200, 800, 900)
        self.setFixedWidth(800)
        self.setFixedHeight(900) 


    def define_widgets(self):
       
        button_vocab = QPushButton(text = "Show vocabulary", parent = self)
        button_vocab.clicked.connect(lambda : self.vocab(self.word_types[0]))
        self.layout.addWidget(button_vocab, 1 ,0)
        
        button_chararacters = QPushButton(text = "Show protagonists", parent = self)
        button_chararacters.clicked.connect(lambda : self.vocab(self.word_types[1]))
        self.layout.addWidget(button_chararacters, 1 ,1)
        
        button_places = QPushButton(text = "Show places", parent = self)
        button_places.clicked.connect(lambda : self.vocab(self.word_types[2]))
        self.layout.addWidget(button_places, 1,2)
        
        button_artifacts = QPushButton(text = "Show artifacts", parent = self)
        button_artifacts.clicked.connect(lambda : self.vocab(self.word_types[3]))
        self.layout.addWidget(button_artifacts, 1 ,3)
                    
        label_hanzi = QLabel(self.tr("汉字"))
        self.form_hanzi = QLineEdit(self)
        label_hanzi.setBuddy(self.form_hanzi)
        self.layout.addWidget(self.form_hanzi, 4, 0)
        self.layout.addWidget(label_hanzi, 3, 0)
        
        label_pinyin = QLabel(self.tr("Pinyin"))
        self.form_pinyin = QLineEdit(self)
        label_pinyin.setBuddy(self.form_pinyin)
        self.layout.addWidget(self.form_pinyin, 4, 1)
        self.layout.addWidget(label_pinyin, 3, 1)
        
        label_meaning = QLabel(self.tr("Meaning"))
        self.form_meaning = QLineEdit(self)
        label_meaning.setBuddy(self.form_meaning)
        self.layout.addWidget(self.form_meaning, 4, 2)
        self.layout.addWidget(label_meaning, 3, 2)
        
        label_type = QLabel(self.tr("Type"))
        self.dropout_type = QComboBox(self)
        self.dropout_type.addItems(self.word_types)
        label_type.setBuddy(self.dropout_type)
        self.layout.addWidget(self.dropout_type, 4, 3)
        self.layout.addWidget(label_type, 3, 3)
        
        
        self.box_autofill = QPushButton("Pinyin autofill", parent = self)
        self.box_autofill.clicked.connect(self.pinyin_autofill)        
        self.layout.addWidget(self.box_autofill, 5 ,1 )        
        
        self.button_suggest = QPushButton("Suggest meaning", parent = self)
        self.button_suggest.clicked.connect(self.suggest_meaning)
        self.layout.addWidget(self.button_suggest, 5 ,2)        
        
        button_new_word = QPushButton("New Word", parent = self)
        button_new_word.clicked.connect(self.new_word)
        self.layout.addWidget(button_new_word, 5, 3)   
        
        self.word_ukw = QLineEdit(parent = self)
        self.layout.addWidget(self.word_ukw, 6, 0)
        
        button_search = QPushButton("Search word", parent = self)
        button_search.clicked.connect(self.search_word)
        self.layout.addWidget(button_search, 6, 1)
        
        button_alike= QPushButton("Try match", parent = self)
        button_alike.clicked.connect(self.words_like)        
        self.layout.addWidget(button_alike, 6, 2)

       
        button_prev = QPushButton("Previous", parent = self)
        button_prev.clicked.connect(self.menu)
        self.layout.addWidget(button_prev,  7, 0)
        
        
        
        self.text_field = QTextEdit(self)
        self.text_field.setFont(self.text_font)
        self.text_field.setReadOnly(True)
        self.layout.addWidget(self.text_field, 8 , 0, 1 , -2)
    
    def menu(self):
        self.parent.show()
        self.parent.reload_chapters()
        self.close()
        
        
    def pinyin_autofill(self) :
        hanzi = self.form_hanzi.text()
        self.form_pinyin.setText(omgchinese_pinyin_scraper(hanzi))
            
    def suggest_meaning(self):
        self.text_field.clear()
        hanzi = self.form_hanzi.text()
        self.text_field.insertPlainText(omgchinese_meaning_scraper(hanzi))
      
    def vocab(self, word_type):
        self.text_field.clear()
        rows = self.database.get_vocab(self.novel_id, word_type, self.chapter)    
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insertPlainText( hanzi + " : " + pinyin + " : " + meaning + " \n")
            
            
    def search_word(self):
        self.text_field.clear()
        res = self.database.search_word(self.novel_id, self.word_ukw.text())
        if res == None : 
            self.text_field.insertPlainText( "No occurence of " + self.word_ukw.text() + " \n")
            self.words_like()
                      
            
        else : self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        self.word_ukw.clear()
    
   
    def words_like(self):
        self.text_field.clear()
        self.text_field.insertPlainText( "Words alike : \n")
        alike = []
        for elt in self.word_ukw.text():
            alike += self.database.similarities(self.novel_id, elt)
        alike = set(alike)
        for word in alike:
            self.text_field.insertPlainText( word[0] + " : "  + word[1] + " : " + word[2] + "\n") 
        self.word_ukw.clear()    
        
        
    def new_word(self):
        hanzi = self.form_hanzi.text()
        pinyin = self.form_pinyin.text()
        meaning = self.form_meaning.text()
        word_type = self.dropout_type.currentText()
        self.form_hanzi.clear()
        self.form_pinyin.clear()
        self.form_meaning.clear()
        if (hanzi != ""):
            if not(self.database.exists(self.novel_id, hanzi)):            
                self.database.new_word(self.novel_id, hanzi, pinyin , meaning, word_type, chapter = self.chapter)            
            else : 
                self.text_field.clear()
                res = self.database.search_word(self.novel_id, hanzi)     
                self.text_field.insertPlainText("Word already exists ! \n")      
                self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        
        else : QMessageBox.about(self, "Error", "Empty word.")
        
        

app = QApplication(sys.argv)

xianxia = MainWindow()
xianxia.setAttribute(Qt.WA_StyledBackground)      
xianxia.setStyleSheet("""MainWindow{border-image : url(""" +  background_path + """) 0 0 0 0;}""")
xianxia.show()
  
# Run application's main loop
sys.exit(app.exec_())
