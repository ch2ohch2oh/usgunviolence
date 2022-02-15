#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pdb
import pandas as pd
import time
import csv

def download_raw_data(page=0):
    """Download data."""
    link = f"https://www.gunviolencearchive.org/last-72-hours?page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }

    data = requests.get(link, headers=headers)
    if data.status_code != 200:
        return None
    return data.text


def extract_table_data(html):
    '''Extract data table from html text.'''
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    table_data = []
    for row in table.find_all("tr"):
        items = row.find_all("td")
        # Skip header row
        if not items:
            continue
        row_data = [item.text.strip() for item in items]
        row_data[-1] = items[-1].find_all("a")[-1]['href']
        table_data.append(row_data)
    return table_data

def download_last72hours():
    '''Download all data within the last 72 hours.'''
    data = []
    for pageid in range(50):
        raw_html = download_raw_data(pageid)
        table = extract_table_data(raw_html)
        data.extend(table)
        if len(table) < 25:
            break
    return data

if __name__ == '__main__':
    data = download_last72hours()
    date = time.strftime('%Y-%m-%d')
    outfile = f'data/data-{date}.csv'
    with open(outfile, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
        print(f'{len(data)} rows written to {outfile}')
    