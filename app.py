import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

data=pd.read_csv("MA_PREDICTOR/data/ma_detailed_data_car_clean.csv")

'''
# M&A Predictor

What would be the probabilities that the cumulative abnormal return for a given merger with the following parameters will be positive, negative or neutral?
'''

target_status = st.selectbox(
    "What is the target's status?",
    options=['public', 'others'])

acquisition_count = st.number_input(
    'How many successful acquisitions has the acquiring company had in the past?',
    value=7)

shares_at_announcement = st.selectbox(
    'Did the acquiror own shares of the target before the merger?',
    options=['yes', 'no'])

shares_acquired = st.selectbox(
    "Will the acquiror obtain full control of the target after the merger?",
    options=['full', 'not_full'])

consideration_offered = st.selectbox(
    'How will the merger be financed?',
    options=['Cash', 'Other'])

bidder_count = st.number_input(
    'How many bidders were present in the merger process?',
    value=1)

deal_value = st.number_input(
    "What is the deal value (in million)?",
    value=2000)

total_assets = st.number_input(
    "What is the total value of assets (in million)?",
    value=10000)

cross_border = st.selectbox(
    'Is the acuisition happening across borders?',
    options=['national', 'cross_border'])

relatedness = st.selectbox(
    'What is the relation between target and acquiror?',
    options=[
        'not_related',
        'industry',
        'industry_group',
        'economic_sector',
        'business_sector'])

econ_sector_ac = st.selectbox(
    'In what economic sector is the acquiror active?',
    options=[
        'Consumer Non-Cyclicals', 'Financials', 'Basic Materials', 'Energy',
        'Industrials', 'Real Estate', 'Technology', 'Healthcare',
        'Consumer Cyclicals', 'Utilities', 'Academic & Educational Services'
    ])


business_sector_ac = st.selectbox(
    'In what business sector is the acquiror active?',
    options=list(data[data['economic_sector_ac'] == econ_sector_ac]
                 ['business_sector_ac'].unique()))

econ_sector_t = st.selectbox(
    'In what economic sector is the target active?',
    options=[
        'Consumer Non-Cyclicals', 'Financials',
        'Basic Materials', 'Energy', 'Industrials',
        'Real Estate', 'Technology', 'Healthcare',
        'Consumer Cyclicals', 'Utilities',
        'Academic & Educational Services'])

business_sector_t = st.selectbox(
    'In what business sector is the target active?',
    options=list(data[data['economic_sector_target'] == econ_sector_t]
                 ['business_sector_ac'].unique()))


cluster_category = st.selectbox(
    'What is the acquisition technique?',
    options=[
        'divestiture', 'asset_driven_op', 'private_companies', 'bankruptcy',
        'possible_problematic', 'Unknown'
    ])

a_fin_adv_count = st.multiselect(
    "Select the acquiror's financial advisors (if present in the list):",
    options=[
        'Barclays', 'Bank of America', 'Citi', 'Credit Suisse',
        'Goldman Sachs', 'JP Morgan', 'Lazard', 'Morgan Stanley', 'Rothschild',
        'UBS'
    ])

t_fin_adv_count = st.multiselect(
     "Select the target's financial advisors (if present in the list):",
    options=[
        'Barclays', 'Bank of America', 'Citi', 'Credit Suisse',
        'Goldman Sachs', 'JP Morgan', 'Lazard', 'Morgan Stanley', 'Rothschild',
        'UBS'
    ])

car_wanted = st.selectbox(
    'Which time horizon do you want to select to compute the CAR:',
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
