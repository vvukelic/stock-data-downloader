
import argparse

from database import Database


def import_stock_data(symbol, input_file):

    rows = []

    for line in input_file:
        line = line.rstrip('\n')
        rows.append(line.rsplit(' ', 5))
        # date, open, high, low, close, volume = line.rsplit(' ', 5)
        #print(date)

    db = Database('test')
    db.write_rows('daily_stock_data', symbol, rows)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('input_file_path', metavar='PATH', help='input file path with stock data')

    options = parser.parse_args()

    with open(options.input_file_path) as input_file:
        symbol = options.input_file_path.split('/')[1]
        import_stock_data(symbol, input_file)


if __name__ == '__main__':
    main()