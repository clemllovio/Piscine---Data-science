import psycopg2
import glob
import os
from dotenv import load_dotenv

load_dotenv(os.path.abspath("./.env"))

def main():
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

        create_table_query = f"""
                        CREATE TABLE IF NOT EXISTS "temptable"(
                            event_time TIMESTAMP WITH TIME ZONE,
                            event_type VARCHAR(255),
                            product_id BIGINT,
                            price FLOAT,
                            user_id INT,
                            user_session UUID,
                            duplicate_count INT
                        )"""
        cursor.execute(create_table_query)

        sql_query = """
                    SELECT event_time, event_type, product_id, price, user_id, user_session
                    FROM (
                    SELECT *, ROW_NUMBER() OVER (PARTITION BY event_type, product_id, user_id, user_session ORDER BY event_time) AS duplicate_count
                    FROM customers
) cte
WHERE duplicate_count = 1;

                """

        cursor.execute(sql_query)
        connection.commit()
        print("Duplicates deleted successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    main()

# WITH cte AS (
        #     SELECT ctid, ROW_NUMBER() OVER (
        #         PARTITION BY event_type, product_id, price, user_id, user_session
        #         ORDER BY event_time
        #     ) AS row_num
        #     FROM customers
        # )
        # DELETE FROM customers
        # WHERE ctid IN (
        #     SELECT ctid FROM cte WHERE row_num > 1
        # );