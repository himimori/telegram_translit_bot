import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
import streamlit as st
import datetime

# Отключаем предупреждение о потокобезопасности Matplotlib
st.set_option('deprecation.showPyplotGlobalUse', False)

ticker_dict = {
    "Microsoft Corporation": "MSFT",
    "Apple Inc": "AAPL",
    "NVIDIA Corporation": "NVDA",
    "Alphabet Inc.": "GOOGL",
    "Amazon.com, Inc.": "AMZN",
    "Meta Platforms, Inc.": "META",
    "Berkshire Hathaway Inc.": "BRK-B",
    "Eli Lilly and Company": "LLY",
    "Taiwan Semiconductor Manufacturing Company Limited": "TSM",
    "Broadcom Inc.": "AVGO",
    "JPMorgan Chase & Co.": "JPM",
    "Novo Nordisk A/S": "NVO",
    "Visa Inc.": "V",
    "Tesla, Inc.": "TSLA",
    "Walmart Inc.": "WMT",
    "Exxon Mobil Corporation": "XOM",
    "UnitedHealth Group Incorporated": "UNH",
    "Mastercard Incorporated": "MA",
    "ASML Holding N.V.": "ASML",
    "Johnson & Johnson": "JNJ",
    "The Procter & Gamble Company": "PG",
    "The Home Depot, Inc.": "HD",
    "Oracle Corporation": "ORCL",
    "Merck & Co., Inc.": "MRK",
    "Toyota Motor Corporation": "TM",
    "Costco Wholesale Corporation": "COST",
    "AbbVie Inc.": "ABBV",
    "Advanced Micro Devices, Inc.": "AMD",
    "Chevron Corporation": "CVX",
    "Bank of America Corporation": "BAC",
    "Salesforce, Inc.": "CRM",
    "Netflix, Inc.": "NFLX",
    "The Coca-Cola Company": "KO",
    "PepsiCo, Inc.": "PEP",
    "SAP SE": "SAP",
    "Accenture plc": "ACN",
    "Adobe Inc.": "ADBE",
    "Linde plc": "LIN",
    "The Walt Disney Company": "DIS",
    "Thermo Fisher Scientific Inc.": "TMO",
    "Shell plc": "SHEL",
    "AstraZeneca PLC": "AZN",
    "Wells Fargo & Company": "WFC",
    "Cisco Systems, Inc.": "CSCO",
    "McDonald's Corporation": "MCD"
}

st.header('Streamlit test')


# Виджет для выбора компании
name = st.selectbox('Выберите компанию', ticker_dict.keys())

info = yf.Ticker(ticker_dict[name])

# Сохраняем инфу о компании
ceo_index = next((index for index, officer in enumerate(info.info['companyOfficers']) if 'CEO' in officer['title']), None)
company_info = {'Отрасль': info.info['industry'],
                'Сектор': info.info['sector'],
                'Местоположение штаб-квартиры': info.info['city'],
                'Должность и имя руководителя': f"{info.info['companyOfficers'][ceo_index]['title']} - {info.info['companyOfficers'][ceo_index]['name']}", 
                'Веб-сайт': info.info['website'],
                'Количество сотрудников': f"{int(info.info['fullTimeEmployees'] / 1000)} тыс."
                }

company_finances = {'Рыночная капитализация': f"{round(info.info['marketCap'] / 1000000000, 1)} млрд $",
                'Выручка': f"{round(info.info['totalRevenue'] / 1000000000, 1)} млрд $",
                'Долг': f"{round(info.info['totalDebt'] / 1000000000, 1)} млрд $"
                }


# Виджеты для выбора дат
start_date = st.date_input("Выберите начальную дату", 
                           value = datetime.date(2024, 1, 1), 
                           min_value = datetime.date(1900, 1, 1))
end_date = st.date_input("Выберите конечную дату",
                         value = datetime.date(2024, 4, 1), 
                         min_value = datetime.date(1900, 1, 2))

df = info.history(start=start_date, end=end_date)
prices = df.loc[:, 'Open':'Close']


fig, ax = mpf.plot(prices, type='candle', style='charles', title=f'Стоимость акций {name}', ylabel='', returnfig=True)

# Отображаем график на Streamlit
st.pyplot(fig)

st.subheader(f'Сводка по компании {name}')

df = pd.DataFrame.from_dict(company_info, orient='index', columns=[""])

# Отображаем таблицу
st.table(df)

# Отображение "метрик" стримлит
col1, col2, col3 = st.columns(3)

col1.metric("**Капитализация**", company_finances['Рыночная капитализация'])
col2.metric("**Выручка**", company_finances['Выручка'])
col3.metric("**Долг**", company_finances['Долг'])
