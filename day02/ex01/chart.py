import psycopg2
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

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


    fig, ax = plt.subplots()
    ax.plot(date, nbr_date)
    ax.tick_params(left=False)
    ax.tick_params(bottom=False)
    ax.set_xlim([datetime(2022, 10, 1), datetime(2023, 2, 28)])
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax.grid(True, color='white')
    # ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=4, steps=[1, 2, 3, 6]))
    months = mdates.MonthLocator(bymonth=[10, 11, 12, 1])
    ax.xaxis.set_major_locator(months)
    ax.set_facecolor((0.9176, 0.9176, 0.9451))
    ax.set_ylabel('Number of customers')
    plt.show()



from datetime import datetime

def main():
    load_dotenv(os.path.abspath("../../.env"))
    data = get_data()
    date, nbr_date = zip(*data)
    print(date)
    # print(nbr_date[0])
    # print(nbr_date[0])
    create_line_chart(date, nbr_date)

if __name__ == "__main__":
    main()