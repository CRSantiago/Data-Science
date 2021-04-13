import cufflinks as cf
import yfinance as yf
import datetime

with open('500-stock-names.txt', 'r') as stocks:
    lines = stocks.readlines()

    ticker_list = []

    for l in lines:
        ticker_list.append(l.replace('\n', ''))

def get_ticker_input():
    while True:
        ticker_input = input('Enter the symbol of the stock you want to check: \n')
        if ticker_input.upper() in ticker_list:
            break
        else:
            print('Please enter a valid symbol')
            continue
    return ticker_input

def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_dates():
    # GET START DATE
    while True:
        start_date_entry = input('Enter start date in YYYY-MM-DD format: \n')
        if validate_date(start_date_entry):
            sYear,sMonth, sDay = map(int, start_date_entry.split('-'))
            start_date = datetime.date(sYear,sMonth,sDay)
            break
        else:
            print('Improper date format')
            continue

    # GET END DATE
    while True:
        end_date_entry = input('Enter end date in YYYY-MM-DD format: \n')
        if validate_date(end_date_entry):
            eYear, eMonth, eDay = map(int, end_date_entry.split('-'))
            end_date = datetime.date(eYear, eMonth, eDay)
            break
        else:
            print('Improper date format')
            continue

    return start_date, end_date

ticker_symbol = get_ticker_input()
start_date, end_date = get_dates()

ticker_data = yf.Ticker(ticker_symbol)
ticker_df = ticker_data.history(period='1d',start=start_date, end=end_date)
qf = cf.QuantFig(ticker_df, title=f"{ticker_data.info['longName']} Price Data", legend='top', name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
fig.write_image('fig1.png')