import psycopg2
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
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

        sql_query = """SELECT user_id, COUNT(*) AS nbr_order, SUM(price) AS total_spent
                    FROM customers
                    WHERE event_type = 'purchase'
                    AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59'
                    GROUP BY user_id;"""

        cursor.execute(sql_query)
        result = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return result


def create_bart_chart_frequency(data):
    if not data:
        return

    try:
        nbr_data, type_data = zip(*data)
        print(nbr_data)
        print(type_data)
        plt.pie(nbr_data, labels=type_data, autopct='%1.1f%%')
        plt.show()
    except ValueError as e:
        print(f"Error unpacking data: {e}")


def main():
    load_dotenv(os.path.abspath("../../.env"))
    data = get_data()
    # nbr_customer = len(data)
    # print(data)
    user_id, nbr_order, total_spent = zip(*data)

    # frequency
    # plt.hist(nbr_order, bins=5, range=[0, 40])
    # plt.xticks(np.arange(0, 50 , 10))

    # monetary value
    # plt.hist(total_spent, bins=5, range=[0,250])
    # plt.show()

if __name__ == "__main__":
    main()