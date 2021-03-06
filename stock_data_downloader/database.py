
from influxdb import InfluxDBClient


class Database(object):

    def __init__(self, db_name):
        self._client = InfluxDBClient('localhost', 8086, 'root', 'root', db_name)


    def write_rows(self, measurement, symbol, rows):
        points = []

        for row in rows:
            point = self._make_point(measurement, symbol, *row)
            points.append(point)

        self._client.write_points(points, time_precision='s')


    def delete_row(self, symbol, date):
        query_str = 'delete from stock where time = \'{0}\' and symbol = \'{1}\''.format(date, symbol)
        self._client.query(query_str)


    def get_last_timestamp(self, symbol):
        query_str = 'select last(close) from daily_stock_data where symbol = \'{0}\''.format(symbol.upper())
        result = self._client.query(query_str, epoch='s')

        point = next(result.get_points(), None)

        if point:
            return point['time']

        return 0


    def _make_point(self, measurement, symbol, timestamp, open, high, low, close, volume):
        return {
                'measurement' : measurement,
                'tags' :
                {
                    'symbol' : symbol
                },
                'time' : timestamp,
                'fields' :
                {
                    'open'   : float(open),
                    'high'   : float(high),
                    'low'    : float(low),
                    'close'  : float(close),
                    'volume' : int(volume)
                }
            }
