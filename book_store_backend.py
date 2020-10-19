import os

import psycopg2


class BookDBHelper:

    def __init__(self):
        database_url = os.environ['HEROKU_BOOK_DB_URL']

        self.db_conn = psycopg2.connect(database_url, sslmode='require')
        self.cur = self.db_conn.cursor()

    def insert(self, title, author, year, isbn):
        try:
            postgres_insert_query = """ INSERT INTO book (title,author,year,isbn)
            VALUES (%s,%s,%s,%s)"""
            # Check if there are empty strings and replace them with None
            if not(year and year.strip() and year.isnumeric()):
                year = None
            if not(author and author.strip()):
                author = None
            if not(title and title.strip()):
                title = None
            if not(isbn and isbn.strip() and isbn.isnumeric()):
                isbn = None

            if isbn is None and year is None and title is None and author is None:
                return

            record_to_insert = (title, author, year, isbn)
            self.cur.execute(postgres_insert_query, record_to_insert)
            self.db_conn.commit()
        except(Exception, psycopg2.Error) as error:
            print('Failed to insert book record: \n', error)

    def update(self, book_id, title, author, year, isbn):
        try:
            # Check if there are empty strings and replace them with None
            # s and s.strip()
            if not(year and year.strip() and year.isnumeric()):
                year = None
            if not(author and author.strip()):
                author = None
            if not(title and title.strip()):
                title = None
            if not(isbn and isbn.strip() and isbn.isnumeric()):
                isbn = None

            if book_id is None:
                return False

            update_query = """Update book set title = %s, author = %s, year = %s, 
            isbn = %s where id = %s"""
            record_to_update = (title, author, year, isbn, book_id)
            self.cur.execute(update_query, record_to_update)
            self.db_conn.commit()
        except(Exception, psycopg2.Error) as error:
            print('Failed to update book record: \n', error)

    def delete(self, book_id):
        try:
            delete_query = """Delete from book where id = %s"""
            self.cur.execute(delete_query, (book_id,))
            self.db_conn.commit()
        except(Exception, psycopg2.Error) as error:
            print('Failed to delete book record: \n', error)

    def search_by_id(self, book_id):
        try:
            search_query = "select * from book where id = %s"
            self.cur.execute(search_query, (book_id,))
            row = self.cur.fetchall()
            return row
        except(Exception, psycopg2.Error) as error:
            print('Failed to search book record: \n', error)

    def search_by_field(self, b_title='', b_author='', b_year='', b_isbn=''):
        try:
            search_query = "select * from book where title ILIKE %s OR author ILIKE %s " \
                           "OR year = %s OR isbn = %s"
            # Check if there are empty strings and replace them with None
            # s and s.strip()
            if not(b_year and b_year.strip() and b_year.isnumeric()):
                b_year = None
            if not(b_author and b_author.strip()):
                b_author = None
            if not(b_title and b_title.strip()):
                b_title = None
            if not(b_isbn and b_isbn.strip() and b_isbn.isnumeric()):
                b_isbn = None

            searchable_fields = (b_title, b_author, b_year, b_isbn)
            self.cur.execute(search_query, searchable_fields)
            rows = self.cur.fetchall()
            return rows
        except(Exception, psycopg2.Error) as error:
            print('Failed to search book record: \n', error)

    def fetch_all_books(self):
        try:
            self.cur.execute("SELECT * FROM book")
            rows = self.cur.fetchall()
            return rows
        except(Exception, psycopg2.Error) as error:
            print('Failed to retrieve books record: \n', error)

    def __del__(self):
        self.db_conn.close()
        self.cur.close()

    # connect()
    # delete(4)
    # insert('Pasha','Pasha',2020, 239823)
    # delete(6)
    # print(search_by_field(b_title='Pasha', b_year=''))
    # print(view())
