import psycopg2
import os
from dotenv import load_dotenv


def join_table():
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
                        CREATE TABLE IF NOT EXISTS customers(
                            id SERIAL PRIMARY KEY,
                            event_time TIMESTAMP WITH TIME ZONE,
                            event_type VARCHAR(255),
                            product_id BIGINT,
                            price FLOAT,
                            user_id INT,
                            user_session UUID
                        )"""
        cursor.execute(create_table_query)

        cursor.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public' and
                    table_name LIKE 'data_202%_%%%';
                """)
        tables = cursor.fetchall()

        union_query = ""
        for table in tables:
            table_name = table[0]
            union_query += f"SELECT event_time, event_type, product_id, price, user_id, user_session FROM {table_name} UNION ALL "

        union_query = union_query.rstrip(" UNION ALL ")

        sql_query = f"""
                    INSERT INTO customers(event_time, event_type, product_id, price, user_id, user_session)
                    {union_query};
                """
        cursor.execute(sql_query)
        connection.commit()

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main():
    load_dotenv(os.path.abspath("./.env"))
    join_table()

if __name__ == "__main__":
    main()