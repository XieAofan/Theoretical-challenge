import sqlite3
import time, json
from datetime import datetime

class DB:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
    
    def init(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS question(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            username TEXT,
            duration INTEGER,
            score REAL
        )
        ''')
        self.conn.commit()

    def add(self, username:str, duration:float, score:int):
        self.cursor.execute('''
        INSERT INTO question(time, username, duration, score) VALUES(?, ?, ?, ?)
        ''', (self.timestamp_to_date(time.time()), username, duration, score))
        self.conn.commit()

    def get_question(self, time=''):
        '''
        time: str, 题目类型
        username: str, 用户名
        duration: int, 用时
        score: float, 得分
        '''
        if time != '':
            self.cursor.execute('''
            SELECT * FROM question WHERE time=?
            ''', (time,))
            result = self.cursor.fetchall()
            return result
        
        self.cursor.execute('''
        SELECT * FROM question
        ''')
        result = self.cursor.fetchall()
        return result
    
    # 新增函数：将时间戳转换为日期
    def timestamp_to_date(self, timestamp: int) -> str:
        """
        将时间戳转换为日期字符串。
        
        :param timestamp: 时间戳（整数）
        :return: 日期字符串，格式为 "YYYY-MM-DD"
        """
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    def close(self):
        self.conn.close()

if __name__ == '__main__':
    db = DB()
    db.init()