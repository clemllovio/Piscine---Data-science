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
    try:

        sql_query = """SELECT event_time, COUNT(*) FROM customers where event_type='purchase' and event_time >= '2022-10-01 00:00:00' and event_time <= '2023-02-28 23:59:59' GROUP BY event_time;
                    """
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
    plt.plot(date, nbr_date)
    plt.show()



def main():
    load_dotenv(os.path.abspath("../../.env"))
    data = get_data()
    date, nbr_date = zip(*data)
    print(date[0])
    print(nbr_date[0])
    # print(nbr_date[0])
    create_line_chart(date, nbr_date)

if __name__ == "__main__":
    main()