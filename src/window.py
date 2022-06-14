from db_handle import Database
import tkinter as tk
from tkinter import messagebox



debug  = True


class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.database = Database()
        self.set_window()
        self.define_widgets()
        self.buffer_string = ""
        self.cancel = False
        
        
    def set_window(self):
        self.geometry("700x300")
        self.resizable(0,0)

    def define_widgets(self):
        self.button_load = tk.Button(self, text="Load Novel", command = self.load_novel)
        self.button_new = tk.Button(self, text="New Novel", command = self.new_novel)      
        self.button_load.pack(side=tk.TOP,pady=10)
        self.button_new.pack(side=tk.TOP,pady=30)
    
        if debug:
            self.button_reset = tk.Button(self, text="Reset DB", command=self.reset)
            self.button_reset.pack(side = tk.BOTTOM, anchor="w")
        
        self.button_quit = tk.Button(self, text="Leave", command=self.quit)
        self.button_quit.pack(side=tk.BOTTOM, anchor="e")

    def load_novel(self):
        ld_window = load_window(self, self.database)
        ld_window.novel_list()     
        self.wait_window(ld_window)
        if not self.cancel :
            novel_win = novel_window(self, self.database, self.buffer_string)        
        self.cancel = False

    def new_novel(self):
        nn_window = new_novel_window(self, self.database)
        nn_window.create_novel()
        self.wait_window(nn_window)
        if not self.cancel :
            novel_win = novel_window(self, self.database, self.buffer_string)
        self.cancel = False    
        

        
        
    def reset(self):
        self.database.reset()
        self.database = Database()
        




#########################################################################

class new_novel_window(tk.Toplevel):
    def __init__(self, parent, db):
        tk.Toplevel.__init__(self, parent)
        self.set_window()
        self.database = db
        self.parent = parent

    def set_window(self):
        self.title("XianXia")
        self.geometry("700x300")
        self.resizable(0,0)

    def create_novel(self):
        text = tk.Label(self, text ="Name of the new novel : ")
        text.pack(side=tk.TOP, anchor = "c")
        
        self.name = tk.StringVar(self)
        text_input = tk.Entry(self, textvariable = self.name)
        text_input.pack(side = tk.TOP, anchor = "c")

        ok = tk.Button(self, text = "New Entry", command = self.next)
        ok.pack(side=tk.RIGHT, anchor="c")
               
        previous = tk.Button(self, text = "Cancel", command = self.cancel)
        previous.pack(side=tk.LEFT, anchor="c")
        
    def cancel(self):
        self.parent.cancel = True
        self.database.commit()
        self.destroy()
        
        
    def next(self):
        novel = self.name.get()
        self.database.create_novel(novel)
        messagebox.showinfo("Success !", "Novel entry " + novel + " created.")
        self.parent.buffer_string = novel
        self.database.commit()
        self.destroy()




############################################################################


class load_window(tk.Toplevel):
    def __init__(self, parent, db):
        tk.Toplevel.__init__(self, parent)
        self.database = db
        self.parent = parent
        self.set_window()
        

    def set_window(self):
        self.title("XianXia")
        self.geometry("700x300")
        self.resizable(0,0)

    def novel_list(self):
        L = self.database.novel_list()
        self.variable = tk.StringVar()
        self.variable.set("Novel List") 
        droplist_novels = tk.OptionMenu(self, self.variable, *L)
        droplist_novels.pack(side=tk.TOP,anchor="c")
        
        ok = tk.Button(self, text = "Select novel", command = self.next)
        ok.pack(side=tk.RIGHT, anchor="c")
               
        previous = tk.Button(self, text = "Cancel", command = self.cancel)
        previous.pack(side=tk.LEFT, anchor="c")
        

    def next(self): 
        self.parent.buffer_string = self.variable.get()
        self.database.commit()
        self.destroy()
        
    def cancel(self):
        self.parent.cancel = True
        self.destroy()




########################################################################


class novel_window(tk.Toplevel):
    def __init__(self, parent, db, name ):
        tk.Toplevel.__init__(self, parent)
        self.database = db
        self.novel = name
        self.set_window()
        self.define_widgets()

    def set_window(self):
        self.geometry("700x300")
        self.resizable(0,0)
        self.title(self.novel)



    def define_widgets(self):
        
        label_novel = tk.Label(self, text = self.novel)
        label_novel.pack(side = tk.TOP, anchor="c")
        
       
        button_vocab = tk.Button(self, text = "Show all vocabulary", command = self.vocab)
        button_vocab.pack(side = tk.TOP, anchor="c")
         
    
        button_chap = tk.Button(self, text="New Chapter", command = self.new_chapter)
        button_chap.pack(side=tk.TOP,pady=10)
        label_word = tk.Label(self, text = "New word")
        label_word.pack(side=tk.TOP,pady=30)
        
        button_search = tk.Button(self, text = "Search word", command = self.search_word)
        button_search.pack(side=tk.TOP,pady=30)
        
        self.word_ukw = tk.StringVar(self)
        word_search = tk.Entry(self, textvariable = self.word_ukw)
        word_search.pack(side = tk.TOP, anchor = "e")


        button_quit = tk.Button(self, text="Leave", command=self.destroy)
        button_quit.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)
        
        self.text_field = tk.Text(self, state='disabled', height = len(rows))
        self.text_field.pack(side = tk.BOTTOM, anchor = "c")
        
       
    def vocab(self):
        self.clean_txt()
        rows = self.database.get_vocab(self.novel)    
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insert(END, hanzi + " : " + pinyin + " : " + meaning + " \n")

    
    def new_chapter(self):
        
        chapter = 1
        chapter_win = chapter_window(self, self.database, self.novel, chapter)
        self.withdraw()
        self.wait_window(chapter_win)
        self.deiconify()
    
    def search_word(self):
        self.clean_txt()
        res = self.database.search_word(self.novel, self.word_ukw.get())
        if res == None : print("not found")
        else : print("found")
        
        
    def clean_txt(self):
        self.text_field.config(state=NORMAL)
        self.text_field.delete('1.0', END)
        self.text_field.config(state=DISABLED)  
        
    def new_word(self):
        return 0
        
        
########################################################################


class chapter_window(tk.Toplevel):
    def __init__(self, parent, db, novel, chapter ):
        tk.Toplevel.__init__(self, parent)
        self.database = db
        self.novel = novel
        self.chapter = chapter
        self.set_window()
        self.define_widgets()

    def set_window(self):
        self.geometry("700x300")
        self.resizable(0,0)
        self.title("Chapter " + str(self.chapter))



    def define_widgets(self):
       
       
        button_vocab = tk.Button(self, text = "Show vocabulary", command = self.vocab)
        button_vocab.pack(side = tk.TOP, anchor="c")
            

        label_word = tk.Label(self, text = "New word")
        button_prev = tk.Button(self, text="Previous", command=self.destroy)

        label_word.pack(side=tk.TOP,pady=30)

        button_prev.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)
        
        self.text_field = tk.Text(self, height = len(rows))
        self.text_field.pack(side = tk.BOTTOM, anchor = "c")

    def vocab(self):
    self.clean_txt()
        rows = self.database.get_vocab(self.novel, self.chapter)
        
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insert(END, hanzi + " : " + pinyin + " : " + meaning + " \n")
        
            
    def clean_txt(self):
        self.text_field.config(state=NORMAL)
        self.text_field.delete('1.0', END)
        self.text_field.config(state=DISABLED)  
            
    

    def new_word(self):
        return 0





if __name__ == "__main__":
    app = Application()
    app.title("XianXia")
    app.mainloop()
