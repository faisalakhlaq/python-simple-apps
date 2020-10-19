from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import validators, SubmitField

from datetime import datetime

from stock_analysis import StockAnalyzer
from book_store_backend import BookDBHelper
from dictionary_helper import search_word
from real_estate_scraper import RockSpringScraper

app = Flask(__name__)
app.config['SECRET_KEY'] = '#$%^&*'


@app.route('/')
def home():
    return render_template("home.html")


class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Fetch Stock Data')


@app.route('/c_currency_data')
def c_currency_data():
    from .forms import CryptoFetcherForm
    form = CryptoFetcherForm()
    return render_template('crypto_fetcher.html', form=form)


@app.route('/stock_analysis', methods=['GET', 'POST'])
def stock_data():
    list_of_tickers = []
    with open("tickers.txt", mode='r') as file:
        list_of_tickers.append(str(ticker) for ticker in file.readlines())
        # for line in file.readlines():
        #     tickers.append(line)
    form = InfoForm()
    if request.method == 'GET':
        return render_template("stock_data.html", list_of_tickers=list_of_tickers, form=form)

    elif request.method == 'POST':
        if not form.validate_on_submit() or \
                form.startdate.data > form.enddate.data or \
                form.startdate.data > datetime.date(datetime.now()):
            error_message = "Invalid Dates!"
            return render_template("stock_data.html", list_of_tickers=list_of_tickers,
                                   error_message=error_message, form=form)

        stock_ticker = request.form.get('stock_ticker_list')
        start_date = form.startdate.data
        end_date = form.enddate.data
        data = StockAnalyzer().get_graph(stock_ticker, start_date, end_date)
        return render_template("stock_data.html", list_of_tickers=list_of_tickers,
                               script1=data[0], div1=data[1], cdn_js=data[2], form=form)


@app.route('/api_spider', methods=['GET', 'POST'])
def api_spider():
    if request.method == 'POST':
        from api_spider import ProgrammablewebSpider
        apis = ProgrammablewebSpider().get_api_details()
        if apis is not None:
            return render_template("api_scraper.html",
                                   html_data=[apis.to_html(classes='data')])
        else:
            print("Got no results")
            # TODO return an error message
    return render_template("api_scraper.html")


@app.route('/web_scraper', methods=['GET', 'POST'])
def web_scraper():
    if request.method == 'GET':
        return render_template("web_scraper.html")
    elif request.method == 'POST':
        if request.form.get('rock_spring_properties'):
            try:
                rs = RockSpringScraper()
                rs_properties = rs.fetch_rockspring_properties()
                if rs_properties is not None:
                    return render_template("web_scraper.html",
                                           html_data=[rs_properties.to_html(classes='data')])
                else:
                    print("Got no results")
                    # TODO return an error message
                    return render_template("web_scraper.html")
            except Exception as error:
                print(error)


@app.route('/dictionary/', methods=['GET', 'POST'])
def dictionary():
    if request.method == 'GET':
        return render_template("dictionary.html")
    elif request.method == 'POST':
        # if request.form.get("search_btn"):
        #     print('Search button pressed')
        word_definitions = search_word(str(request.form.get('search_word')))
        if not word_definitions:
            word_definitions = ["Please enter another word"]
        return render_template("dictionary.html", word_definitions=word_definitions)


@app.route('/book_store/', methods=['GET', 'POST'])
def book_store():
    if request.method == 'GET':
        helper = BookDBHelper()
        books = helper.fetch_all_books()
        return render_template("book_store.html", books=books, book=None)

    elif request.method == 'POST':
        book = None
        title = request.form.get('title')
        author = request.form.get('author')
        year = request.form.get('year')
        isbn = request.form.get('isbn')
        book_id = request.form.get('displayed_book_id')

        helper = BookDBHelper()
        if request.form.get("search"):
            books = helper.search_by_field(b_title=title, b_author=author,
                                           b_year=year, b_isbn=isbn)
            return render_template("book_store.html", books=books, book=book)
        elif request.form.get("view_all"):
            books = helper.fetch_all_books()
            return render_template("book_store.html", books=books, book=book)
        elif request.form.get("add_new"):
            helper.insert(title=title, author=author,
                          year=year, isbn=isbn)
            books = helper.fetch_all_books()
            return render_template("book_store.html", books=books, book=book)
        elif request.form.get("delete"):
            book = helper.delete(book_id)
            books = helper.fetch_all_books()
            return render_template("book_store.html", books=books, book=book)
        elif request.form.get("edit"):
            book = helper.search_by_id(request.form.get('edit'))
            if len(book) == 0:
                book = None
            books = helper.fetch_all_books()
            return render_template("book_store.html", books=books, book=book)
        elif request.form.get("update"):
            helper.update(book_id=book_id, title=title, author=author,
                          year=year, isbn=isbn)
            books = helper.fetch_all_books()
            return render_template("book_store.html", books=books, book=book)

        books = helper.fetch_all_books()
        return render_template("book_store.html", books=books, book=None)


@app.route('/projects/')
def projects():
    return render_template("projects.html")


@app.route('/map/')
def world_map():
    return render_template("map.html")


if __name__ == "__main__":
    # static_folder = "your path to static"
    app.run(debug=True)
