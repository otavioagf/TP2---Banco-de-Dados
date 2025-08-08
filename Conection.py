import psycopg2
from psycopg2 import OperationalError, ProgrammingError, DatabaseError

class Connect:
    def __init__(self, host, db, user, password, port=5432):
        self.host = host
        self.db = db
        self.user = user
        self.password = password
        self.port = port
        self._db = self.connect()
    
    def connect(self):
        try:
            return psycopg2.connect(
                host = self.host,
                database = self.db,
                user = self.user,
                password = self.password,
                port = self.port
            )
        except OperationalError as e:
            print("Erro de conexão:", e)
            return None
        
    def manipulate(self, sql, params=None):
        try:
            with self._db.cursor() as cur:
                cur.execute(sql, params)
                self._db.commit()
            return True
        except (ProgrammingError, DatabaseError) as e:
            print("Erro de manipulação:", e)
            self.reconect()
            return False
    
    def consult(self, sql, params=None):
        try:
            with self._db.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()
        except (ProgrammingError, DatabaseError) as e:
            print("Erro de consulta:", e)
            self.reconect()
            return None
        
    def reconect(self):
        if self._db:
            self._db.close()
        self._db = self.connect()

    def closing(self):
        if self._db:
            self._db.close()