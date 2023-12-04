import pandas as pd


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
    df = pd.DataFrame(data[0]['Monthly Time Series'])
    
    df = df.T
    df.reset_index(inplace=True)
    df.columns = ['stock_datetime','price_open', 'price_high', 'price_low', 'price_close', 'trading_volume']
    df['symbol'] = data[1]
    pd.to_datetime(df['stock_datetime'], format='%Y-%m-%d')

    print(df.info())

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
