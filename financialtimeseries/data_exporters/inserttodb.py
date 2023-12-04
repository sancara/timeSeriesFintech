import pandas as pd
import psycopg2
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

db_params = {
    'host': get_secret_value('HOST'),
    'database': get_secret_value('POSTGRES_DB'),
    'user': get_secret_value('POSTGRES_USER'),
    'password': get_secret_value('POSTGRES_PASSWORD'),
    'port': get_secret_value('POSTGRES_PORT')
}

@data_exporter
def export_data_to_postgres(df: pd.DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql

    """
    # Create a connection
    try:
        connection = psycopg2.connect(**db_params)
        print("Connected to the database!")
        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Define the table schema
        table_name = get_secret_value('TABLE_NAME')
       

        schema_definition = """
            CREATE TABLE IF NOT EXISTS {table_name} (
                stock_datetime TIMESTAMP,
                open_price FLOAT,
                highest_price FLOAT,
                lowest_price FLOAT,
                close_price FLOAT,
                trading_volume BIGINT,
                symbol VARCHAR(8)
                -- Add more columns as needed
            );
        """.format(table_name=table_name)

        df_columns = df.columns.tolist()

        # Execute the schema definition query
        cursor.execute(schema_definition)
        connection.commit()

        for index, row in df.iterrows():
            insert_query = f"INSERT INTO {table_name} ({', '.join(df_columns)}) VALUES {tuple(row.values)}"
            cursor.execute(insert_query)


        connection.commit()
        print(f"Records inserted into {table_name}")

    except Exception as e:
        print(f"Error: Unable to connect to the database - {e}")

    finally:
        # Close the connection in the finally block to ensure it's always closed
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")
        
