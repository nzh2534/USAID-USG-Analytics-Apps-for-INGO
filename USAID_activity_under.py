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

def usaid_act_fxn_under(chart_name, year_var, country_name_input,username,api_key):

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.usaid.gov", "fUVyoT1bwM4on31Ux67EHfpcG")
    results = client.get("azij-hu6e", country_name=country_name_input,fiscal_year=year_var)
    results_df = pd.DataFrame.from_records(results)

    results_df['Activity'] = results_df['activity_name'] + ' ' + results_df['activity_project_number'] + ' - ' + results_df['implementing_partner_name']

    results_df.current_dollar_amount = pd.to_numeric(results_df.current_dollar_amount, errors='coerce')

    activity_name_list = []
    for i in results_df['Activity']:
        if i in activity_name_list:
            continue
        elif i not in activity_name_list:
            activity_name_list.append(i)

    activity_name_dict ={}
    for i in activity_name_list:
        activity_name_dict[i]= results_df.loc[results_df['Activity'] == i, 'current_dollar_amount'].sum()

    activity_name_amount = []
    for i in activity_name_list:
        activity_name_amount.append(activity_name_dict[i])

    dict_for_df = {'Activity':activity_name_list,'Amount':activity_name_amount}

    results_df = pd.DataFrame(dict_for_df)

    results_df = results_df.loc[results_df["Amount"] <= 1000000]

    results_df = results_df.sort_values("Amount", ascending=False)

    barchart = px.bar(
            title = "USAID " + country_name_input + " Funding by Activity (Less than or Equal to $1M) for " + year_var,
            data_frame=results_df,
            x = "Activity",
            y = "Amount",
            opacity = 0.9,
            orientation="v",
            barmode='relative',
            template='gridon',
            labels={
                "Activity": "",
            }
        )

    barchart.update_layout(hovermode="x",barmode='overlay')

    #py.plot(barchart, filename = chart_name, auto_open = False)

    barchart.show()

fh_dict_activity = {
    "Bangladesh":"USAID Activity Bangladesh",
    "Bolivia":"USAID Activity Bolivia",
    "Burundi":"USAID Activity Burundi",
    "Cambodia":"USAID Activity Cambodia",
    "Congo (Kinshasa)":"USAID Activity Congo (Kinshasa)",
    "Dominican Republic":"USAID Activity Dominican Republic",
    "Ethiopia":"USAID Activity Ethiopia",
    "Guatemala":"USAID Activity Guatemala",
    "Haiti":"USAID Activity Haiti",
    "Indonesia":"USAID Activity Indonesia",
    "Kenya":"USAID Activity Kenya",
    "Mozambique":"USAID Activity Mozambique",
    "Nicaragua":"USAID Activity Nicaragua",
    "Peru":"USAID Activity Peru",
    "Philippines":"USAID Activity Philippines",
    "Rwanda":"USAID Activity Rwanda",
    "South Sudan":"USAID Activity South Sudan",
    "Uganda":"USAID Activity Uganda"}

for i in fh_dict_activity:
    usaid_act_fxn_under(fh_dict_activity[i],year_var,i)