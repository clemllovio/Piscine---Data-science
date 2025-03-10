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

        sql_query = """SELECT COUNT(*) AS "Number of event_type", event_type 
                        FROM customers 
                        GROUP BY event_type;
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


def create_pie_chart(data):
    if not data:
        return

    try:
        nbr_data, type_data = zip(*data)
        plt.pie(nbr_data, labels=type_data, autopct='%1.1f%%')
        plt.show()
    except ValueError as e:
        print(f"Error unpacking data: {e}")


def main():
    load_dotenv(os.path.abspath("../../.env"))
    data = get_data()
    create_pie_chart(data)

if __name__ == "__main__":
    main()