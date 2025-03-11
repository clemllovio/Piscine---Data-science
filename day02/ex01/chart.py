import psycopg2
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np
import matplotlib.ticker as mticker

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
    result2 = []
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
                            AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-02-28 23:59:59'
                            GROUP BY TO_CHAR(event_time, 'YYYY-MM') 
                            ORDER BY purchase_month;"""
        cursor.execute(sql_query)
        result1 = cursor.fetchall()

        sql_query = """
        SELECT 
        TO_CHAR(event_time, 'YYYY-MM-DD') AS purchase_day,
        SUM(price) / COUNT(DISTINCT user_id) AS avg_spend_per_customer_per_day
        FROM customers
        WHERE event_type = 'purchase' 
        AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-02-28 23:59:59'
        GROUP BY TO_CHAR(event_time, 'YYYY-MM-DD')
        ORDER BY purchase_day;"""
        cursor.execute(sql_query)
        result2 = cursor.fetchall()

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result, result1, result2

def plot_style(grid):
    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False
    if grid:
        plt.grid(True, color='white')
    else:
        plt.grid(axis = 'y', color='white')
    plt.gca().set_facecolor((0.9176, 0.9176, 0.9451))
    plt.tick_params(left=False, bottom=False)

def create_line_plot(data):
    if not data:
        print("Error: empty data")
        return
    date, nbr_date = zip(*data)

    plot_style(True)
    plt.plot(date, nbr_date)

    plt.xlim([datetime(2022, 10, 1), datetime(2023, 1, 31)])
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.ylabel('Number of customers')

    plt.show()

def create_bar_plot(data):
    if not data:
        print("Error: empty data")
        return

    month, amount = zip(*data)
    formatted_months = [datetime.strptime(m, '%Y-%m').strftime('%b') for m in month]

    plot_style(False)
    plt.bar(formatted_months, amount, color='#B9C4D6', edgecolor='white', zorder=3)

    ax = plt.gca()
    ax.yaxis.get_offset_text().set_visible(False)
    plt.ylabel('total sales in million of A')

    plt.show()

def create_line_plot_full(data):
    if not data:
        print("Error: empty data")
        return

    purchase_day, average_spend_per_customer_per_day = zip(*data)
    purchase_day = [datetime.strptime(day, '%Y-%m-%d') for day in purchase_day]

    plot_style(True)

    plt.plot(purchase_day, average_spend_per_customer_per_day, color='#B9C4D6', zorder=3)
    plt.fill_between(purchase_day, average_spend_per_customer_per_day, color='#B9C4D6', zorder=3)

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.ylabel('average spend/customers in A')

    plt.xlim(purchase_day[0], purchase_day[-1])
    plt.ylim(0, max(average_spend_per_customer_per_day) + 5)

    plt.show()

def main():
    load_dotenv(os.path.abspath("../../.env"))
    data_line_plot, data_bar_plot, data_line_plot_full = get_data()

    create_line_plot(data_line_plot)
    create_bar_plot(data_bar_plot)
    create_line_plot_full(data_line_plot_full)

if __name__ == "__main__":
    main()
