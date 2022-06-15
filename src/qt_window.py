import sys  
from db_handle import Database
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
  
debug  = True


class MainWindow(QMainWindow):

    def __init__(self):
        QWidget.__init__(self)
        self.database = Database()
        self.set_window()
        self.define_widgets()
        self.buffer_string = ""
        self.cancel = False
        
        
    def set_window(self):
        self.setWindowTitle("XianXia") 
    

    def define_widgets(self):
    
        button_load = QPushButton("Load Novel", parent = self)
        button_load.clicked.connect(self.load)
        button_load.move(60,15)

        button_new_novel = QPushButton("New Novel Entry", parent = self)
        button_new_novel.clicked.connect(self.new_novel)
        button_load.move(60,45)

    
    def load(self):
        self.ld_window = LoadWindow(self, self.database)
        self.ld_window.show()
        self.ld_window.novel_list()     
        #if not self.cancel :
            #novel_win = novel_window(self, self.database, self.buffer_string)        
        self.cancel = False

    def new_novel(self):
        self.nn_window = NewNovelWindow(self, self.database)
        self.nn_window.show()
        self.nn_window.create_novel()
        #if not self.cancel :
            #novel_win = novel_window(self, self.database, self.buffer_string)
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
        self.set_window()
        self.layout = QVBoxLayout(self) 
        

    def set_window(self):
        self.setWindowTitle("XianXia")



    def novel_list(self):
        L = self.database.novel_list()
        
        ok = QPushButton("Select novel", parent = self)
        ok.clicked.connect(self.next)
        
        previous= QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        
        self.layout.addWidget(ok)
        self.layout.addWidget(previous)
        
        
     
        

    def next(self): 
        self.parent.buffer_string = ""
        self.database.commit()
        #self.destroy()
        
    def cancel(self):
        self.parent.cancel = True
        #self.destroy()




#########################################################################

class NewNovelWindow(QWidget):
    def __init__(self, parent, db):
        super().__init__()
        self.set_window()
        self.database = db
        self.parent = parent
        self.layout = QVBoxLayout(self)


    def set_window(self):
        self.setWindowTitle("XianXia")


    def create_novel(self):
        text = QLabel(text ="Name of the new novel : ", parent = self)
        self.layout.addWidget(text)

        self.text_input = QLineEdit(parent = self)
        self.layout.addWidget(self.text_input)


        ok = QPushButton("New Entry", parent = self)
        ok.clicked.connect(self.forward)
        self.layout.addWidget(ok)

        previous = QPushButton("Cancel", parent = self)
        previous.clicked.connect(self.cancel)
        self.layout.addWidget(previous)


    def cancel(self):
        self.parent.cancel = True
        self.database.commit()


    def forward(self):
        novel = self.text_input.text()
        self.database.create_novel(novel)
        QMessageBox.about(self, "Success !", "Novel entry " + novel + " created.")
        self.parent.buffer_string = novel
        self.database.commit()


#########################################################################

        
   
app = QApplication(sys.argv)
  
xianxia = MainWindow()
xianxia.show()
  
# Run application's main loop
sys.exit(app.exec_())
