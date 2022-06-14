import sys  
from db_handle import Database
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
  
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
    
    def load(self):
        self.ld_window = LoadWindow(self, self.database)
        self.ld_window.show()
        self.ld_window.novel_list()     
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




########################################################################        
        
   
app = QApplication(sys.argv)
  
xianxia = MainWindow()
xianxia.show()
  
# Run application's main loop
sys.exit(app.exec_())
