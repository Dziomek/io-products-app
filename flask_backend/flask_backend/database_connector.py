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
    def insert_into_users(username, email, password_hash, is_active):
        query = 'INSERT INTO users (username, email, password_hash, is_active) VALUES (%s, %s, %s, %s)', (username, email, password_hash, is_active)
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
