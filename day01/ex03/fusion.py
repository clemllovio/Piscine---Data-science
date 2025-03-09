import psycopg2
import os
from dotenv import load_dotenv

def fusion_tables():
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


        sql_query = """
                    ALTER TABLE customers
                    ADD COLUMN IF NOT EXISTS category_id BIGINT NULL,
                    ADD COLUMN IF NOT EXISTS category_code VARCHAR(255) NULL,
                    ADD COLUMN IF NOT EXISTS brand VARCHAR(255) NULL
                    """
        cursor.execute(sql_query)

        sql_query = """
            UPDATE customers
            SET
                category_id = item.category_id
            FROM item
            WHERE customers.product_id = item.product_id
            """
        cursor.execute(sql_query)

        sql_query = """
            UPDATE customers
            SET
                category_code = item.category_code
            FROM item
            WHERE customers.product_id = item.product_id
             """
        cursor.execute(sql_query)

        sql_query = """
                            UPDATE customers
                            SET
                                brand = item.brand
                            FROM item
                            WHERE customers.product_id = item.product_id;
                            """
        cursor.execute(sql_query)
        connection.commit()
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.rollback()
    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def main():
    load_dotenv(os.path.abspath("./.env"))
    fusion_tables()


if __name__ == "__main__":
    main()