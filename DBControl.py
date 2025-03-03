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
            type TEXT,
            question TEXT,
            choice TEXT,
            answer TEXT
        )
        ''')
        self.conn.commit()

    def add_question(self, type:str, question:list, choice:list, answer:list):
        '''
        type: str, 题目类型
        question: list, 题目
        choice: list, 选项
        answer: list, 答案
        '''
        question = json.dumps(question)
        choice = json.dumps(choice)
        answer = json.dumps(answer)
        self.cursor.execute('''
        INSERT INTO question(time, type, question, choice, answer) VALUES(?, ?, ?, ?, ?)
        ''', (int(time.time()), type, question, choice, answer))
        self.conn.commit()

    def get_question(self, type:str):
        '''
        type: str, 题目类型
        '''
        self.cursor.execute('''
        SELECT * FROM question WHERE type=?
        ''', (type,))
        result = self.cursor.fetchall()
        return result
    
if __name__ == '__main__':
    db = DB()
    db.init()
    db.add_question('mc', ['1+1=?'], ['1', '2', '3', '4'], [1, 'B'])
    print(db.get_question('mc'))