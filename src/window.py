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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)



    def define_widgets(self):
        
        label_novel = tk.Label(self, text = self.novel)
        label_novel.grid(row=0,column=1)
        
       
        button_vocab = tk.Button(self, text = "Show all vocabulary", command = self.vocab)
        button_vocab.grid(row=1,column=1)
         
    
        button_chap = tk.Button(self, text="New Chapter", command = self.new_chapter)
        button_chap.grid(row=2,column=1)
        button_new_word = tk.Button(self, text = "New word", command = self.new_word)
        button_new_word.grid(row=3,column=1)
        
        button_search = tk.Button(self, text = "Search word", command = self.search_word)
        button_search.grid(row=4,column=1)
        
        self.word_ukw = tk.StringVar(self)
        word_search = tk.Entry(self, textvariable = self.word_ukw)
        word_search.grid(row=4, column = 2)


        button_quit = tk.Button(self, text="Leave", command=self.destroy)
        button_quit.grid(row=5, column = 2)
        
        self.text_field = tk.Text(self, state='disabled', height = 3)
        self.text_field.grid(row=5, column = 1)
    
    
    def number_chapters(self):
        return self.database.number_chapters(self.novel)[0]



       
    def vocab(self):
        self.clean_txt()
        rows = self.database.get_vocab(self.novel)    
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insert(tk.END, hanzi + " : " + pinyin + " : " + meaning + " \n")

    
    def new_chapter(self):
        chapter = self.number_chapters() + 1
        chapter_win = chapter_window(self, self.database, self.novel, chapter)
        self.withdraw()
        self.wait_window(chapter_win)
        self.deiconify()
    
    def search_word(self):
        self.clean_txt()
        res = self.database.search_word(self.novel, self.word_ukw.get())
        if res == None : self.text_field.insert(tk.END, "No occurence of " + self.word_ukw.get() + " \n")
        else : self.text_field.insert(tk.END, res[0] + " : "  + res[1] + " : " + res[2] + "\n")
        
        
    def clean_txt(self):
        self.text_field.config(state= tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.config(state= tk.DISABLED)  
        
    def new_word(self):
        self.database.new_word(self.novel, "hanzi", "pinyin" , "meaning")
        
        
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
            

        button_new_word = tk.Button(self, text = "New word", command = self.new_word)
        button_new_word.pack(side=tk.TOP,pady=30)
        
        button_prev = tk.Button(self, text="Previous", command=self.destroy)
        button_prev.pack(side=tk.BOTTOM,anchor="e", padx=8, pady=8)
        
        self.text_field = tk.Text(self, height = 1)
        self.text_field.pack(side = tk.BOTTOM, anchor = "c")

    def vocab(self):
        self.clean_txt()
        rows = self.database.get_vocab(self.novel, self.chapter)
        
        for (hanzi, pinyin, meaning) in rows :
            self.text_field.insert(tk.END, hanzi + " : " + pinyin + " : " + meaning + " \n")
        
            
    def clean_txt(self):
        self.text_field.config(state= tk.NORMAL)
        self.text_field.delete('1.0', tk.END)
        self.text_field.config(state= tk.DISABLED)  
            
    

    def new_word(self):
        return 0





if __name__ == "__main__":
    app = Application()
    app.title("XianXia")
    app.mainloop()
