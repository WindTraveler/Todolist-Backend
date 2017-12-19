import psycopg2

def connect_db():
    conn = psycopg2.connect(database="notedb", user="postgres", password="postgres", host="localhost", port="5432")
    return conn

class User():


    def get_User(self,sql='',parm=()):
        conn = connect_db()
        self.cur = conn.cursor()
        self.cur.execute(sql,parm)
        self.result =  self.cur.fetchone()
        return self.result


    def set_User(self,sql='',parm=()):
        conn = connect_db()
        self.cur = conn.cursor()
        self.cur.execute(sql, parm)
        conn.commit()
        conn.close()


class Note():


    def get_Note(self,sql='',parm=()):
        conn = connect_db()
        self.cur = conn.cursor()
        self.cur.execute(sql,parm)
        self.result =  self.cur.fetchone()
        return self.result


    def get_AllNote(self,sql='',parm=()):
        conn = connect_db()
        self.cur = conn.cursor()
        self.cur.execute(sql,parm)
        self.result = self.cur.fetchall()
        return self.result


    def set_Note(self,sql='',parm=()):
        conn = connect_db()
        self.cur = conn.cursor()
        self.cur.execute(sql, parm)
        conn.commit()
        conn.close()