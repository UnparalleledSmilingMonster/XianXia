import sys  
from db_handle import Database
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTextEdit 
from PyQt5.QtCore import QEventLoop
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontDatabase


debug  = True


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.database = Database()
        self.layout = QGridLayout(self) 
        self.buffer_string = ""
        self.cancel = False
        self.fonts = QFontDatabase.addApplicationFont("../fonts/Sumi.otf")
        self.set_window()
        self.define_widgets()
        
        
        
    def set_window(self):
        self.setWindowTitle("The XianXia Project")
        self.setGeometry(200, 200, 500, 700)
        #self.setLayout(self.layout)


    

    def define_widgets(self):
    
        app_title = QLabel("THE XIANXIA PROJECT", parent=self)
        app_title.setFont(QFont('Sumi',50))
        self.layout.addWidget(app_title, 0, 1, 0, 2)
    
        button_load = QPushButton("Load Novel", parent = self)
        button_load.clicked.connect(self.load)
        self.layout.addWidget(button_load, 1,2)

        button_new_novel = QPushButton("New Novel Entry", parent = self)
        button_new_novel.clicked.connect(self.new_novel)
        self.layout.addWidget(button_new_novel, 2,2)
        
        
        button_quit = QPushButton("Quit", parent = self)
        button_quit.clicked.connect(quit)
        self.layout.addWidget(button_quit, 3,4)
        
        
        if debug:
            button_reset = QPushButton("Reset DB", parent = self)
            button_reset.clicked.connect(self.reset)
            self.layout.addWidget(button_reset, 3,0)
        

    
    def load(self):
        self.ld_window = LoadWindow(self, self.database)

        self.ld_window.show()
        self.ld_window.novel_list()
         
        if not self.cancel :
            self.ld_window.setAttribute(Qt.WA_DeleteOnClose)
            loop = QEventLoop()
            self.ld_window.destroyed.connect(loop.quit)
            loop.exec()
            self.novel_win = NovelWindow(self, self.database, self.buffer_string)    
            self.novel_win.show()
                        

        self.cancel = False

    def new_novel(self):
        self.nn_window = NewNovelWindow(self, self.database)
        self.nn_window.show()
        self.nn_window.create_novel()
        if not self.cancel :
            self.nn_window.setAttribute(Qt.WA_DeleteOnClose)
            loop = QEventLoop()
            self.nn_window.destroyed.connect(loop.quit)
            loop.exec()
            self.novel_win = NovelWindow(self, self.database, self.buffer_string)
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
        self.vlayout = QVBoxLayout(self) 
        self.set_window()
       
        

    def set_window(self):
        self.setWindowTitle("XianXia")
        self.setGeometry(200, 200, 500, 700)



    def novel_list(self):
        L = self.database.novel_list()
        
        ok = QPushButton("Select novel", parent = self)
        ok.clicked.connect(self.forward)
        
        previous= QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        
        self.novel_dropout = QComboBox(parent = self)
        self.novel_dropout.setGeometry(100 , 10 , 150 , 30)
        self.novel_dropout.addItems(L)
        self.vlayout.addWidget(self.novel_dropout)
        
        self.vlayout.addWidget(ok)
        self.vlayout.addWidget(previous)
        
    def forward(self): 
        self.parent.buffer_string = self.novel_dropout.currentText()
        self.close()
        
    def cancel(self):
        self.parent.cancel = True
        self.close()




#########################################################################

class NewNovelWindow(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.vlayout = QVBoxLayout(self)
        self.database = db
        self.parent = parent
        self.set_window()

    def set_window(self):
        self.setWindowTitle("XianXia")
        self.setGeometry(200, 200, 500, 700)


    def create_novel(self):
        text = QLabel(text ="Name of the new novel : ", parent = self)
        self.vlayout.addWidget(text)

        self.text_input = QLineEdit(parent = self)
        self.vlayout.addWidget(self.text_input)


        ok = QPushButton("New Entry", parent = self)
        ok.clicked.connect(self.forward)
        self.vlayout.addWidget(ok)

        previous = QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        self.vlayout.addWidget(previous)

    def cancel(self):
        self.parent.cancel = True
        self.close()

    def forward(self):
        novel = self.text_input.text()
        self.database.create_novel(novel)
        QMessageBox.about(self, "Success !", "Novel entry " + novel + " created.")
        self.parent.buffer_string = novel
        self.close()


#########################################################################

class NovelWindow(QWidget):
    def __init__(self, parent, db, name ):
        super().__init__()
        self.database = db
        self.novel = name
        self.vlayout = QVBoxLayout(self)
        self.set_window()
        self.define_widgets()
        
        
    def set_window(self):
        self.setWindowTitle(self.novel)
        self.setGeometry(200, 200, 500, 700)

    def define_widgets(self):
        
        label_novel = QLabel(self.novel, parent = self)
        self.vlayout.addWidget(label_novel)
        
       
        button_vocab = QPushButton(text = "Show all vocabulary", parent = self)
        button_vocab.clicked.connect(self.vocab)
        self.vlayout.addWidget(button_vocab)
         
    
        button_chap = QPushButton("New Chapter", parent = self)
        button_chap.clicked.connect(self.new_chapter)
        self.vlayout.addWidget(button_chap)
        
        button_new_word = QPushButton("New Word", parent = self)
        button_new_word.clicked.connect(self.new_word)
        self.vlayout.addWidget(button_new_word)
        
        button_search = QPushButton("Search word", parent = self)
        button_search.clicked.connect(self.search_word)
        self.vlayout.addWidget(button_search)
        
        self.word_ukw = QLineEdit(parent = self)
        self.vlayout.addWidget(self.word_ukw)


        button_quit = QPushButton("Leave", parent = self)
        button_quit.clicked.connect(self.close)
        self.vlayout.addWidget(button_quit)
        
        self.text_field = QTextEdit(self)
        self.vlayout.addWidget(self.text_field)
    
    def number_chapters(self):
        return self.database.number_chapters(self.novel)[0]
       
    def vocab(self):
        self.text_field.clear()
        rows = self.database.get_vocab(self.novel)    
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insertPlainText( hanzi + " : " + pinyin + " : " + meaning + " \n")

    
    def new_chapter(self):
        chapter = self.number_chapters() + 1
        self.chapter_win = ChapterWindow(self, self.database, self.novel, chapter)
        self.chapter_win.show()
        self.hide()
        self.chapter_win.setAttribute(Qt.WA_DeleteOnClose)
        loop = QEventLoop()
        self.chapter_win.destroyed.connect(loop.quit)
        loop.exec()
        self.show()
    
    def search_word(self):
        self.text_field.clear()
        res = self.database.search_word(self.novel, self.word_ukw.text())
        if res == None : self.text_field.insertPlainText( "No occurence of " + self.word_ukw.text() + " \n")
        else : self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        
        
    def new_word(self):
        self.database.new_word(self.novel, "hanzi", "pinyin" , "meaning")
        
        
########################################################################

class ChapterWindow(QWidget):
    def __init__(self, parent, db, novel, chapter ):
        super().__init__()
        self.database = db
        self.novel = novel
        self.chapter = chapter
        self.vlayout = QVBoxLayout(self)
        self.set_window()
        self.define_widgets()

    def set_window(self):
        self.setWindowTitle("Chapter " + str(self.chapter))
        self.setGeometry(200, 200, 500, 700)



    def define_widgets(self):
       
        button_vocab = QPushButton(text = "Show vocabulary", parent = self)
        button_vocab.clicked.connect(self.vocab)
        self.vlayout.addWidget(button_vocab)
         
    
        
        
        button_new_word = QPushButton("New Word", parent = self)
        button_new_word.clicked.connect(self.new_word)
        self.vlayout.addWidget(button_new_word)
        
        button_search = QPushButton("Search word", parent = self)
        button_search.clicked.connect(self.search_word)
        self.vlayout.addWidget(button_search)
       
        button_prev = QPushButton("Previous", parent = self.close)
        button_prev.clicked.connect(self.new_chapter)
        self.vlayout.addWidget(button_prev)
        
        self.text_field = QTextEdit(self)
        self.vlayout.addWidget(self.text_field)

    def vocab(self):
        self.clean_txt()
        rows = self.database.get_vocab(self.novel, self.chapter)
        
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insert(tk.END, hanzi + " : " + pinyin + " : " + meaning + " \n")
        
            
    def clean_txt(self):
        self.text_field.config(state= tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.config(state= tk.DISABLED)  
            
    
    def search_word(self):
        self.text_field.clear()
        res = self.database.search_word(self.novel, self.word_ukw.text())
        if res == None : self.text_field.insertPlainText( "No occurence of " + self.word_ukw.text() + " \n")
        else : self.text_field.insertPlainText( res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        
    def new_word(self):
        return 0


        
   
app = QApplication(sys.argv)
  
xianxia = MainWindow()
xianxia.show()
  
# Run application's main loop
sys.exit(app.exec_())
