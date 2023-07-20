import logging
import mysql.connector
from mysql.connector import errorcode

# import mariadb
# import sqlite3

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

class Database:
    def __init__(self):
        self.host = DB_HOST
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_DATABASE

        try:
            logging.info("DB starting Test-Connection")
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your DB user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.connection.cursor()
            logging.info("DB Test-Connection established!")
            self.__disconnect__()

    def __connect__(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )
        self.cursor = self.connection.cursor()
        logging.debug("DB connection established!")

    def __disconnect__(self):
        self.cursor.close()
        self.connection.close()
        logging.debug("DB cursor and connection closed!")

    def user_exists(self, user_id):
        self.__connect__()
        sql = "SELECT `tg_id` FROM bot_users WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        if result is None:
            return 0
        else:
            return 1
        
    def add_user_empty(self, tg_id, tg_username):
        self.__connect__()
        sql = "INSERT INTO bot_users (`tg_id`,`tg_username`) VALUES (%s, %s)"
        self.cursor.execute(sql, (tg_id, tg_username))
        self.connection.commit()
        #result = self.cursor.fetchall()
        self.__disconnect__()
        return 1
    
    def add_user_question(self, tg_id, user_question):
        self.__connect__()
        sql = "INSERT INTO user_questions (`tg_user`, `user_question`) VALUES ((SELECT `id_bot_users` FROM bot_users WHERE `tg_id` = %s), %s)"
        self.cursor.execute(sql, (tg_id, user_question))
        self.connection.commit()
        #result = self.cursor.fetchall()
        self.__disconnect__()
        return 1
        
    def get_user_question_history(self, user_id):
        self.__connect__()
        sql = "SELECT `user_question` FROM user_questions WHERE `tg_user` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchall()
        self.__disconnect__()
        if result is None:
            return 0
        else:
            return result
        
    def get_user_id(self, user_id):
        self.__connect__()
        sql = "SELECT `id_bot_users` FROM bot_users WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        if result is None:
            return None
        else:
            return result[0]

    def get_user_language(self, user_id):
        self.__connect__()
        sql = "SELECT `language` FROM bot_users WHERE `tg_id` = %s"
        self.cursor.execute(sql, (user_id,))
        result = self.cursor.fetchone()
        self.__disconnect__()
        if result is None:
            return "ru"
        else:
            return result[0]

    def change_user_language(self, user_id, new_language):
        self.__connect__()
        sql = "UPDATE bot_users SET `language` = %s WHERE `tg_id` = %s"
        self.cursor.execute(
            sql,
            (
                new_language,
                user_id,
            ),
        )
        self.connection.commit()
        self.__disconnect__()
        return True