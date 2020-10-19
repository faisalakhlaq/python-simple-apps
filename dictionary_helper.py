import mysql.connector
import os


def connect_to_dictionary_db():
    con = mysql.connector.connect(
        user=os.environ.get('DICT_DB_USER'),
        password=os.environ.get('DICT_DB_PASSWORD'),
        host=os.environ.get('DICT_DB_HOST'),
        database=os.environ.get('DICT_DB_NAME'),
    )
    return con


def get_user_input():
    """
    Asks the user to input a work and keeps
    asking until non-empty input is given
    :returns lower case string provided by user
    """
    user_input = input("Enter a word: ")
    # user_input is not None AND user_input is not empty or blank
    while not bool(user_input and user_input.strip()):
        user_input = input("Please enter a word: ")

    return user_input


def search_word(word):
    try:
        conn = connect_to_dictionary_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s'" % word)
        # query = cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s'" % get_user_input())
        results = cursor.fetchall()
        word_definitions = []
        if results:
            for result in results:
                word_definitions.append(result[1])
        # else:
        #     print("Sorry! No Definitions found")
        cursor.close()
        conn.close()
        return word_definitions
    except Exception as error:
        print('Failed to retrieve word definitions: \n', error)
    finally:
        if conn:
            cursor.close()
            conn.close()