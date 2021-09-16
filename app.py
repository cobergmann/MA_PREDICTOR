import streamlit as st

import datetime
import pandas as pd
import requests

data=pd.read_csv("MA_PREDICTOR/data/ma_detailed_data_car_clean.csv")
#st.write(data.head())
'''
# M&A Predictor

What would be the Cumulative Abnormal Return for a given merger with the following parameters:
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


params = dict(target_status=target_status,
              acquisition_count=acquisition_count,
              shares_at_announcement=shares_at_announcement,
              shares_acquired=shares_acquired,
              consideration_offered=consideration_offered,
              bidder_count=bidder_count,
              rel_deal_value=deal_value / total_assets,
              cross_border=cross_border,
              relatedness=relatedness,
              economic_sector_ac=econ_sector_ac,
              business_sector_ac=business_sector_ac,
              economic_sector_target=econ_sector_t,
              business_sector_target=business_sector_t,
              cluster_category=cluster_category,
              a_fin_adv_count=list(a_fin_adv_count),
              t_fin_adv_count=list(t_fin_adv_count))




if st.button('Get your prediction'):
    st.write('Why hello there')
    st.balloons()
