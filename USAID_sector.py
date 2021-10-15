import pandas as pd
from sodapy import Socrata

import numpy as np

from sklearn.datasets import load_iris

import plotly
import plotly.express as px
import plotly.io as pio

import chart_studio

year_var = input("Fiscal Year?: ")
username = input("Chart Studio Username?: ")
api_key = input("Chart Studio Password?: ")

def usaid_sec_fxn(chart_name, year_var, country_name_input,username,api_key):

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    import chart_studio.plotly as py
    import chart_studio.tools as tls

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.usaid.gov", "fUVyoT1bwM4on31Ux67EHfpcG")

    results = client.get("azij-hu6e", country_name=country_name_input,fiscal_year=year_var)
    results_df = pd.DataFrame.from_records(results)

    results_df.current_dollar_amount = pd.to_numeric(results_df.current_dollar_amount, errors='coerce')

    sector_name_list = []
    for i in results_df['us_sector_name']:
        if i in sector_name_list:
            continue
        elif i not in sector_name_list:
            sector_name_list.append(i)

    sector_name_dict ={}
    for i in sector_name_list:
        sector_name_dict[i]= results_df.loc[results_df['us_sector_name'] == i, 'current_dollar_amount'].sum()

    sector_name_amount = []
    for i in sector_name_list:
        sector_name_amount.append(sector_name_dict[i])

    dict_for_df = {'Sector':sector_name_list,'Amount':sector_name_amount}

    results_df = pd.DataFrame(dict_for_df)

    results_df = results_df.sort_values("Amount", ascending=False)

    barchart = px.bar(
            title = "USAID " + country_name_input + " Funding by Sector for " + year_var,
            data_frame=results_df,
            x = "Sector",
            y = "Amount",
            opacity = 0.9,
            orientation="v",
            barmode='relative',
            template='gridon',
            labels={
                "Sector": "",
            }
        )

    barchart.update_layout(hovermode="x",barmode='overlay')

    # py.plot(barchart, filename = chart_name, auto_open = False)
    
    barchart.show()

fh_dict_sec = {
    "Bangladesh":"USAID Sector Bangladesh",
    "Bolivia":"USAID Sector Bolivia",
    "Burundi":"USAID Sector Burundi",
    "Cambodia":"USAID Sector Cambodia",
    "Congo (Kinshasa)":"USAID Sector Congo (Kinshasa)",
    "Dominican Republic":"USAID Sector Dominican Republic",
    "Ethiopia":"USAID Sector Ethiopia",
    "Guatemala":"USAID Sector Guatemala",
    "Haiti":"USAID Sector Haiti",
    "Indonesia":"USAID Sector Indonesia",
    "Kenya":"USAID Sector Kenya",
    "Mozambique":"USAID Sector Mozambique",
    "Nicaragua":"USAID Sector Nicaragua",
    "Peru":"USAID Sector Peru",
    "Philippines":"USAID Sector Philippines",
    "Rwanda":"USAID SectorRwanda",
    "South Sudan":"USAID Sector South Sudan",
    "Uganda":"USAID Sector Uganda"}

for i in fh_dict_sec:
    usaid_sec_fxn(fh_dict_sec[i],year_var,i)