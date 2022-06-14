import tkinter as tk

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
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



if __name__ == "__main__":
    app = Application()
    app.title("XianXia")
    app.mainloop()
