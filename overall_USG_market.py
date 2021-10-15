import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime

from copy import Error
import pandas as pd
import requests
import numpy as np

import plotly
import plotly.express as px
import plotly.io as pio

import chart_studio

username = input("Chart Studio Username?: ")
api_key = input("Chart Studio Password?: ")
creds_json = input("Google API Service Account JSON (use .json)?: ")
sheet_name = input("Google Sheet Name?: ")

chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

import chart_studio.plotly as py
import chart_studio.tools as tls

url = "https://api.usaspending.gov"

#User Input
year_var = input("\nYear?: ")
year_start = input("\nInput exact FY start date; Use YYYY-MM-DD format exactly: ")
year_end = input("Input exact FY end date; Use YYYY-MM-DD format exactly: ")
agency_name = input("\nInput Agency Name (Options: USAID or USDS or USDA): ")
recipient_name = input("\nInput Competitor Recipient Name (Options: CRS, SAVE, MCORPS, or WVISION): ")
date_after_var = input("\nInput a date to show the USAID Business Forecast After; Use MM/DD/YYYY format exactly: ")

agency_filter = ""
end_loop_agency = 0
while end_loop_agency != 1:
    if agency_name == "USAID":
        agency_filter = "Agency for International Development"
        end_loop_agency = 1
    elif agency_name == "USDS":
        agency_filter = "Department of State"
        end_loop_agency = 1
    elif agency_name =="USDA":
        agency_filter = "Department of Agriculture"
        end_loop_agency = 1
    else:
        print("Incorrect Agency Name Option; Please input one of available")
        agency_name = input("Available Options: USAID, USDS, or USDA: ")


# ------------------------------------------------- START OF CHART 1 -------------------------------------------------------------

#USAID Spending By Country _reg ---Chart #1
endpoint_reg = "/api/v2/search/spending_by_category/country"
payload_reg = {
      "filters": {
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ],
          "agencies": [
              {
                  "type": "awarding",
                  "tier": "toptier",
                  "name": agency_filter,
              }
          ]
      },
      "category": "country",
      "limit": 29,
      "page": 1
  }
response_reg = requests.post(f"{url}{endpoint_reg}", json=payload_reg)
data_reg = response_reg.json()
df_reg = pd.DataFrame(data_reg["results"])
nonapp_countries = ['UNITED STATES','SWITZERLAND','JAPAN','AFGHANISTAN','GERMANY','UNITED KINGDOM','CANADA','KOREA, SOUTH','KUWAIT','ITALY','SAUDI ARABIA','QATAR','FRANCE','UNITED ARAB EMIRATES','BAHRAIN','ISRAEL']

for i in nonapp_countries:
    df_reg = df_reg.drop(index=df_reg[df_reg['name'] == i].index)

# df_reg.to_csv(r'C:\Users\nhagl\Desktop\work\demo\alldata.txt', header=None, index=None, sep=' ', mode='a') # --- For reference regarding country codes

barchart_reg = px.bar(
    title = agency_name + " Funding by Top 25 Countries (Doesn't Include Developed) for FY" + str(year_var),
    data_frame=df_reg,
    x = "name",
    y = "amount",
    opacity = 0.9,
    orientation="v",
    barmode='relative',
    template='gridon',
    labels={
        "name": "",
        "amount": "Amount",
        "org": 'Organization'
    }
)

# ------------------------------------------------- START OF CHART 2 -------------------------------------------------------------

#FH Funding By Country _regfh ---Chart #2
endpoint_regfh = "/api/v2/search/spending_by_category/country"
payload_regfh = {
      "filters": {
          "recipient_id": "78911b63-cf98-0b58-4cab-6cabc3be1464-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "country",
      "limit": 10,
      "page": 1
  }
response_regfh = requests.post(f"{url}{endpoint_regfh}", json=payload_regfh)
data_regfh = response_regfh.json()
df_regfh = pd.DataFrame(data_regfh["results"])

#CRS Funding By Country _regcrs ---Chart #2
endpoint_regcrs = "/api/v2/search/spending_by_category/country"
payload_regcrs = {
      "filters": {
          "recipient_id": "d0340209-86e2-4d29-1f1c-4a1f17416684-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "country",
      "limit": 10,
      "page": 1
  }
response_regcrs = requests.post(f"{url}{endpoint_regcrs}", json=payload_regcrs)
data_regcrs = response_regcrs.json()
df_regcrs = pd.DataFrame(data_regcrs["results"])

#Save the Children Funding By Country _regsav ---Chart #2 DUNS: 072129919
endpoint_regsav = "/api/v2/search/spending_by_category/country"
payload_regsav = {
      "filters": {
          "recipient_id": "d43777ac-95bd-5506-495d-3aee0d9488d2-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "country",
      "limit": 11,
      "page": 1
  }
response_regsav = requests.post(f"{url}{endpoint_regsav}", json=payload_regsav)
data_regsav = response_regsav.json()
df_regsav = pd.DataFrame(data_regsav["results"])

#Mercy Corps Funding By Country _regmc ---Chart #2 DUNS: 134170547
endpoint_regmc = "/api/v2/search/spending_by_category/country"
payload_regmc = {
      "filters": {
          "recipient_id": "764db89c-fbc0-d406-6f9b-16705e3fb7bc-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "country",
      "limit": 10,
      "page": 1
  }
response_regmc = requests.post(f"{url}{endpoint_regmc}", json=payload_regmc)
data_regmc = response_regmc.json()
df_regmc = pd.DataFrame(data_regmc["results"])

#World Vision Funding By Country _regwv ---Chart #2 DUNS: 071903322
endpoint_regwv = "/api/v2/search/spending_by_category/country"
payload_regwv = {
      "filters": {
          "recipient_id": "99a98475-96db-966e-ea6c-656c24aff22c-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "country",
      "limit": 11,
      "page": 1
  }
response_regwv = requests.post(f"{url}{endpoint_regwv}", json=payload_regwv)
data_regwv = response_regwv.json()
df_regwv = pd.DataFrame(data_regwv["results"])

df_regfh['org'] = "Food for the Hungry"
df_regcrs['org'] = "Catholic Relief Services"
df_regsav['org'] = "Save the Children"
df_regmc['org'] = "Mercy Corps"
df_regwv['org'] = "World Vision"

df_regfh = df_regfh.append(df_regcrs, ignore_index=True)
df_regfh = df_regfh.append(df_regsav, ignore_index=True)
df_regfh = df_regfh.append(df_regmc, ignore_index=True)
df_regfh = df_regfh.append(df_regwv, ignore_index=True)

for i in nonapp_countries:
    df_regfh = df_regfh.drop(index=df_regfh[df_regfh['name'] == i].index)

df_regfh = df_regfh.sort_values('amount', ascending=False)

barchart_regfh = px.bar(
    title = "Top 10 Funded Countries Per Recipient (Doesn't Include Developed) for FY" + str(year_var),
    data_frame=df_regfh,
    x = "name",
    y = "amount",
    color = "org",
    opacity = 0.9,
    orientation="v",
    barmode='relative',
    template='gridon',
    labels={
        "name": "",
        "amount": "Amount",
        "org": 'Organization'
    }
)

# ------------------------------------------------- START OF CHART 3 -------------------------------------------------------------


#FH Funding By CFDA Categories _cfdafh ---Chart #3
endpoint_cfdafh = "/api/v2/search/spending_by_category/cfda"
payload_cfdafh = {
      "filters": {
          "recipient_id": "78911b63-cf98-0b58-4cab-6cabc3be1464-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "cfda",
      "limit": 10,
      "page": 1
  }
response_cfdafh = requests.post(f"{url}{endpoint_cfdafh}", json=payload_cfdafh)
data_cfdafh = response_cfdafh.json()
df_cfdafh = pd.DataFrame(data_cfdafh["results"])

#CRS Funding By CFDA Categories _cfdacrs ---Chart #3
endpoint_cfdacrs = "/api/v2/search/spending_by_category/cfda"
payload_cfdacrs = {
      "filters": {
          "recipient_id": "d0340209-86e2-4d29-1f1c-4a1f17416684-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "cfda",
      "limit": 10,
      "page": 1
  }
response_cfdacrs = requests.post(f"{url}{endpoint_cfdacrs}", json=payload_cfdacrs)
data_cfdacrs = response_cfdacrs.json()
df_cfdacrs = pd.DataFrame(data_cfdacrs["results"])

#Save the Children Funding by CFDA Categories _cfdasav ---Chart #3 DUNS: 072129919
endpoint_cfdasav = "/api/v2/search/spending_by_category/cfda"
payload_cfdasav = {
      "filters": {
          "recipient_id": "d43777ac-95bd-5506-495d-3aee0d9488d2-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "cfda",
      "limit": 10,
      "page": 1
  }
response_cfdasav = requests.post(f"{url}{endpoint_cfdasav}", json=payload_cfdasav)
data_cfdasav = response_cfdasav.json()
df_cfdasav = pd.DataFrame(data_cfdasav["results"])

#Mercy Corps Funding By CFDA Categories _cfdamc ---Chart #3 DUNS: 134170547
endpoint_cfdamc = "/api/v2/search/spending_by_category/cfda"
payload_cfdamc = {
      "filters": {
          "recipient_id": "764db89c-fbc0-d406-6f9b-16705e3fb7bc-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "cfda",
      "limit": 10,
      "page": 1
  }
response_cfdamc = requests.post(f"{url}{endpoint_cfdamc}", json=payload_cfdamc)
data_cfdamc = response_cfdamc.json()
df_cfdamc = pd.DataFrame(data_cfdamc["results"])

#World Vision Funding By CFDA Categories _cfdawv ---Chart #3 DUNS: 071903322
endpoint_cfdawv = "/api/v2/search/spending_by_category/cfda"
payload_cfdawv = {
      "filters": {
          "recipient_id": "99a98475-96db-966e-ea6c-656c24aff22c-C",
          "time_period": [
              {
                  "start_date": year_start,
                  "end_date": year_end
              }
          ]
      },
      "category": "cfda",
      "limit": 10,
      "page": 1
  }
response_cfdawv = requests.post(f"{url}{endpoint_cfdawv}", json=payload_cfdawv)
data_cfdawv = response_cfdawv.json()
df_cfdawv = pd.DataFrame(data_cfdawv["results"])

df_cfdafh['org'] = "Food for the Hungry"
df_cfdacrs['org'] = "Catholic Relief Services"
df_cfdasav['org'] = "Save the Children"
df_cfdamc['org'] = "Mercy Corps"
df_cfdawv['org'] = "World Vision"

df_cfdafh = df_cfdafh.append(df_cfdacrs, ignore_index=True)
df_cfdafh = df_cfdafh.append(df_cfdasav, ignore_index=True)
df_cfdafh = df_cfdafh.append(df_cfdamc, ignore_index=True)
df_cfdafh = df_cfdafh.append(df_cfdawv, ignore_index=True)

nonapp_cfda = ['USAID Foreign Assistance for Programs Overseas']
for i in nonapp_cfda:
    df_cfdafh = df_cfdafh.drop(index=df_cfdafh[df_cfdafh['name'] == i].index)

df_cfdafh = df_cfdafh.sort_values('amount', ascending=False)

barchart_cfdafh = px.bar(
    title = "Top 10 Funded CFDA Categories Per Recipient for FY" + str(year_var),
    data_frame=df_cfdafh,
    x = "name",
    y = "amount",
    color = "org",
    opacity = 0.9,
    orientation="v",
    barmode='relative',
    template='gridon',
    labels={
        "name": "",
        "amount": "Amount",
        "org": 'Organization'
    }
)

# ------------------------------------------------- START OF CHART 4 -------------------------------------------------------------

#USAID Spending By Country (DFSA) _regcom ---Chart #4
def chart_4(year_start,year_end,agency_filter):
    app_countries = ['ETH','KEN','COD','SSD','UGA','MOZ','GTM','KHM','RWA','BOL','BDI','IDN','PER','PHL','BGD','HTI','NIC','DOM']

    endpoint_regcom = "/api/v2/search/spending_by_category/country"
    payload_regcom = {
        "filters": {
            "time_period": [
                {
                    "start_date": year_start,
                    "end_date": year_end
                }
            ],
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": agency_filter,
                }],
            "place_of_performance_locations": [
                {
                    "country": 'BGD'},
                {
                    "country": "BOL"},
                {
                    "country": "BDI"},
                {
                    "country": "KHM"},
                {
                    "country": "COD"},
                {
                    "country": "DOM"},
                {
                    "country": "ETH"},
                {
                    "country": "GTM"},
                {
                    "country": "HTI"},
                {
                    "country": "IDN"},
                {
                    "country": "KEN"},
                {
                    "country": "MOZ"},
                {
                    "country": "NIC"},
                {
                    "country": "PER"}, 
                {
                    "country": "PHL"},
                {
                    "country": "RWA"},
                {
                    "country": "SSD"},
                {
                    "country": "UGA"},
                ],
        },
        "category": "country",
        "limit": 20,
        "page": 1
    }
    response_regcom = requests.post(f"{url}{endpoint_regcom}", json=payload_regcom)
    data_regcom = response_regcom.json()
    df_regcom = pd.DataFrame(data_regcom["results"])

    for i in df_regcom['code']:
        if i not in app_countries: 
            df_regcom = df_regcom.drop(index=df_regcom[df_regcom['code'] == i].index)

    total_usaid = df_regcom['amount'].sum()
    total_usaid = "{:,}".format(total_usaid)

    #FH Spending By Country _regfhonly ---Chart #4
    endpoint_regfhonly = "/api/v2/search/spending_by_category/country"
    payload_regfhonly= {
        "filters": {
            "recipient_id": "78911b63-cf98-0b58-4cab-6cabc3be1464-C",
            "time_period": [
                {
                    "start_date": year_start,
                    "end_date": year_end
                }
            ],
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": agency_filter,
                }],
        },
        "category": "country",
        "limit": 16,
        "page": 1
    }

    response_regfhonly = requests.post(f"{url}{endpoint_regfhonly}", json=payload_regfhonly)
    data_regfhonly = response_regfhonly.json()
    df_regfhonly = pd.DataFrame(data_regfhonly["results"])

    for i in df_regfhonly['code']:
        if i not in app_countries: 
            df_regfhonly = df_regfhonly.drop(index=df_regfhonly[df_regfhonly['code'] == i].index)

    total_fh = df_regfhonly['amount'].sum()
    total_fh = "{:,}".format(total_fh)

    df_regcom['org'] = agency_name + "($"+total_usaid+")"
    df_regfhonly['org'] = "FH ($"+total_fh+")"

    df_regcom = df_regcom.append(df_regfhonly, ignore_index=True)

    df_regcom = df_regcom.sort_values('amount', ascending=False)

    barchart_regcom = px.bar(
        title = "FH's Share of the " + agency_name + " Market for Where We Work and FY" + str(year_var),
        data_frame=df_regcom,
        x = "name",
        y = "amount",
        color = 'org',
        opacity = 0.9,
        orientation="v",
        barmode='relative',
        template='gridon',
        labels={
            "name": "",
            "amount": "Amount",
            "org": 'Organization'
        }
    )

    return barchart_regcom

while True:
    try:
        barchart_regcom = chart_4(year_start,year_end,agency_filter)
        break
    except KeyError:
        print("")
        print ("FH doesn't have funding from provided agency (Chart 4); Using default instead (USAID)")
        barchart_regcom = chart_4(year_start,year_end,"Agency for International Development")
        break

# ------------------------------------------------- START OF CHART 5 -------------------------------------------------------------

def chart_5(year_var,year_start,year_end,agency_filter):
    #USG/FH CFDA Categories _cfdafhonly ---Chart 5
    endpoint_cfdafhonly = "/api/v2/search/spending_by_category/cfda"
    payload_cfdafhonly = {
        "filters": {
            "recipient_id": "78911b63-cf98-0b58-4cab-6cabc3be1464-C",
            "time_period": [
                {
                    "start_date": year_start,
                    "end_date": year_end
                }
            ],
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": agency_filter,
                }],
        },
        "category": "cfda",
        "limit": 10,
        "page": 1
    }
    response_cfdafhonly = requests.post(f"{url}{endpoint_cfdafhonly}", json=payload_cfdafhonly)
    data_cfdafhonly = response_cfdafhonly.json()
    df_cfdafhonly = pd.DataFrame(data_cfdafhonly["results"])

    program_numbers = []
    for i in df_cfdafhonly['code']:
        program_numbers.append(i)

    #USG/FH CFDA Categories _cfdausg ---Chart 5
    endpoint_cfdausg = "/api/v2/search/spending_by_category/cfda"
    payload_cfdausg = {
        "filters": {
            "time_period": [
                {
                    "start_date": year_start,
                    "end_date": year_end
                }
            ],
            "agencies": [
                {
                    "type": "awarding",
                    "tier": "toptier",
                    "name": agency_filter,
                }],
            "program_numbers": program_numbers
        },
        "category": "cfda",
        "limit": 10,
        "page": 1
    }
    response_cfdausg = requests.post(f"{url}{endpoint_cfdausg}", json=payload_cfdausg)
    data_cfdausg = response_cfdausg.json()
    df_cfdausg = pd.DataFrame(data_cfdausg["results"])

    df_cfdausg['org'] = "USAID"
    df_cfdafhonly['org'] = "Food for the Hungry"

    df_cfdausg = df_cfdausg.append(df_cfdafhonly, ignore_index=True)

    df_cfdausg = df_cfdausg.sort_values('amount', ascending=False)

    df_cfdausg['Name and Code'] = df_cfdausg['code'] + ' ' + df_cfdausg['name']

    barchart_cfdafhonly = px.bar(
        title = "FH's CFDA versus the USG Available Market " + str(year_var),
        data_frame=df_cfdausg,
        x = "Name and Code",
        y = "amount",
        color = "org",
        opacity = 0.9,
        orientation="v",
        barmode='relative',
        template='gridon',
        labels={
            "Name and Code": "",
            "amount": "Amount",
            "org": 'Organization'
        }
    )

    return barchart_cfdafhonly

while True:
    try:
        barchart_cfdafhonly = chart_5(year_var,year_start,year_end,agency_filter)
        break
    except KeyError:
        print("")
        print ("FH doesn't have funding from provided agency (Chart 5); Using default instead (USAID)")
        barchart_cfdafhonly = chart_5(year_var,year_start,year_end,"Agency for International Development")
        break

# ------------------------------------------------- START OF CHART 6 -------------------------------------------------------------

df_reg_custom = ""
df_cfda_custom = ""
end_loop_recipient = 0
while end_loop_recipient != 1:
    if recipient_name == "CRS":
        df_reg_custom = df_regcrs
        df_cfda_custom = df_cfdacrs
        end_loop_recipient = 1
    elif recipient_name == "SAVE":
        df_reg_custom = df_regsav
        df_cfda_custom = df_cfdasav
        end_loop_recipient = 1
    elif recipient_name == "MCORPS":
        df_reg_custom = df_regmc
        df_cfda_custom = df_cfdamc
        end_loop_recipient = 1
    elif recipient_name == "WVISION":
        df_reg_custom = df_regwv
        df_cfda_custom = df_cfdawv
        end_loop_recipient = 1
    else:
        print("")
        print("Incorrect Competitor Recipient Name; Please input one of available")
        recipient_name = input("Available Options: CRS, SAVE, MCORPS, or WVISION: ")


#Reg per individual competitor - uses dataframe from Chart 3
barchart_reg_custom = px.bar(
    title = "Top 10 USG Funded Countries for " + recipient_name + " for FY" + str(year_var),
    data_frame=df_reg_custom,
    x = "name",
    y = "amount",
    opacity = 0.9,
    orientation="v",
    barmode='relative',
    template='gridon',
    labels={
        "name": "",
        "amount": "Amount"
    }
)

# ------------------------------------------------- START OF CHART 7 -------------------------------------------------------------

#CFDA per individual competitor - uses dataframe from Chart 3
barchart_cfda_custom = px.bar(
    title = "Top 10 USG Funded CFDA Categories for " + recipient_name + " for FY" + str(year_var),
    data_frame=df_cfda_custom,
    x = "name",
    y = "amount",
    opacity = 0.9,
    orientation="v",
    barmode='relative',
    template='gridon',
    labels={
        "name": "",
        "amount": "Amount"
    }
)

# ------------------------------------------------- START OF CHART 8 -------------------------------------------------------------

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


# ------------------------------------------------- Settings and Upload -------------------------------------------------------------

#Barchart Styles
barchart_reg.update_layout(hovermode="x",barmode='overlay')
barchart_regfh.update_layout(hovermode="x",barmode='overlay')
barchart_cfdafh.update_layout(hovermode="x",barmode='overlay')
barchart_regcom.update_layout(hovermode="x",barmode='overlay')
barchart_cfdafhonly.update_layout(hovermode="x",barmode='overlay')
barchart_cfda_custom.update_layout(hovermode="x",barmode='overlay')
barchart_reg_custom.update_layout(hovermode="x",barmode='overlay')
scatterplot.update_traces(marker={'size': 15})


# #Post to Plotly
# py.plot(barchart_reg, filename = 'Chart #1', auto_open = False)
# py.plot(barchart_regfh, filename = 'Chart #2', auto_open = False)
# py.plot(barchart_cfdafh, filename = 'Chart #3', auto_open = False)
# py.plot(barchart_regcom, filename = 'Chart #4', auto_open = False)
# py.plot(barchart_cfdafhonly, filename = 'Chart #5', auto_open = False)
# py.plot(barchart_reg_custom, filename = 'Chart #6', auto_open = False)
# py.plot(barchart_cfda_custom, filename = 'Chart #7', auto_open = False)
# py.plot(scatterplot, filename = 'USAID BF for Washington', auto_open = False)

barchart_reg.show()
barchart_regfh.show()
barchart_cfdafh.show()
barchart_regcom.show()
barchart_cfdafhonly.show()
barchart_cfda_custom.show()
barchart_reg_custom.show()
scatterplot.show()






