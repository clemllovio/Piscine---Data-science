import psycopg2
import glob
import os
from dotenv import load_dotenv


load_dotenv(os.path.abspath("./.env"))


def create_table_and_copy_data(csv_path: str, table_name: str):
    """
    Creates a table in the PostgreSQL database if it doesn't exist and
    loads the provided DataFrame into it.
    """

    connection_params = {
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': os.getenv("HOST"),
        'port': os.getenv("POSTGRES_PORT")
    }

    connection = psycopg2.connect(**connection_params)
    cursor = connection.cursor()

    try:
        create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name}(
                    event_time TIMESTAMP WITH TIME ZONE,
                    event_type VARCHAR(255),
                    product_id BIGINT,
                    price FLOAT,
                    user_id INT,
                    user_session UUID
                )"""
        cursor.execute(create_table_query)

        with open(csv_path, 'r') as f:
            next(f)
            columns = ("event_time, event_type, product_id, "
                       "price, user_id, user_session")
            cursor.copy_expert(
                f"COPY {table_name} ({columns}) FROM STDIN WITH CSV",
                f
            )

        connection.commit()
        print(f"Successfully copied data from {csv_path} to {table_name}")

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()


def main():
    """
    Iterates through all CSV files in a directory
    and processes them by calling `create_table_and_copy_data`
    """
    joined_list = glob.glob("subject/customer/*.csv")
    for csv_file in joined_list:
        create_table_and_copy_data(csv_file,
                                   csv_file.split('/')[-1].replace('.csv', ''))


if __name__ == "__main__":
    main()
