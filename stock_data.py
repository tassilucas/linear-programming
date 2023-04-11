import yfinance as yf
import pandas as pd
import statistics

tickers = [
  'ABEV3', 'ALPA4', 'AMER3', 'ASAI3', 'AZUL4',
  'B3SA3', 'BEEF3', 'BBAS3', 'BIDI11', 'BPAN4', 'BBSE3', 'BRML3',
  'BBDC3', 'BBDC3', 'BRAP4', 'BRKM5', 'BPAC11',
  'CASH3', 'CRFB3', 'CCRO3', 'CMIG4', 'CIEL3',
  'COGN3', 'CPLE6', 'CSAN3', 'CPFE3', 'CSNA3',
  'CMIN3', 'CVCB3', 'CYRE3',
  'DXCO3',
  'ECOR3', 'ELET3', 'ELET6', 'EMBR3', 'ENBR3', 'ENGI11',
  'ENEV3', 'EGIE3', 'EQTL3', 'EZTC3',
  'FLRY3',
  'GGBR4', 'GOAU4', 'GOLL4', 'GNDI3',
  'HAPV3', 'HYPE3',
  'IGTI11', 'IRBR3',
  'ITUB4', 'ITSA4',
  'JBSS3', 'JHSF3',
  'KLBN11',
  'LCAM3', 'LWSA3', 'LAME4', 'LREN3',
  'MGLU3', 'MRFG3', 'MRVE3', 'MULT3',
  'NTCO3',
  'PCAR3', 'PETR3', 'PETR4', 'PRIO3', 'PETZ3', 'POSI3',
  'QUAL3',
  'RADL3', 'RDOR3', 'RAIL3', 'RENT3', 'RRRP3',
  'SBSP3', 'SOMA3', 'SANB11', 'SULA11', 'SUZB3',
  'TAEE11', 'TIMS3', 'TOTS3', 
  'UGPA3', 'USIM5',
  'VALE3', 'VIIA3', 'VBBR3', 'VIVT3',
  'WEGE3', 'YDUQ3'
]

# returns a dataframe in format
# ticker | variancia | rentabilidade mensal | year
def create_stock_data():
    data = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker + '.SA')
            hist = stock.history(period="max")

            variance = statistics.variance(hist.Close.dropna())
            mean = hist.Close.pct_change().mean()
            year = hist.index[0].year
            data.append([ticker, variance, mean, year])
        except:
            pass

    df = pd.DataFrame(data, columns=['ticker', 'variancia', 'rentabilidade', 'year']).round(7)
    df.to_csv('data/stock_data.csv')

def read_stock_data():
    return pd.read_csv('data/stock_data.csv')

if __name__ == "__main__":
    create_stock_data()
