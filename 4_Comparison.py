from cProfile import label
from tkinter.font import names
from pyparsing import line
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go
import calendar

st.set_page_config(layout="wide")

container1 = st.container()
st.markdown("""<style>.big-font {font-size:70px !important;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.medium-font {font-size:40px !important;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.small-font {font-size:20px !important;text-align: center;}</style>""", unsafe_allow_html=True)
    
@st.cache(allow_output_mutation=True)
def load_data(allow_output_mutation=True):
    data = pd.read_csv('D:\Koding\Python\Dashboard KMMI\dataset1_clean.csv', encoding='latin-1')
    return data

df = load_data()

df['shipping date (DateOrders)'] = pd.to_datetime(df["shipping date (DateOrders)"])
df[' tanggal order (DateOrders)'] = pd.to_datetime(df[" tanggal order (DateOrders)"])

years = sorted(df[" tanggal order (DateOrders)"].dt.year.unique(),reverse=True)
months = sorted(df[" tanggal order (DateOrders)"].dt.month.unique())
months = pd.to_datetime(months, format="%m").month_name()

with container1:
    st.markdown('<p class="big-font">DATA COMPARISON</p>', unsafe_allow_html=True)
    option = st.selectbox('Select type of comparison', ['yearly', 'monthly'], index=0)
    if option == 'yearly':
        col1, col2, col3 = st.columns(3)
        with col1:
            year_choice = st.selectbox('Select type of comparison', years, label_visibility='collapsed')
            years2 = [x for x in years if x != year_choice]
        with col2:
            st.markdown('<p class="small-font">COMPARED TO</p>', unsafe_allow_html=True)
        with col3:
            year_choice2 = st.selectbox('Select type of comparison', years2, label_visibility='collapsed')
        data1_name = str(year_choice)
        data2_name = str(year_choice2)
        df_data1 = df[(df[' tanggal order (DateOrders)'] > str(year_choice)+'-01-01') & (df[' tanggal order (DateOrders)'] < str(year_choice+1)+'-01-01')]
        df_data2 = df[(df[' tanggal order (DateOrders)'] >= str(year_choice2)+'-01-01') & (df[' tanggal order (DateOrders)'] < str(year_choice2+1)+'-01-01')]
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            months_option = st.selectbox('Select type of comparison', months, index=0, key='month1', label_visibility='collapsed')
        with col2:
            years_option = option2 = st.selectbox('Select type of comparison', years, index=0, key='year1', label_visibility='collapsed')
        with col3:
            st.markdown('<p class="small-font">COMPARED TO</p>', unsafe_allow_html=True)
        with col4:
            months_option2 = st.selectbox('Select type of comparison', months, index=0, key='month2', label_visibility='collapsed')
        with col5:
            years_option2 = st.selectbox('Select type of comparison', years, index=0, key='year2', label_visibility='collapsed')
        if (months_option == months_option2) & (years_option == years_option2):
            st.warning('Months inputed should be different')
            st.stop()
        else:
            month1 = datetime.datetime.strptime(months_option, "%B").month
            month2 = datetime.datetime.strptime(months_option2, "%B").month
            data1_name = months_option+" "+str(years_option)
            data2_name = months_option2+" "+str(years_option2)
            if months_option == 'December':
                df_data1 = df[(df[' tanggal order (DateOrders)'] >= str(years_option)+'-'+str(month1)+'-01') & (df[' tanggal order (DateOrders)'] <= str(years_option)+'-12-31')]
            else:
                df_data1 = df[(df[' tanggal order (DateOrders)'] >= str(years_option)+'-'+str(month1)+'-01') & (df[' tanggal order (DateOrders)'] < str(years_option)+'-'+str(month1+1)+'-01')]
            if months_option2 == 'December':
                df_data2 = df[(df[' tanggal order (DateOrders)'] >= str(years_option2)+'-'+str(month2)+'-01') & (df[' tanggal order (DateOrders)'] <= str(years_option2)+'-12-31')]
            else:
                df_data2 = df[(df[' tanggal order (DateOrders)'] >= str(years_option2)+'-'+str(month2)+'-01') & (df[' tanggal order (DateOrders)'] < str(years_option2)+'-'+str(month2+1)+'-01')]

container2 = st.container()

with container2:
    if option == 'yearly':
        data1_sales_recap = df_data1[' tanggal order (DateOrders)'].groupby(df_data1[' tanggal order (DateOrders)'].dt.month).agg('count').reset_index(name='Count')
        data1_sales_recap[' tanggal order (DateOrders)'] = [calendar.month_name[x] for x in data1_sales_recap[' tanggal order (DateOrders)']] 
        data2_sales_recap = df_data2[' tanggal order (DateOrders)'].groupby(df_data2[' tanggal order (DateOrders)'].dt.month).agg('count').reset_index(name='Count')
        data2_sales_recap[' tanggal order (DateOrders)'] = [calendar.month_name[x] for x in data2_sales_recap[' tanggal order (DateOrders)']]       
    else:
        data1_sales_recap = df_data1[' tanggal order (DateOrders)'].groupby(df_data1[' tanggal order (DateOrders)'].dt.date).agg('count').reset_index(name='Count')
        data1_sales_recap[' tanggal order (DateOrders)'] = [x.strftime("%d") for x in data1_sales_recap[' tanggal order (DateOrders)']] 
        data2_sales_recap = df_data2[' tanggal order (DateOrders)'].groupby(df_data2[' tanggal order (DateOrders)'].dt.date).agg('count').reset_index(name='Count')
        data2_sales_recap[' tanggal order (DateOrders)'] = [x.strftime("%d") for x in data2_sales_recap[' tanggal order (DateOrders)']]           
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data1_sales_recap[' tanggal order (DateOrders)'], y=data1_sales_recap['Count'], fill='tozeroy', name=data1_name))
    fig.add_trace(go.Scatter(x=data2_sales_recap[' tanggal order (DateOrders)'], y=data2_sales_recap['Count'], fill='tozeroy', name=data2_name))
    fig.update_layout(width=700, height=300, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig)