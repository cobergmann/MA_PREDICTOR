import streamlit as st
import joblib
import datetime
import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

data=pd.read_csv("MA_PREDICTOR/data/ma_detailed_data_car_clean.csv")

'''
# M&A Predictor

What would be the probabilities that the Cumulative Abnormal Return for a given merger with the following parameters will be positive, negative or neutral?
'''

target_status = st.selectbox('What is the target status?',
                             options=['public', 'others'])

acquisition_count = st.number_input(
    'How many acquisitions have been done by the acquiror company?', value=7)
shares_at_announcement = st.selectbox('Did the acquiror company owned shares of the target company before the merger ?',
                                      options=['yes', 'no'])
shares_acquired = st.selectbox(
    'Will the acquiring company own the totality of the target shares after the merger ?',
    options=['full', 'not_full'])
consideration_offered = st.selectbox(
    'How the merger will be financed ?',
    options=['Cash', 'Other'])
bidder_count = st.number_input(
    'How many bidders were present in the merger process?', value=1)
deal_value = st.number_input("What is the deal value (in million)?", value=2654)
total_assets = st.number_input("What is the total value of assets (in million)?", value=1234)
cross_border = st.selectbox('Is the merger national or cross-border ?',
                            options=['national', 'cross_border'])
relatedness = st.selectbox(
    'How related are the acquiring and the target companies to each other ?',
    options=[
        'not_related', 'industry', 'industry_group', 'economic_sector',
        'business_sector'
    ])
econ_sector_ac = st.selectbox(
    'What is the economic sector of the acquiring company?',
    options=[
        'Consumer Non-Cyclicals', 'Financials', 'Basic Materials', 'Energy',
        'Industrials', 'Real Estate', 'Technology', 'Healthcare',
        'Consumer Cyclicals', 'Utilities', 'Academic & Educational Services'
    ])


business_sector_ac = st.selectbox(
    'What is the business sector of the acquiring company?',
    options=list(data[data['economic_sector_ac'] == econ_sector_ac]['business_sector_ac'].unique()))

econ_sector_t = st.selectbox(
    'What is the economic sector of the target company?',
    options=[
        'Consumer Non-Cyclicals', 'Financials', 'Basic Materials', 'Energy',
        'Industrials', 'Real Estate', 'Technology', 'Healthcare',
        'Consumer Cyclicals', 'Utilities', 'Academic & Educational Services'
    ])

business_sector_t = st.selectbox(
    'What is the business sector of the target company?',
    options=list(data[data['economic_sector_target'] == econ_sector_t]
                 ['business_sector_ac'].unique()))


cluster_category = st.selectbox(
    'What is the acquisition technique?',
    options=[
        'divestiture', 'asset_driven_op', 'private_companies', 'bankruptcy',
        'possible_problematic', 'Unknown'
    ])

a_fin_adv_count = st.multiselect(
    'Select the financial advisors for the acquiring company (if present in the list):',
    options=[
        'Barclays', 'Bank of America', 'Citi', 'Credit Suisse',
        'Goldman Sachs', 'JP Morgan', 'Lazard', 'Morgan Stanley', 'Rothschild',
        'UBS'
    ])

t_fin_adv_count = st.multiselect(
    'Select the financial advisors for the target company (if present in the list):',
    options=[
        'Barclays', 'Bank of America', 'Citi', 'Credit Suisse',
        'Goldman Sachs', 'JP Morgan', 'Lazard', 'Morgan Stanley', 'Rothschild',
        'UBS'
    ])

car_wanted = st.selectbox(
    'Which horizon do you want to select to compute the CAR :',
    options=[
        1, 3, 5, 10
    ], key=10 )



params = dict(target_status=[target_status],
              acquisition_count=[acquisition_count],
              shares_at_announcement=[shares_at_announcement],
              shares_acquired=[shares_acquired],
              consideration_offered=[consideration_offered],
              bidder_count=[bidder_count],
              rel_deal_value=[deal_value / total_assets],
              cross_border=[cross_border],
              relatedness=[relatedness],
              economic_sector_ac=[econ_sector_ac],
              business_sector_ac=[business_sector_ac],
              economic_sector_target=[econ_sector_t],
              business_sector_target=[business_sector_t],
              cluster_category=[cluster_category],
              a_fin_adv_count=[len(a_fin_adv_count)],
              t_fin_adv_count=[len(t_fin_adv_count)])

df_pred= pd.DataFrame.from_dict(params)

# Testing the model
sgd = joblib.load(f'MA_PREDICTOR/models/SGDClassifier_car{car_wanted}')
arr=sgd.predict_proba(df_pred)[0]
results = list(arr)


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Negative', 'Neutral', 'Positive'
sizes = results
explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')


if st.button('Get your prediction'):
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,
            explode=explode,
            autopct='%1.0f%%',
            shadow=False,
            startangle=90,
            colors=['#2a4d69', '#4b86b4', '#adcbe3'])
    fig1.legend(
        labels,
        edgecolor='white',
        prop=matplotlib.font_manager.FontProperties(family='monospace'))
    fig1.patch.set_facecolor('#0e1117')
    ax1.axis('equal')   #Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
    st.balloons()
