import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px
# import plotly.graph_objs as go
from googletrans import Translator

translator = Translator()

st.set_page_config(layout="wide")

container1 = st.container()
container2 = st.container()
container3 = st.container()
container4 = st.container()

st.markdown("""<style>.big-font {font-size:70px !important;text-align: center;}</style>""", unsafe_allow_html=True)

@st.cache(allow_output_mutation=True)
def load_data(allow_output_mutation=True):
    data = pd.read_csv('https://drive.google.com/file/d/1pYZAPKwUX9SZ3tdD4KH40bBymhccDxkS/view?usp=sharing', encoding='latin-1')
    return data

df = load_data()

df['shipping date (DateOrders)'] = pd.to_datetime(df["shipping date (DateOrders)"])
df[' tanggal order (DateOrders)'] = pd.to_datetime(df[" tanggal order (DateOrders)"])

years = ['Total']+sorted(df[" tanggal order (DateOrders)"].dt.year.unique(),reverse=True)

with container1:
    st.markdown('<p class="big-font">GENERAL OVERVIEW</p>', unsafe_allow_html=True)
    option = st.selectbox('Select data to display', years, index=0)
    st.write('You selected ', option)

with container2:
    
    if option == 'Total':
        df_year = df
    else:
        df_year = df[(df[' tanggal order (DateOrders)'] >= str(option)+'-01-01') & (df[' tanggal order (DateOrders)'] < str(option+1)+'-01-01')]
    # @st.cache(allow_output_mutation=True)
    # def get_country_sales_total():
    #     countries_sales = df_year['Negara order'].value_counts().reset_index()
    #     countries_sales['index'] = countries_sales['index'].apply(lambda x : translator.translate(x).text)
    #     return countries_sales

    # countries = get_country_sales_total()

    total_sales = len(df_year)

    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        st.markdown('#')
        st.markdown('#')
        st.write("Total Sales")
        st.header("{:,.0f}".format(total_sales))
        st.markdown('#')
        if option == 'Total':
            monthly_avg = int(df_year[' tanggal order (DateOrders)'].groupby(df_year[' tanggal order (DateOrders)'].dt.year).agg('count').mean())
            st.write("Yearly sales average")
            st.header("{:,.0f}".format(monthly_avg))
        else:
            monthly_avg = int(df_year[' tanggal order (DateOrders)'].groupby(df_year[' tanggal order (DateOrders)'].dt.month).agg('count').mean()) 
            st.write("Monthly sales average")
            st.header("{:,.0f}".format(monthly_avg))
        
    with col2:
        st.markdown('#')
        st.markdown('#')
        if option == 'Total':   
            total_sales_revenue = int(df_year['penjualan'].groupby(df_year[' tanggal order (DateOrders)'].dt.year).sum().sum())
            st.write("Total sales revenue")
            st.header("${:,.0f}".format(total_sales_revenue))
        else:
            total_sales_revenue = int(df_year['penjualan'].groupby(df_year[' tanggal order (DateOrders)'].dt.month).sum().sum())
            st.write("Total sales revenue")
            st.header("${:,.0f}".format(total_sales_revenue))
        st.markdown("#")
        if option == 'Total':
            sales_revenue = int(df_year['penjualan'].groupby(df_year[' tanggal order (DateOrders)'].dt.year).sum().mean())
            st.write("Yearly sales revenue")
            st.header("${:,.0f}".format(sales_revenue))
        else:
            sales_revenue = int(df_year['penjualan'].groupby(df_year[' tanggal order (DateOrders)'].dt.month).sum().mean()) 
            st.write("Monthly sales revenue")
            st.header("${:,.0f}".format(sales_revenue))

    with col3:
        if option == 'Total':
            monthly_sales = df_year.groupby(df_year[' tanggal order (DateOrders)'].dt.year)[' tanggal order (DateOrders)'].agg('count')
            graph_title = 'TOTAL SALES YEARLY'
        else:
            graph_title = 'TOTAL SALES IN ' + str(option)
            monthly_sales = df_year.groupby(df_year[' tanggal order (DateOrders)'].dt.month)[' tanggal order (DateOrders)'].agg('count')
            monthly_sales.index = pd.to_datetime(monthly_sales.index, format="%m").month_name()
        fig = px.bar(monthly_sales, width=850)
        fig.update_layout(title_text=graph_title, title_x=0.5)
        fig['layout']['title']['font'] = dict(size=20)
        fig.update_xaxes(type='category')
        fig.update_layout(showlegend=False)
        fig.update_yaxes(title='Sales Count')
        fig.update_xaxes(title='')
        fig.update_xaxes(tickangle=315)
        st.plotly_chart(fig)   


with container3:
    # st.subheader("Geographical Overview")
    col1, col2 = st.columns(2)

    with col1:
        region_sales = df_year['pasar'].value_counts().sort_values().reset_index()
        region_sales['percentage'] = region_sales.pasar/len(df_year)*100
        fig2 = px.bar(region_sales, y=region_sales['index'], x=region_sales['pasar'] , orientation='h', height=300, text=region_sales['percentage'])
        fig2.update_xaxes(title='Sales Count')
        fig2.update_yaxes(title='')
        fig2.update_layout(title_text="TOTAL SALES PER REGION", title_x=0.5)
        fig2.update_traces(texttemplate='%{text:.2f} %',textposition='auto')
        fig2['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig2)  

    with col2:
        st.write("NANTI YAAA")
        # fig2 = px.choropleth(countries, locations=countries['index'], color=countries['Negara order'], locationmode='country names')
        # fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        # st.plotly_chart(fig2)  

with container4:
    col1, col2, col3, col4 = st.columns([3.2, 1.5, 1, 1])
    with col1:
        goods_category = df_year['Nama departemen'].value_counts()
        fig3 = px.pie(region_sales, names=goods_category.index, values=goods_category.values, height=550, width=550)
        fig3.update_traces(textfont_size=20)
        fig3.update_layout(title_text="TOTAL SALES PRODUCT CATEGORIES", title_x=0.5)
        fig3['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig3) 
    with col2:
        if option == 'Total':
            sales_profit = df_year['keuntungan Order Per Order'].groupby(df_year[' tanggal order (DateOrders)'].dt.year).sum()
            graph_title = 'SALES PROFIT YEARLY'
        else:
            graph_title = 'SALES PROFIT IN ' + str(option)
            sales_profit = df_year['keuntungan Order Per Order'].groupby(df_year[' tanggal order (DateOrders)'].dt.month).sum()
            sales_profit.index = pd.to_datetime(sales_profit.index, format="%m").month_name()
        fig4 = px.line(sales_profit, width=750, height=300, markers=True, text=sales_profit.values)
        fig4.update_layout(title_text=graph_title, title_x=0.5, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), plot_bgcolor='rgba(255,255,255,0.01)')
        fig4.update_layout(yaxis={'visible': False, 'showticklabels': False})
        fig4.update_traces(texttemplate="$%{text:,.0f}")
        fig4['layout']['title']['font'] = dict(size=20)
        fig4.update_xaxes(type='category')
        fig4.update_layout(showlegend=False, margin=dict(l=0))
        fig4.update_yaxes(title='Profit')
        fig4.update_xaxes(title='')
        fig4.update_xaxes(tickangle=340)
        st.plotly_chart(fig4)  

        if option == 'Total':   
            profit_average = int(df_year['keuntungan Order Per Order'].groupby(df_year[' tanggal order (DateOrders)'].dt.year).sum().mean())
            st.write("Yearly profit average")
            st.header("${:,.0f}".format(profit_average))
        else:
            profit_average = int(df_year['keuntungan Order Per Order'].groupby(df_year[' tanggal order (DateOrders)'].dt.month).sum().mean())
            st.write("Monthly profit average")
            st.header("${:,.0f}".format(profit_average))
    
    with col3:
        profit_average_perorder = df_year['keuntungan Order Per Order'].mean()
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.write("Profit per order")
        st.header("${:,.2f}".format(profit_average_perorder))

    with col4:
        profit_ratio_average_perorder = df_year['rasio keuntungan Order Item'].mean()
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        st.write("Profit ratio per order")
        st.header("{:,.4f}".format(profit_ratio_average_perorder))

    
    

