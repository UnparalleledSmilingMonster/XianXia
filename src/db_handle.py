import sqlite3 as sql
import sys
import os

class Database(object):

    DB_LOCATION_FILE = "../data/xianxia_db.sqlite"
    DB_LOCATION_EXE = "./data/xianxia_db.sqlite"
    
    TABLE_PARAMETER = "{TABLE_PARAMETER}"
    DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
    GET_TABLES_SQL = "SELECT name FROM sqlite_master WHERE type='table';"

    def __init__(self):
        """Initialize db class variables"""
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            config_path = os.path.join(application_path, Database.DB_LOCATION_EXE)
        elif __file__:
            application_path = os.path.dirname(__file__)            
            config_path = os.path.join(application_path, Database.DB_LOCATION_FILE)
            
        self.connection = sql.connect(config_path)
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
        self.cur.execute("""SELECT max(id) FROM novels;""")
        novel_id = self.cur.fetchone()[0]
        
        query_create_novel = """CREATE TABLE IF NOT EXISTS """ + self.scrub(name) + str(novel_id) + """ (
            id integer PRIMARY KEY,
            hanzi text NOT NULL,
            pinyin text NOT NULL,
            meaning text NOT NULL,
            chapter integer,
            type text
            );"""
            
        self.cur.execute(query_create_novel)
        self.commit()
        return novel_id
    
    def number_chapters(self, novel_id):
        query_nb_chapters = """ SELECT COUNT( DISTINCT chapter) FROM """ + self.novel_table_name(novel_id) + """ ; """
        self.cur.execute(query_nb_chapters)
        return self.cur.fetchone()
    
    def novel_name(self, novel_id):
        query_novel_name = """ SELECT name FROM novels WHERE id == ?; """
        self.cur.execute(query_novel_name, (novel_id,))
        return self.cur.fetchone()
    
    def novel_table_name(self, novel_id):
        return self.scrub(self.novel_name(novel_id)) + str(novel_id)
    
    def search_word(self, novel_id, hanzi):
        query_search_word = """SELECT hanzi, pinyin, meaning FROM """ + self.novel_table_name(novel_id) + """ 
            WHERE hanzi == ? ; """
        self.cur.execute(query_search_word, (hanzi,))
        res = self.cur.fetchone()
        return res
    
    def similarities(self, novel_id, hanzi):
        query_similarities = """SELECT hanzi, pinyin, meaning FROM """ + self.novel_table_name(novel_id) + """ 
            WHERE hanzi LIKE ? ; """
        self.cur.execute(query_similarities, ("%"+hanzi+"%",))
        res = self.cur.fetchall()
        return res
        


    def close(self):
        """close sqlite3 connection"""
        self.connection.close()


    def novel_list(self):
        self.cur.execute(""" SELECT id,name from novels""")
        rows = self.cur.fetchall()
        return rows

    
    def get_vocab(self, novel_id, word_type, chapter = None):
        if chapter == None :
            query_add_novel = """SELECT hanzi, pinyin, meaning FROM """   + self.novel_table_name(novel_id)  + """
             WHERE type == ?;"""
            self.cur.execute(query_add_novel, (word_type,))
        else :
            query_add_novel = """SELECT hanzi, pinyin, meaning FROM """   + self.novel_table_name(novel_id)  + """ 
                WHERE type == ? AND chapter == ? ;"""
            self.cur.execute(query_add_novel, (word_type, chapter))
        rows = self.cur.fetchall()
        return rows
  
    def exists(self, novel_id, hanzi):
        if self.search_word(novel_id, hanzi) is not None : return True
        return False
    
    
    
    def new_word(self, novel_id, hanzi, pinyin, meaning, word_type, chapter = None):
        if chapter == None :
            query_new_word = """ INSERT INTO """ + self.novel_table_name(novel_id) + """ (hanzi, pinyin, meaning, type) values (?,?,?,?);"""
            self.cur.execute(query_new_word, (hanzi, pinyin, meaning, word_type))
        else :
            query_new_word = """ INSERT INTO """ + self.novel_table_name(novel_id) + """ (hanzi, pinyin, meaning, type, chapter) values (?,?,?,?,?);"""
            self.cur.execute(query_new_word, (hanzi, pinyin, meaning, word_type, chapter))
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
    
    
