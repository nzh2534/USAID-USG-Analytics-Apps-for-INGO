import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime

import pandas as pd
import numpy as np

import plotly
import plotly.express as px
import plotly.io as pio

import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

# Please note that this function is included in the demo.py program for the USG Overview; SEE Chart 8

date_after_var = input("Date to show the USAID Business Forecast After (MM/DD/YYYY): ")
username = input("Chart Studio Username?: ")
api_key = input("Chart Studio Password?: ")
creds_json = input("Google API Service Account JSON (use .json)?: ")
sheet_name = input("Google Sheet Name?: ")

def usaid_bf_wash_fxn(date_after_var,username,api_key,creds_json,sheet_name):

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    #Access Google Sheets
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json,scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    lyst1 = sheet.get_all_records()

    df = pd.DataFrame(lyst1)

    def split(value):
        a, b= value.split('-')
        return a

    lyst2 =[]
    for i in df["Total Estimated Cost/Amount Range"]:
        lyst2.append(split(i))

    df["Estimated Cost Minimum"] = lyst2

    df['Anticipated Solicitation Release Date']= pd.to_datetime(df['Anticipated Solicitation Release Date'])

    date1 = date_after_var

    df = df.loc[df["Anticipated Solicitation Release Date"] > datetime.strptime(date1, "%m/%d/%Y")]
    df = df.loc[df["Location"] == "Washington"]

    df["Award Description"] = df["Award Description"].str.wrap(45)
    df["Award Description"] = df["Award Description"].apply(lambda x: x.replace('\n', '<br>'))

    scatterplot = px.scatter(
        title = "USAID Business Forecast (For Washington Operating Unit)",
        data_frame=df,
        x = "Anticipated Solicitation Release Date",
        y = "Estimated Cost Minimum",
        color = "Sector",
        hover_name = "Award Title",
        hover_data=["Operating Unit","Total Estimated Cost/Amount Range","Anticipated Award Date","Award Length","Award Description"],
        opacity = 0.9,
        orientation="v",
        template='gridon',
        labels={
            "Anticipated Solicitation Release Date": "<b>Anticipated Solicitation Release Date</b>",
            "Total Estimated Cost/Amount Range":"<b>Estimated Cost Range</b>",
            "Award Description":"<br><b>Award Description</b>",
            "Sector":"<b>Sector</b>",
            "Estimated Cost Minimum":"<b>Estimated Cost Minimum</b>",
            "Anticipated Award Date":"<b>Anticipated Award Date</b>",
            "Award Length":"<b>Award Length</b>",
            "Operating Unit":"<b>Operating Unit</b>"
        }
    )

    scatterplot.update_traces(marker={'size': 15})

    # py.plot(scatterplot, filename = 'USAID BF for Washington', auto_open = False)

    scatterplot.show()

usaid_bf_wash_fxn(date_after_var,username,api_key,creds_json,sheet_name)