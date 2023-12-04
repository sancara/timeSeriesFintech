import pandas as pd
import psycopg2
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

db_params = {
    'host': get_secret_value('HOST'),
    'database': get_secret_value('POSTGRES_DB'),
    'user': get_secret_value('POSTGRES_USER'),
    'password': get_secret_value('POSTGRES_PASSWORD'),
    'port': get_secret_value('POSTGRES_PORT')
}

table_name = get_secret_value('TABLE_NAME')

@transformer
def transform_in_postgres(*args, **kwargs) -> pd.DataFrame:
    """
    Performs a transformation in Postgres
    """
    try:
        connection = psycopg2.connect(**db_params)
        print("Connected to the database!")
        # Create a cursor to execute SQL queries
        analytic_query ='''
        SELECT
            symbol,
            TO_CHAR(stock_datetime, 'dd/mm/yyyy') as date,
            AVG(trading_volume) OVER (PARTITION BY symbol ORDER BY stock_datetime RANGE BETWEEN '3 months' PRECEDING AND CURRENT ROW) AS avg_volume_last_quarter
        FROM
            {table_name}
        WHERE
            stock_datetime >= NOW() - INTERVAL '3 months'
        ORDER BY
            symbol, stock_datetime;
        '''.format(table_name=table_name)

        result = pd.read_sql_query(analytic_query, connection)

    except Exception as e:
        print(f"Error: Unable to connect to the database - {e}")

    finally:
        # Close the connection in the finally block to ensure it's always closed
        if connection:
            connection.close()
            print("Connection closed.")
        
        return result


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
