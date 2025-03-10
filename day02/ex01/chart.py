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
    try:

        sql_query = """SELECT DATE(event_time) AS purchase_date, COUNT(*) AS customer_count
                    FROM customers
                    WHERE event_type = 'purchase' 
                    AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-02-28 23:59:59'
                    GROUP BY purchase_date
                    ORDER BY purchase_date;"""
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return (result)
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return (result)


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


def main():
    load_dotenv(os.path.abspath("../../.env"))
    data = get_data()
    date, nbr_date = zip(*data)
    print(date)
    create_line_chart(date, nbr_date)

if __name__ == "__main__":
    main()
