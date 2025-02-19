import sqlite3
from abc import ABC, abstractmethod

class Model(ABC):

    def __init__(self) -> None:
        self.name : str = self.get_name()
        self.db_path : str = self.get_db_path()
        self.schema : dict = self.get_schema()

    @abstractmethod
    def get_schema(self) -> dict:
        pass

    @abstractmethod
    def get_db_path(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def table_from_model(self) -> None:
        columns = ''
        for column in self.schema.keys():
            columns = columns + column + " " + self.schema[column] + ","

        conn = sqlite3.connect(self.db_path + ".db")
        with conn :
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.name} ({columns[:-1]})')

    def insert(self, data : tuple) -> None:
        placeholders = ''
        for column in self.schema.keys():
            placeholders = placeholders + "?,"

        conn = sqlite3.connect(self.db_path + ".db")
        with conn:
            c = conn.cursor()
            c.execute(f"INSERT INTO {self.name} VALUES ({placeholders[:-1]})", data)

    def insert_many(self, data_list : list[tuple]) -> None:
        placeholders = ''
        for column in self.schema.keys():
            placeholders = placeholders + "?,"

        conn = sqlite3.connect(self.db_path + ".db")
        with conn:
            c = conn.cursor()
            for data in data_list:
                c.execute(f"INSERT INTO {self.name} VALUES ({placeholders[:-1]})", data)        

    def get_all(self, rowid = False) -> list:
        conn = sqlite3.connect(self.db_path + '.db')
        query = None

        _rowid = "rowid, " if rowid == True else ""

        with conn:
            c = conn.cursor()
            c.execute(f'SELECT {_rowid} * FROM {self.name}')
            query = c.fetchall()
        
        return query

    def get_first(self, _column : str, _operator : str, _filter : str, rowid = False) -> tuple:

        conn = sqlite3.connect(self.db_path + ".db")
        query = None

        _rowid = "rowid, " if rowid == True else ""

        with conn:
            c = conn.cursor()
            ftr = _filter
            if type(_filter) == str:
                ftr = f"'{_filter}'"
            command = f"SELECT {_rowid} * FROM {self.name} WHERE {_column}{_operator}{ftr}"
            c.execute(command)
            query = c.fetchone()
        return query

    def get_where(self, _column : str, _operator : str, _filter : str, rowid = False) -> list:

        conn = sqlite3.connect(self.db_path + ".db")
        query = None

        _rowid = "rowid, " if rowid == True else ""

        with conn:
            c = conn.cursor()
            ftr = _filter
            if type(_filter) == str:
                ftr = f"'{_filter}'"
            command = f"SELECT {_rowid} * FROM {self.name} WHERE {_column} {_operator} {ftr}"
            c.execute(command)
            query = c.fetchall()
        return query

    def get_where_in_list(self,  _column : str, _list : list, rowid = False):
        conn = sqlite3.connect(self.db_path + ".db")
        query = None
        _rowid = "rowid, " if rowid == True else ""

        alias_list = ''

        for i in range(len(_list)):
            alias_list += '?,'

        with conn:
            c = conn.cursor()
            command = f"SELECT {_rowid} * FROM {self.name} WHERE {_column} IN ({alias_list[:-1]})"
            c.execute(command, _list)
            query = c.fetchall()
        return query        

    def get_columns(self, _columns : list[str]):
        columns = ""
        for column in _columns:
            columns = columns + column + ","

        conn = sqlite3.connect(self.db_path + '.db')
        query = None

        with conn:
            c = conn.cursor()
            c.execute(f'SELECT {columns[:-1]} FROM {self.name}')
            query = c.fetchall()       

        return query

    def get_column_as_list(self, _column : str):
        conn = sqlite3.connect(self.db_path + '.db')
        query = None

        with conn:
            c = conn.cursor()
            c.execute(f'SELECT {_column} FROM {self.name}')
            query = c.fetchall()
        
        return [i[0] for i in query]  

    def get_distinct_column_as_list(self, _column : str):
        conn = sqlite3.connect(self.db_path + '.db')
        query = None

        with conn:
            c = conn.cursor()
            c.execute(f'SELECT DISTINCT {_column} FROM {self.name}')
            query = c.fetchall()
        
        return [i[0] for i in query]         

    def delete_where(self, _column : str, _operator : str, _filter : str) -> None:

        conn = sqlite3.connect(self.db_path + ".db")
        with conn:
            c = conn.cursor()
            if type(_filter) == str:
                ftr = f"'{_filter}'"
            c.execute(f"DELETE FROM {self.name} WHERE {_column} {_operator} {ftr}")

    def delete_by_rowid(self, rowid : int) -> None:

        conn = sqlite3.connect(self.db_path + ".db")
        with conn:
            c = conn.cursor()
            c.execute(f"DELETE FROM {self.name} WHERE rowid = ?", (rowid,))        

    def update_by_rowid(self, data : tuple) -> None:

        set_text = ""

        for key in self.schema.keys():

            set_text = set_text + str(key) + " = ? ,"

        conn = sqlite3.connect(self.db_path + ".db")
        with conn:
            c = conn.cursor()
            c.execute(f"UPDATE {self.name} SET {set_text[:-1]} WHERE rowid = ?", data)

class LikersModel(Model):
    def get_schema(self) -> dict:
        schema = {
            'username' : 'text',
            'full_name' : 'text',
            'is_private' : 'text',
            'source_target' : 'text',
            'post_id' : 'text',
        }
        return schema
    
    def get_name(self) -> str:
        return "LikersTable"
    
    def get_db_path(self) -> str:
        return 'data\\likers_data'
    
if __name__ == "__main__":
    likers = LikersModel()
    likers.table_from_model()
    