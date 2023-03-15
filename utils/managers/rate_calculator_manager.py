from django.db import connection

from utils.helpers.date_time_helpers import parse_date_from_datetime


class RateCalculatorManager:

    def __get_rate_calculator_raw_query(self):
        return """
                    WITH RECURSIVE temporary_date_table(date) AS (
                      SELECT %(date_from)s::date as date
                      UNION
                      SELECT (date + INTERVAL '1 DAY')::date
                      FROM temporary_date_table
                      WHERE date < %(date_to)s::date
                    )
                    SELECT td.date, group_by_date_table.average_price FROM temporary_date_table AS td
                    LEFT JOIN (
                        SELECT day, ROUND(avg(prices.price), %(max_decimal_place)s) AS average_price FROM prices
                        WHERE prices.orig_code in %(origin_port_list)s
                        AND prices.dest_code in %(destination_port_list)s
                        AND prices.day >= %(date_from)s::date
                        AND prices.day <= %(date_to)s::date
                        GROUP BY day
                        having count(prices.price) > %(max_count)s
                    ) AS group_by_date_table ON group_by_date_table.day = td.date
                    ORDER BY td.date
                """

    def __parse_rate_data(self, raw_data):
        daily_rate_list = []

        for day, average_price in raw_data:
            daily_rate_list.append({
                'day': parse_date_from_datetime(day),
                'average_price': average_price
            })
        return daily_rate_list

    def calculate_rate(self, origin_port, destination_port, date_from, date_to):
        rate_query = self.__get_rate_calculator_raw_query()

        with connection.cursor() as cursor:
            cursor.execute(rate_query, {
                'date_from': date_from,
                'date_to': date_to,
                'origin_port_list': tuple(origin_port),
                'destination_port_list': tuple(destination_port),
                'max_count': 3,
                'max_decimal_place': 2
            })
            formatted_result = self.__parse_rate_data(cursor.fetchall())
            return formatted_result
