import requests
from bs4 import BeautifulSoup


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

url = 'https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/'
html_content = requests.get(url).text

def get_top10_usa_companies_by_market_cap_gain():
    soup = BeautifulSoup(html_content, 'html.parser')
    symbols_list = [e.text for e in soup.select('div.company-code')]

    return symbols_list[:10]

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    data = {}
    symbols_lst = get_top10_usa_companies_by_market_cap_gain()
    for symbol in symbols_lst:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={{mage_secret_var("API_KEY")}}'
        url_demo = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo"
        response = requests.get(url)
        data[symbol] = response.json()

    return data
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
