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

def usaid_partner_fxn(chart_name, year_var, country_name_input,username,api_key):

    chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.usaid.gov", "fUVyoT1bwM4on31Ux67EHfpcG")
    results = client.get("azij-hu6e", country_name=country_name_input,fiscal_year=year_var)
    results_df = pd.DataFrame.from_records(results)

    results_df.current_dollar_amount = pd.to_numeric(results_df.current_dollar_amount, errors='coerce')

    partner_name_list = []
    for i in results_df['implementing_partner_name']:
        if i in partner_name_list:
            continue
        elif i not in partner_name_list:
            partner_name_list.append(i)

    partner_name_dict ={}
    for i in partner_name_list:
        partner_name_dict[i]= results_df.loc[results_df['implementing_partner_name'] == i, 'current_dollar_amount'].sum()

    partner_name_amount = []
    for i in partner_name_list:
        partner_name_amount.append(partner_name_dict[i])

    dict_for_df = {'Partner':partner_name_list,'Amount':partner_name_amount}

    results_df = pd.DataFrame(dict_for_df)

    results_df = results_df.sort_values("Amount", ascending=False)

    barchart = px.bar(
            title = "USAID " + country_name_input + " Funding by Implementing Partners for " + year_var,
            data_frame=results_df,
            x = "Partner",
            y = "Amount",
            opacity = 0.9,
            orientation="v",
            barmode='relative',
            template='gridon',
            labels={
                "Partner": "",
            }
        )

    barchart.update_layout(hovermode="x",barmode='overlay')

    # py.plot(barchart, filename = chart_name, auto_open = False)

    barchart.show()

fh_dict_partner = {
    "Bangladesh":"USAID Implementing Partners Bangladesh",
    "Bolivia":"USAID Implementing Partners Bolivia",
    "Burundi":"USAID Implementing Partners Burundi",
    "Cambodia":"USAID Implementing Partners Cambodia",
    "Congo (Kinshasa)":"USAID Implementing Partners Congo (Kinshasa)",
    "Dominican Republic":"USAID Implementing Partners Dominican Republic",
    "Ethiopia":"USAID Implementing Partners Ethiopia",
    "Guatemala":"USAID Implementing Partners Guatemala",
    "Haiti":"USAID Implementing Partners Haiti",
    "Indonesia":"USAID Implementing Partners Indonesia",
    "Kenya":"USAID Implementing Partners Kenya",
    "Mozambique":"USAID Implementing Partners Mozambique",
    "Nicaragua":"USAID Implementing Partners Nicaragua",
    "Peru":"USAID Implementing Partners Peru",
    "Philippines":"USAID Implementing Partners Philippines",
    "Rwanda":"USAID Implementing Partners Rwanda",
    "South Sudan":"USAID Implementing Partners South Sudan",
    "Uganda":"USAID Implementing Partners Uganda"}

for i in fh_dict_partner:
    usaid_partner_fxn(fh_dict_partner[i],year_var,i)