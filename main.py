import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def get_data_100(event, sex, page, date) -> pd.DataFrame:
    """
    Download the table of 100 results in the world rankings for a specific event, sex, page, date
    """
    url = f"https://worldathletics.org/world-rankings/{event}/{sex}?regionType=world&page={page:d}&rankDate={date}&limitByCountry=0"
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all tables with class 'records-table'
    table = soup.find_all('table', class_='records-table')
    
    if len(table) > 1:
        print(f"len(table) = {len(table):d}")
        exit()
    
    df = pd.read_html(StringIO(str(table)))

    if len(df) > 1:
        print(f"len(df_page) = {len(df):d}")
        exit()

    return df[0]


event = "long-jump"
sex = "women"
date = "2025-07-01"


## Find number of pages
url = f"https://worldathletics.org/world-rankings/{event}/{sex}?regionType=world&page=1&rankDate={date}&limitByCountry=0"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.content, 'html.parser')

pages = soup.find_all('a', class_="btn--number btn--pagination pag--end pag--show")
if len(pages) > 1:
    print(f"len(pages) = {len(pages):d}")
    exit()

max_page = int(pages[0].get("data-page"))


## Get all the results for that event, sex, date
df = pd.DataFrame()
for page in range(1, max_page + 1):

    df_page = get_data_100(event, sex, page, date)
    df = pd.concat([df, df_page])

df = df.reset_index(drop=True)

filename = f"data/{sex}_{event}_{date}.csv"
df.to_csv(filename, index=False)
