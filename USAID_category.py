import pandas as pd
from sodapy import Socrata

import numpy as np

from sklearn.datasets import load_iris

import plotly
import plotly.express as px
import plotly.io as pio

import chart_studio
import chart_studio.plotly as py
import chart_studio.tools as tls

year_var = input("Fiscal Year?: ")
username = input("Chart Studio Username?: ")
api_key = input("Chart Studio Password?: ")

def usaid_cat_fxn(chart_name, year_var, country_name_input,username,api_key):

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.usaid.gov", "fUVyoT1bwM4on31Ux67EHfpcG")
    results = client.get("azij-hu6e", country_name=country_name_input,fiscal_year=year_var)
    results_df = pd.DataFrame.from_records(results)

    results_df.current_dollar_amount = pd.to_numeric(results_df.current_dollar_amount, errors='coerce')

    category_name_list = []
    for i in results_df['us_category_name']:
        if i in category_name_list:
            continue
        elif i not in category_name_list:
            category_name_list.append(i)

    category_name_dict ={}
    for i in category_name_list:
        category_name_dict[i]= results_df.loc[results_df['us_category_name'] == i, 'current_dollar_amount'].sum()

    category_name_amount = []
    for i in category_name_list:
        category_name_amount.append(category_name_dict[i])

    dict_for_df = {'Category':category_name_list,'Amount':category_name_amount}

    results_df = pd.DataFrame(dict_for_df)

    results_df = results_df.sort_values("Amount", ascending=False)

    barchart = px.bar(
            title = "USAID " + country_name_input + " Funding by Category for " + year_var,
            data_frame=results_df,
            x = "Category",
            y = "Amount",
            opacity = 0.9,
            orientation="v",
            barmode='relative',
            template='gridon',
            labels={
                "Category": "",
            }
        )

    barchart.update_layout(hovermode="x",barmode='overlay')

    #py.plot(barchart, filename = chart_name, auto_open = False)

    barchart.show()

fh_dict_category = {
    "Bangladesh":"USAID Category Bangladesh",
    "Bolivia":"USAID Category Bolivia",
    "Burundi":"USAID Category Burundi",
    "Cambodia":"USAID Category Cambodia",
    "Congo (Kinshasa)":"USAID Category Congo (Kinshasa)",
    "Dominican Republic":"USAID Category Dominican Republic",
    "Ethiopia":"USAID Category Ethiopia",
    "Guatemala":"USAID Category Guatemala",
    "Haiti":"USAID Category Haiti",
    "Indonesia":"USAID Category Indonesia",
    "Kenya":"USAID Category Kenya",
    "Mozambique":"USAID Category Mozambique",
    "Nicaragua":"USAID Category Nicaragua",
    "Peru":"USAID Category Peru",
    "Philippines":"USAID Category Philippines",
    "Rwanda":"USAID Category Rwanda",
    "South Sudan":"USAID Category South Sudan",
    "Uganda":"USAID Category Uganda"}

for i in fh_dict_category:
    usaid_cat_fxn(fh_dict_category[i],year_var,i)