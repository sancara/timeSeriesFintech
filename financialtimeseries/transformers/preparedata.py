import pandas as pd
import json

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    
    # Extract symbols and data
    result = {}
    for symbol, symbol_data in data.items():
        if "Meta Data" in symbol_data and "Monthly Time Series" in symbol_data:
            meta_data = symbol_data["Meta Data"]
            time_series = symbol_data["Monthly Time Series"]

            formatted_data = {date: {
                "open": value["1. open"],
                "high": value["2. high"],
                "low": value["3. low"],
                "close": value["4. close"],
                "volume": value["5. volume"]
            } for date, value in time_series.items()}

            result[symbol] = formatted_data

    rows = []

    # Iterate over symbols and dates
    for symbol, symbol_data in result.items():
        for date, values in symbol_data.items():
            row = {
                'stock_datetime': date,
                'open_price': float(values['open']),
                'highest_price': float(values['high']),
                'lowest_price': float(values['low']),
                'close_price': float(values['close']),
                'trading_volume': int(values['volume']),
                'symbol': symbol
            }
            rows.append(row)

    # Create a Pandas DataFrame
    df = pd.DataFrame(rows)
    pd.to_datetime(df['stock_datetime'], format='%Y-%m-%d')

    # Print the DataFrame
    return df
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
