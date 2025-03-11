import psycopg2
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt

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

        sql_query = """SELECT 
        COUNT(price) AS count,
        AVG(price) AS mean,
        STDDEV(price) AS std,
        MIN(price) AS min,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS "25%",
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY price) AS "50%",
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS "75%",
        MAX(price) AS max
        FROM customers
        WHERE event_type = 'purchase'
        AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59';
        """
        cursor.execute(sql_query)
        result = cursor.fetchall()

        sql_query = """SELECT price
        FROM customers
        WHERE event_type = 'purchase'
        AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59';
        """
        cursor.execute(sql_query)
        result1 = cursor.fetchall()

        sql_query = """SELECT id, SUM(price) / COUNT(price) AS avg_basket_price
FROM customers
WHERE event_type = 'purchase'
AND event_time BETWEEN '2022-10-01 00:00:00' AND '2023-01-31 23:59:59'
GROUP BY id;
                """
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


def create_box_plot(price, q1, q3, average_basket_price):
    if not price:
        return
    # plt.boxplot(price, vert=False, widths=0.7)

    # plt.boxplot(price, vert=False, widths=0.7, showfliers=False)
    # print(average_basket_price)
    plt.boxplot(average_basket_price, vert=False, widths=0.7, flierprops=dict(marker='D', markeredgecolor='black',
                      markerfacecolor='blue'), showfliers=False)

    plt.show()



def main():
    load_dotenv(os.path.abspath("../../.env"))
    data, price, data1 = get_data()
    count, mean, std, min, q1, q2, q3, max = zip(*data)
    print(f'count: {count}\nmean: {mean}\nstd: {std}\nmin: {min}\nq1: {q1}\nq2: {q2}\nq3: {q3}\nmax: {max}')
    create_box_plot([p[0] for p in price], q1[0],q3[0], [d[0] for d in data1])
if __name__ == "__main__":
    main()