#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import MySQLdb
import constants
from pandas import DataFrame
import telebot
bot = telebot.TeleBot(constants.token)
#df = DataFrame({'Имя':names, 'Номер': phones})
#df.to_excel('clients.xlsx', sheet_name='sheet1', index=False)

class MySQL:
    def __init__(self):
        self.connection = MySQLdb.connect (host = constants.host,
                               user = constants.user,
                               passwd = constants.passwd,
                               db = constants.db)
        self.cursor = self.connection.cursor()
    def check_version(self):
        with self.connection:
            self.cursor.execute("SELECT VERSION()")
            return self.cursor.fetchall()
    def select_users(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM business")
            return self.cursor.fetchall()
    def insert_user(self,ids,name,phone_number):
        with self.connection:
            self.cursor.execute("INSERT INTO business values(%s,%s,%s)",(ids,name,phone_number))

class SQLight:
    #create table users(user_id,nomer,aty_zhoni,sala,syltau,kadam_1,kadam_3,kadam_4,kadam_5);
    def __init__(self):
        self.connection = sqlite3.connect(constants.db_name)
        self.cursor = self.connection.cursor()
    def check_user_exists(self,nomer):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM users WHERE nomer = ? ',(user_id,)).fetchall())>0

    def select_users(self):
        with self.connection:
            data =  self.cursor.execute('SELECT * FROM users').fetchall()
            temp_data = []
            for row in data:
                temp_data.append(list(row))
            return temp_data
    def register_user(self,user_id,nomer,aty_zhoni):
        with self.connection:
            return self.cursor.execute('INSERT INTO users (user_id, nomer, aty_zhoni) values(?,?,?)',(user_id, nomer, aty_zhoni))
    def update_sala(self, user_id, sala):
        with self.connection:
            return self.cursor.execute('UPDATE users set sala = ? where user_id = ? ',(sala, user_id))
    def update_syltau(self, user_id, syltau):
        with self.connection:
            return self.cursor.execute('UPDATE users set syltau = ? where user_id = ? ',(syltau, user_id))
    def update_kadam_1(self, user_id, kadam_1):
        with self.connection:
            return self.cursor.execute('UPDATE users set kadam_1 = ? where user_id = ? ',(kadam_1, user_id))
    def update_kadam_3(self, user_id,  kadam_3):
        with self.connection:
            return self.cursor.execute('UPDATE users set kadam_3 = ? where user_id = ? ',(kadam_3, user_id))
    def update_kadam_4(self, user_id, kadam_4):
        with self.connection:
            return self.cursor.execute('UPDATE users set kadam_4 = ? where user_id = ? ',(kadam_4, user_id))
    def update_kadam_5(self, user_id, kadam_5):
        with self.connection:
            return self.cursor.execute('UPDATE users set kadam_5 = ? where user_id = ? ',(kadam_5, user_id))



    def get_excel(self,user_id):
        with self.connection:
            try:
                data = self.select_users()
                temp_names = []
                temp_phones = []
                temp_sala = []
                temp_syltau = []
                temp_kadam_1 = []
                temp_kadam_3 = []
                temp_kadam_4 = []
                temp_kadam_5 = []

                for info in data:
                    temp_names.append(info[2])
                    temp_phones.append(info[1])
                    temp_sala.append(info[3])
                    temp_syltau.append(info[4])
                    temp_kadam_1.append(info[5])
                    temp_kadam_3.append(info[6])
                    temp_kadam_4.append(info[7])
                    temp_kadam_5.append(info[8])

                #df = DataFrame({'1. Аты-жөні':temp_names, '2. Телефон номері': temp_phones,'3. Сала бар|жоқ': temp_sala,'4. Сылтаулары': temp_syltau, '5. Қадам-1': temp_kadam_1,'6. Қадам-3': temp_kadam_3,'7. Қадам-4': temp_kadam_4,'8. Қадам-5': temp_kadam_5})
                df = DataFrame({'Аты-жөні':temp_names, 'Телефон номері': temp_phones,'Сала бар|жоқ': temp_sala,'Сылтаулары': temp_syltau, 'Қадам-1': temp_kadam_1,'Қадам-3': temp_kadam_3,'Қадам-4': temp_kadam_4,'Қадам-5': temp_kadam_5})
                df.to_csv(constants.csv, encoding='utf-8', index=False)
                #df.to_excel('clients.xlsx', sheet_name="sheet1", index=False)

                doc = open(constants.csv, 'rb')
                bot.send_document(user_id, doc)
            except:
                print("ERROR")
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()

if '__main__' == __name__:
    sql_db = SQLight()
    #mysql_db = MySQL()
    #print(sql_db.register_user(123,87774545454,"Kairat"))
    #print(sql_db.select_users())
    #print(sql_db.get_excel(2))
