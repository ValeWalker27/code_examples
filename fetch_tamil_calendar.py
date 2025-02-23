import requests 
import pandas as pd
import polars as pl

from io import StringIO
from bs4 import BeautifulSoup


def fetch_tamil_calendar(input_month: str, input_year: int):

    url = f"https://www.prokerala.com/general/calendar/tamilcalendar.php?year={input_year}&mon={input_month.lower()}&sb=1"

    response = requests.get(url, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"})
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for data in soup.find('table', {'id': 'calendar-table'}).find_all('td', {'role': 'button'}):
        main_date = f"{data.find('a').text} {input_month[:3]}, {input_year}"
        main_day = f"{data.find('div').get('data-week_en')} ({data.find('div').get('data-week_ta')})"
        tamil_date = data.find('span', {'class': 'sub-day'}).text
        nakshatra = " ".join(data.find('span', {'class': 'day_nakshatra'}).text.split('\n')[1].split())
        thithi = " ".join(data.find('span', {'class': 'day_tithi'}).text.split('\n')[1].split())
        bank_holiday = '-'
        if len(data.find_all('span', {'class': 'bank-holiday'})) > 0:
            bank_holiday = data.find('span', {'class': 'bank-holiday'}).text
        tamil_festival = '-'
        if len(data.find_all('span', {'class': 'tamil-festival'})) > 0:
            tamil_festival = data.find('span', {'class': 'tamil-festival'}).text.split('\n')[1].strip()

        results.append({
            'Date': main_date
            ,'Tamil Date': tamil_date
            , 'Day': main_day
            , 'Nakshatra': nakshatra
            , 'Thithi': thithi
            , 'Tami lFestival': tamil_festival
            , 'Bank Holiday': bank_holiday
        })

    pl.from_dicts(results).write_excel(f"Tamil Calendar {input_month} {input_year}.xlsx")


if __name__== "__main__":
    fetch_tamil_calendar("March", 2025)
