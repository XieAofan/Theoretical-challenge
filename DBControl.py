import sqlite3
import time, json

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
    
    def init(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS question(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time INTEGER,
            username TEXT,
            duration INTEGER,
            score REAL
        )
        ''')
        self.conn.commit()

    def add(self, username:str, duration:float, score:int):
        self.cursor.execute('''
        INSERT INTO question(time, username, duration, score) VALUES(?, ?, ?, ?)
        ''', (int(time.time()), username, duration, score))
        self.conn.commit()

    def get_question(self, type:str):
        '''
        type: str, 题目类型
        username: str, 用户名
        duration: int, 用时
        score: float, 得分
        '''
        self.cursor.execute('''
        SELECT * FROM question
        ''')
        result = self.cursor.fetchall()
        return result
    
if __name__ == '__main__':
    db = DB()
    db.init()