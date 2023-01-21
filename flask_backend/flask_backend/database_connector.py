import mysql.connector
import logging
import sys
from flask_backend.database_config import HOST, USER, PASSWORD, DATABASE

class DatabaseConnector:
    # establishing connection to database
    try:
        database = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)

    except mysql.connector.Error as e:
        logging.critical('Connection to database has not been established: ' + str(e))
        sys.exit()

    @staticmethod
    def insert_into_users(username, email, password_hash, is_active, timestamp):
        query = 'INSERT INTO users (username, email, password_hash, is_active, timestamp) VALUES (%s, %s, %s, %s, %s)', (username, email, password_hash, is_active, timestamp)
        print(query)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def select_from_users_by_username(username):
        query = 'SELECT * FROM users WHERE username=%s', (username,)
        print(query)
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            data = []
            for element in cursor:
                data.append(element)
            return data
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def select_from_users_by_email(email):
        query = 'SELECT * FROM users WHERE email=%s', (email,)
        print(query)
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            data = []
            for element in cursor:
                data.append(element)
            return data
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def update_users_account_activation(email):
        query = 'UPDATE users SET is_active=True WHERE email=%s', (email,)
        print(query)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def insert_into_products_history(user_id, name, link, price, timestamp):
        query = 'INSERT INTO products_history (user_id, name, link, price, timestamp) VALUES (%d, %s, %s, %%.2f, %s)', (user_id, name, link, price, timestamp)
        print(query)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def select_from_products_history(user_id):
        query = 'SELECT * FROM products_history WHERE user_id=%d', (user_id,)
        print(query)
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(*query)
            data = []
            for element in cursor:
                data.append(element)
            return data
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def execute_database_retention():
        query_1 = 'DELETE FROM products_history WHERE timestamp < now() - INTERVAL 6 MONTH'
        print(query_1)
        #query_2 = 'DELETE FROM users WHERE timestamp < now() - INTERVAL 6 MONTH'
        #print(query_2)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute('SET SQL_SAFE_UPDATES = 0')
            cursor.execute(*query_1)
            #cursor.execute(*query_2)
            cursor.execute('SET SQL_SAFE_UPDATES = 1')
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))