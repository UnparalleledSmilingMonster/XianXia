from db_handle import Database
import tkinter as tk

debug  = True

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.database = Database()
        self.set_window()
        self.define_widgets()
        
        
    def set_window(self):
        self.geometry("700x300")
        self.resizable(0,0)

    def define_widgets(self):
        self.button_load = tk.Button(self, text="Load Novel", command = self.load_novel)
        self.button_new = tk.Button(self, text="New Novel", command = self.new_novel)      
        self.button_load.pack(side=tk.TOP,pady=10)
        self.button_new.pack(side=tk.TOP,pady=30)
    
        if debug:
            self.button_reset = tk.Button(self, text="Reset DB", command=self.quit)
            self.button_reset.pack(side = tk.BOTTOM, anchor="e", padx=0, pady=8)
        
        self.button_quit = tk.Button(self, text="Leave", command=self.quit)
        self.button_quit.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)

    def load_novel(self):
        ld_window = load_window(self, self.database)
        ld_window.novel_list()


    def new_novel(self):
        nn_window = new_novel_window(self, self.database)
        nn_window.create_novel()
        




#########################################################################

class new_novel_window(tk.Toplevel):
    def __init__(self, parent, db):
        tk.Toplevel.__init__(self, parent)
        self.set_window()
        self.database = db

    def set_window(self):
        self.title("XianXia")
        self.geometry("700x300")
        self.resizable(0,0)

    def create_novel(self):
        text = tk.Label(self, text ="Name of the new novel : ")
        text.pack()
        ok = tk.Button(self, text = "New Entry")
        ok.pack
        self.database.create_novel("天影")




############################################################################


class load_window(tk.Toplevel):
    def __init__(self, parent, db):
        tk.Toplevel.__init__(self, parent)
        self.set_window()
        self.database = db

    def set_window(self):
        self.title("XianXia")
        self.geometry("700x300")
        self.resizable(0,0)

    def novel_list(self):
        L = self.database.novel_list()
        variable = tk.StringVar(self)
        variable.set("Novel List") 
        droplist_novels = tk.OptionMenu(self, variable, *L)
        droplist_novels.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)




########################################################################


class sub_window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, database)
        self.set_window()
        self.define_widgets()

    def set_window(self):
        self.geometry("700x300")
        self.resizable(0,0)



    def define_widgets(self):
        self.button_chap = tk.Button(self, text="New Chapter", command = self.new_chapter)
        self.label_word = tk.Label(self, text = "New word")



        self.button_quit = tk.Button(self, text="Leave", command=self.quit)

        self.button_chap.pack(side=tk.TOP,pady=10)
        self.label_word.pack(side=tk.TOP,pady=30)

        self.button_quit.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)


    def new_chapter(self):
        return 0

    def new_word(self):
        return 0





if __name__ == "__main__":
    app = Application()
    app.title("XianXia")
    app.mainloop()
