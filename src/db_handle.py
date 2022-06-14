import sqlite3 as sql

class Database(object):
    """sqlite3 database class that holds testers jobs"""
    DB_LOCATION = "../data/xianxia_db.sqlite"

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
        self.commit()




    def close(self):
        """close sqlite3 connection"""
        self.connection.close()


    def novel_list(self):
        self.cur.execute(""" SELECT name from novels""")
        rows = self.cur.fetchall()
        return rows




    def commit(self):
        """commit changes to database"""
        self.connection.commit()
