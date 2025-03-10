import psycopg2
import os
from dotenv import load_dotenv

def delete_duplicates():
    connection_params = {
        'dbname': os.getenv("POSTGRES_DB"),
        'user': os.getenv("POSTGRES_USER"),
        'password': os.getenv("POSTGRES_PASSWORD"),
        'host': os.getenv("HOST"),
        'port': os.getenv("POSTGRES_PORT")
    }

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS temp_table;")

        create_table_query = f"""
                            CREATE TABLE IF NOT EXISTS "temp_table"(
                                ID SERIAL PRIMARY KEY,
                                event_time TIMESTAMP WITH TIME ZONE,
                                event_type VARCHAR(255),
                                product_id BIGINT,
                                price FLOAT,
                                user_id INT,
                                user_session UUID
                            )"""
        cursor.execute(create_table_query)

        sql_query = """
                        INSERT INTO temp_table (event_time, event_type, product_id, price, user_id, user_session)
                        SELECT DISTINCT ON (event_type, product_id, price, user_id, user_session, DATE_TRUNC('second', event_time)) 
                            event_time, event_type, product_id, price, user_id, user_session
                        FROM (
                            SELECT customers.*,
                            LAG(event_time) OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_time) as prev_time
                            FROM customers 
                        ) as subq
                        WHERE 
                            prev_time IS NULL OR 
                            event_time - prev_time > INTERVAL '1 second'
                        ORDER BY event_type, product_id, price, user_id, user_session, DATE_TRUNC('second', event_time), event_time;
                    """
        cursor.execute(sql_query)

        sql_query = "DROP TABLE IF EXISTS customers;"
        cursor.execute(sql_query)

        sql_query = "ALTER TABLE temp_table RENAME TO customers;"
        cursor.execute(sql_query)

        connection.commit()
        print("Duplicates deleted successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def main():
    load_dotenv(os.path.abspath("../.env"))
    delete_duplicates()


if __name__ == "__main__":
    main()