from unittest.mock import MagicMock, patch
import pandas as pd

#create mock data for call_api function
def call_api(symbol ,function) -> pd.DataFrame:
    mock_response = MagicMock()
    mock_response.status_code = 200
    if(symbol == 'AMZN' and function == 'OVERVIEW'):
        mock_response.json.return_value = {
        "Symbol": "AMZN",
        "AssetType": "Common Stock",
        "Name": "Amazon.com Inc",
        "Description": "Amazon.com, Inc. is an American multinational technology company which focuses on e-commerce, cloud computing, digital streaming, and artificial intelligence. It is one of the Big Five companies in the U.S. information technology industry, along with Google, Apple, Microsoft, and Facebook. The company has been referred to as one of the most influential economic and cultural forces in the world, as well as the world's most valuable brand.",
        "CIK": "1018724",
        "Exchange": "NASDAQ",
        "Currency": "USD",
        "Country": "USA",
        "Sector": "TRADE & SERVICES",
        "Industry": "RETAIL-CATALOG & MAIL-ORDER HOUSES",
        "Address": "410 TERRY AVENUE NORTH, SEATTLE, WA, US",
        "FiscalYearEnd": "December",
        "LatestQuarter": "2022-06-30",
        "MarketCapitalization": "1089054441000",
        "EBITDA": "52620001000",
        "PERatio": "101.81",
        "PEGRatio": "4.257",
        "BookValue": "12.9",
        "DividendPerShare": "0",
        "DividendYield": "0",
        "EPS": "1.05",
        "RevenuePerShareTTM": "47.82",
        "ProfitMargin": "0.0239",
        "OperatingMarginTTM": "0.0315",
        "ReturnOnAssetsTTM": "0.0245",
        "ReturnOnEquityTTM": "0.0943",
        "RevenueTTM": "485901992000",
        "GrossProfitTTM": "197478000000",
        "DilutedEPSTTM": "1.05",
        "QuarterlyEarningsGrowthYOY": "0.975",
        "QuarterlyRevenueGrowthYOY": "0.072",
        "AnalystTargetPrice": "170.32",
        "TrailingPE": "101.81",
        "ForwardPE": "44.44",
        "PriceToSalesRatioTTM": "2.241",
        "PriceToBookRatio": "8.29",
        "EVToRevenue": "2.373",
        "EVToEBITDA": "22.75",
        "Beta": "1.322",
        "52WeekHigh": "188.11",
        "52WeekLow": "101.26",
        "50DayMovingAverage": "126.96",
        "200DayMovingAverage": "134.57",
        "SharesOutstanding": "10187600000",
        "DividendDate": "None",
        "ExDividendDate": "None"
        }
    elif(symbol == 'GOOGL' and function == 'TIME_SERIES_INTRADAY'):
        mock_response.json.return_value = {
            "Meta Data": {
                "1. Information": "Intraday (15min) open, high, low, close prices and volume",
                "2. Symbol": "GOOGL",
                "3. Last Refreshed": "2022-10-18 20:00:00",
                "4. Interval": "15min",
                "5. Output Size": "Compact",
                "6. Time Zone": "US/Eastern"
            },
            "Time Series (15min)": {
                "2022-10-18 20:00:00": {
                    "1. open": "102.3900",
                    "2. high": "102.6700",
                    "3. low": "102.2900",
                    "4. close": "102.4400",
                    "5. volume": "7123"
                },
                "2022-10-18 19:45:00": {
                    "1. open": "102.7900",
                    "2. high": "102.7900",
                    "3. low": "102.3500",
                    "4. close": "102.4000",
                    "5. volume": "5464"
                },
                "2022-10-18 19:30:00": {
                    "1. open": "102.8400",
                    "2. high": "102.9700",
                    "3. low": "102.7100",
                    "4. close": "102.8100",
                    "5. volume": "4638"
                }
            }
        }
    #return json content as dataframe
    return mock_response.json()


if __name__ == '__main__':
    #create mock data for call_api function
    data = call_api('AMZN','OVERVIEW')