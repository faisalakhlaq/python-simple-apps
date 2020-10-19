from flask import Flask, render_template, request, flash


app = Flask(__name__)
app.config['SECRET_KEY'] = '#$%^&*'


@app.route('/', methods=['GET', 'POST'])
def c_currency_data():
    from forms import CryptoFetcherForm
    from crypto import CoinMarket
    form = CryptoFetcherForm()
    crypto_symbols = list(CoinMarket().get_cur_symol_id().values())
    if request.method == 'POST':
        # import pdb; pdb.set_trace()
        if form.add_currency.data:
            if form.validate_on_submit():
                symbol = form.currency_symbol.data
                form.currency_symbol.data = None
                amount = form.amount.data
                form.amount.data = ''
                form.currencies.data = str(form.currencies.data) + \
                                       str(symbol) +'-'+ str(amount) + '\n'
        elif form.fetch_data.data:
            # 1. Get the currencies from textarea
            # 2. Check if they are valid or send directly if the api won't crash with wrong symbols
            # 3. Put the returned data in a tabular form
            txtarea = form.currencies.data
            amount = txtarea.split()
            currencies = {}
            seperator = '-'
            for cur in amount:
                k = cur.split(seperator, 1)
                # v = cur.split(seperator, 1)[1]
                currencies[str(k[0]).upper()] = k[1]
            try:
                data = CoinMarket().get_crypto_portfolio(currencies)
                return render_template('crypto_fetcher.html', form=form,
                                       list_data=data, crypto_symbols=crypto_symbols)
            except ValueError as e:
                flash(str(e)) # TODO FIXME not being displayed
                print(e)
            # print(str(currencies))
    return render_template('crypto_fetcher.html', form=form,
                           crypto_symbols=crypto_symbols)


if __name__ == "__main__":
    app.run(debug=True)