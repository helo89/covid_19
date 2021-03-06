#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import scrape_common as sc

d = sc.download('https://www.fr.ch/covid19/sante/covid-19/coronavirus-statistiques-evolution-de-la-situation-dans-le-canton', silent=True)

soup = BeautifulSoup(d, 'html.parser')
xls_url = soup.find(href=re.compile("\.xlsx$")).get('href')
assert xls_url, "URL is empty"
if not xls_url.startswith('http'):
    xls_url = f'https://www.fr.ch{xls_url}'

xls = sc.xlsdownload(xls_url, silent=True)
rows = sc.parse_xls(xls, header_row=0, sheet_name='Données sites internet')
for i, row in enumerate(rows):
    print('FR')
    sc.timestamp()
    print('Downloading:', xls_url)
    print('Date and time:', row['Date'].date().isoformat())
    print('Confirmed cases:', row['Total cas avérés'])
    print('Hospitalized:', row['Personnes hospitalisées'])
    print('ICU:', row['dont soins intensifs'])
    print('Deaths:', row['Total décès'])
    print('Recovered:', row['Total Sortis de l\'hôpital'])
    # do not print record delimiter for last record
    # this is an indicator for the next script to check
    # for expected values.
    if len(rows) - 1 > i:
        print('-' * 10)
