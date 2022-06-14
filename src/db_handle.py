import sqlite3 as sql

class Database(object):

    DB_LOCATION = "../data/xianxia_db.sqlite"
    TABLE_PARAMETER = "{TABLE_PARAMETER}"
    DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
    GET_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type='table';"

    def __init__(self):
        """Initialize db class variables"""
        self.connection = sql.connect(Database.DB_LOCATION)
        self.cur = self.connection.cursor()
        self.instantiate()


    def instantiate(self):
        query_create_novels_table = """CREATE TABLE IF NOT EXISTS novels (
            id integer PRIMARY KEY,
            name text NOT NULL,
            eng_name text
            );"""

        self.cur.execute(query_create_novels_table)

        
    def create_novel(self, name):
        query_add_novel = """INSERT INTO novels (name) VALUES (?);"""
        self.cur.execute(query_add_novel,(name,))
        
        query_create_novel = """CREATE TABLE IF NOT EXISTS """ + self.scrub(name) + """ (
            id integer PRIMARY KEY,
            hanzi text NOT NULL,
            pinyin text NOT NULL,
            meaning text NOT NULL,
            chapter integer,
            type text
            );"""
            
        self.cur.execute(query_create_novel)
        self.commit()
    
    def number_chapters(self, novel):
        query_nb_chapters = """ SELECT COUNT( DISTINCT chapter) FROM """ + self.scrub(novel) + """ ; """
        self.cur.execute(query_nb_chapters)
        return self.cur.fetchone()
    

    
    def search_word(self, novel, word):
        query_search_word = """SELECT hanzi, pinyin, meaning FROM """ + self.scrub(novel) + """ 
            WHERE hanzi == ? ; """
        self.cur.execute(query_search_word, (word,))
        res = self.cur.fetchone()
        return res
    


    def close(self):
        """close sqlite3 connection"""
        self.connection.close()


    def novel_list(self):
        self.cur.execute(""" SELECT name from novels""")
        rows = self.cur.fetchall()
        return [i for (i,) in rows]

    
    def get_vocab(self, name, chapter = None):
        if chapter == None :
            query_add_novel = """SELECT hanzi, pinyin, meaning FROM """   + self.scrub(name)  + """ ;"""
            self.cur.execute(query_add_novel)
        else :
            query_add_novel = """SELECT hanzi, pinyin, meaning FROM """   + self.scrub(name)  + """ 
                WHERE chapter == ?"""
            self.cur.execute(query_add_novel, (chapter, ))
        rows = self.cur.fetchall()
        return rows
   
    def new_word(self, novel, hanzi, pinyin, meaning, chapter = None):
        if chapter == None :
            query_new_word = """ INSERT INTO """ + self.scrub(novel) + """ (hanzi, pinyin, meaning) values (?,?,?);"""
            self.cur.execute(query_new_word, (hanzi, pinyin, meaning))
        else :
            query_new_word = """ INSERT INTO """ + self.scrub(novel) + """ (hanzi, pinyin, meaning, chapter) values (?,?,?,?);"""
            self.cur.execute(query_new_word, (hanzi, pinyin, meaning, chapter))
        self.commit()
        
    
    def commit(self):
        """commit changes to database"""
        self.connection.commit()
       
       
       
    # Mainly for debug from this point :
    

    def get_tables(self):
        self.cur.execute(Database.GET_TABLES_SQL)
        tables = self.cur.fetchall()
        return tables

        
    def delete_table(self, tables):
        for table, in tables:
           sql = Database.DROP_TABLE_SQL.replace(Database.TABLE_PARAMETER, table)
           self.cur.execute(sql)
        
    def reset(self):
        tables = self.get_tables()
        self.delete_table(tables)
        
    def scrub(self, word):
        return ''.join( chr for chr in word if chr.isalnum() )  
    
