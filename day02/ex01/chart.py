import psycopg2
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def get_data():
    connection_params = {
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': os.getenv("HOST"),
        'port': os.getenv("POSTGRES_PORT")
    }

    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()
    result = []
    result1 = []
    try:

        sql_query = """SELECT DATE(event_time) AS purchase_date, COUNT(*) AS customer_count
                    FROM customers
                    WHERE event_type = 'purchase' 
                    AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-02-28 23:59:59'
                    GROUP BY purchase_date
                    ORDER BY purchase_date;"""
        cursor.execute(sql_query)
        result = cursor.fetchall()

        sql_query = """SELECT TO_CHAR(event_time, 'YYYY-MM') AS purchase_month, SUM(price) AS total_price
                            FROM customers
                            WHERE event_type = 'purchase' 
                            AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59'
                            GROUP BY TO_CHAR(event_time, 'YYYY-MM') 
                            ORDER BY purchase_month;"""
        cursor.execute(sql_query)
        result1 = cursor.fetchall()

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result, result1


def create_line_chart(date, nbr_date):
    # if not data:
    #     return
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False

    plt.plot(date, nbr_date)
    plt.tick_params(left=False, bottom=False)

    plt.xlim([datetime(2022, 10, 1), datetime(2023, 1, 31)])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    plt.grid(True, color='white')

    plt.gca().set_facecolor((0.9176, 0.9176, 0.9451))
    plt.ylabel('Number of customers')
    plt.show()

def create_bar_plot(month, amout):
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    formatted_months = [datetime.strptime(m, '%Y-%m').strftime('%b') for m in month]
    plt.bar(formatted_months, amout)
    plt.tick_params(left=False, bottom=False)
    plt.gca().set_facecolor((0.9176, 0.9176, 0.9451))
    plt.ylabel('total sales in million of A')
    plt.show()

def main():
    load_dotenv(os.path.abspath("../../.env"))
    data, data1 = get_data()
    date, nbr_date = zip(*data)
    print(data1)
    month, amount = zip(*data1)
    create_line_chart(date, nbr_date)
    create_bar_plot(month, amount)

if __name__ == "__main__":
    main()
