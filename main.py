import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, timedelta


def get_ranking_dates(start_date, end_date):
    """
    Gives a list of all the dates of all the tuesdays between start_date and end_date
    """
    with open('rankings_dates.json', 'r') as f:
        dates = json.load(f)

    # Convert start and end dates to datetime objects
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    # Filter dates
    filtered_dates = []
    for d in dates:
        date_value = datetime.strptime(d["value"], "%Y-%m-%d")
        if start_dt <= date_value <= end_dt:
            filtered_dates.append(d["value"])

    return filtered_dates
    

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


def get_rakings_on_date(event, sex, date):
    """
    Save to a f"data/{sex}_{event}_{date}.csv" file the world rankings for a specific event, sex on a specific date
    """

    ## Find number of pages
    url = f"https://worldathletics.org/world-rankings/{event}/{sex}?regionType=world&page=1&rankDate={date}&limitByCountry=0"
    print(url)
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    pages = soup.find_all('a', class_="btn--number btn--pagination pag--end pag--show")

    if len(pages) > 1:
        print(f"len(pages) = {len(pages):d}")
        exit()

    if len(pages) == 0:
        pages = soup.find_all('a', class_="btn--number btn--pagination")
        if len(pages) == 0:
            print("I attempted to find the higher pages number, but\n")
            print(f"len(pages) = {len(pages):d}")
            exit()
        else:
            max_page = int(pages[-1].get("data-page"))
    else:
        max_page = int(pages[0].get("data-page"))


    ## Get all the results for that event, sex, date
    df = pd.DataFrame()
    for page in range(1, max_page + 1):

        df_page = get_data_100(event, sex, page, date)
        df = pd.concat([df, df_page])

    df = df.reset_index(drop=True)

    filename = f"data/{sex}_{event}/{sex}_{event}_{date}.csv"
    df.to_csv(filename, index=False)


event = "110mh"
sex = "men"

# Example start and end dates
start_date = "2019-01-01"
end_date = "2019-07-02"
dates = get_ranking_dates(start_date, end_date)

for date in dates:
    print(date)
    get_rakings_on_date(event, sex, date)
