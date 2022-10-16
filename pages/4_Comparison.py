import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import plotly.graph_objects as go
import calendar
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

container1 = st.container()
st.markdown("""<style>.big-font {font-size:70px !important;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.medium-font {font-size:40px !important;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.small-font {font-size:25px !important;text-align: center;}</style>""", unsafe_allow_html=True)
    
@st.cache(allow_output_mutation=True)
def load_data(allow_output_mutation=True):
    url='https://drive.google.com/file/d/1pYZAPKwUX9SZ3tdD4KH40bBymhccDxkS/view?usp=sharing'
    file_id=url.split('/')[-2]
    dwn_url='https://drive.google.com/uc?id=' + file_id
    data = pd.read_csv(dwn_url, encoding='latin-1')
    return data

df = load_data()

df['shipping date (DateOrders)'] = pd.to_datetime(df["shipping date (DateOrders)"])
df[' tanggal order (DateOrders)'] = pd.to_datetime(df[" tanggal order (DateOrders)"])

years = sorted(df[" tanggal order (DateOrders)"].dt.year.unique(),reverse=True)
months = sorted(df[" tanggal order (DateOrders)"].dt.month.unique())
months = pd.to_datetime(months, format="%m").month_name()

with container1:
    st.markdown('<p class="big-font">DATA COMPARISON</p>', unsafe_allow_html=True)
    option = st.selectbox('Select type of comparison', ['year', 'month'], index=0)
    if option == 'year':
        xaxes_title = ""
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
        xaxes_title = "Date"
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
    col1, col2, col3, col4 = st.columns([3.3, 1, 1, 1])
    if option == 'year':
        segmentation_details = '(monthly)'
        data1_sales_recap = df_data1[' tanggal order (DateOrders)'].groupby(df_data1[' tanggal order (DateOrders)'].dt.month).agg('count').reset_index(name='Count')
        data1_sales_recap[' tanggal order (DateOrders)'] = [calendar.month_name[x] for x in data1_sales_recap[' tanggal order (DateOrders)']] 
        data2_sales_recap = df_data2[' tanggal order (DateOrders)'].groupby(df_data2[' tanggal order (DateOrders)'].dt.month).agg('count').reset_index(name='Count')
        data2_sales_recap[' tanggal order (DateOrders)'] = [calendar.month_name[x] for x in data2_sales_recap[' tanggal order (DateOrders)']] 
        
        data1_revenue = df_data1['total Order Item'].groupby(df_data1[' tanggal order (DateOrders)'].dt.month).agg('sum').reset_index(name='sum')
        data1_revenue['total Order Item'] = [calendar.month_name[x] for x in data1_revenue[' tanggal order (DateOrders)']] 
        data2_revenue = df_data2['total Order Item'].groupby(df_data2[' tanggal order (DateOrders)'].dt.month).agg('sum').reset_index(name='sum')
        data2_revenue['total Order Item'] = [calendar.month_name[x] for x in data2_revenue[' tanggal order (DateOrders)']] 

        data1_profit = df_data1['keuntungan Order Per Order'].groupby(df_data1[' tanggal order (DateOrders)'].dt.month).agg('sum').reset_index(name='sum')
        data1_profit['keuntungan Order Per Order'] = [calendar.month_name[x] for x in data1_revenue[' tanggal order (DateOrders)']] 
        data2_profit = df_data2['keuntungan Order Per Order'].groupby(df_data2[' tanggal order (DateOrders)'].dt.month).agg('sum').reset_index(name='sum')
        data2_profit['keuntungan Order Per Order'] = [calendar.month_name[x] for x in data2_revenue[' tanggal order (DateOrders)']]   
              
    else:
        segmentation_details = '(daily)'
        data1_sales_recap = df_data1[' tanggal order (DateOrders)'].groupby(df_data1[' tanggal order (DateOrders)'].dt.date).agg('count').reset_index(name='Count')
        data1_sales_recap[' tanggal order (DateOrders)'] = [x.strftime("%d") for x in data1_sales_recap[' tanggal order (DateOrders)']] 
        data2_sales_recap = df_data2[' tanggal order (DateOrders)'].groupby(df_data2[' tanggal order (DateOrders)'].dt.date).agg('count').reset_index(name='Count')
        data2_sales_recap[' tanggal order (DateOrders)'] = [x.strftime("%d") for x in data2_sales_recap[' tanggal order (DateOrders)']]  
        
        data1_revenue = df_data1['total Order Item'].groupby(df_data1[' tanggal order (DateOrders)'].dt.date).agg('sum').reset_index(name='sum')
        data1_revenue['total Order Item'] = [x.strftime("%d") for x in data1_revenue[' tanggal order (DateOrders)']] 
        data2_revenue = df_data2['total Order Item'].groupby(df_data2[' tanggal order (DateOrders)'].dt.date).agg('sum').reset_index(name='sum')
        data2_revenue['total Order Item'] = [x.strftime("%d") for x in data2_revenue[' tanggal order (DateOrders)']] 

        data1_profit = df_data1['keuntungan Order Per Order'].groupby(df_data1[' tanggal order (DateOrders)'].dt.date).agg('sum').reset_index(name='sum')
        data1_profit['keuntungan Order Per Order'] = [x.strftime("%d") for x in data1_revenue[' tanggal order (DateOrders)']] 
        data2_profit = df_data2['keuntungan Order Per Order'].groupby(df_data2[' tanggal order (DateOrders)'].dt.date).agg('sum').reset_index(name='sum')
        data2_profit['keuntungan Order Per Order'] = [x.strftime("%d") for x in data2_revenue[' tanggal order (DateOrders)']]               

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data1_sales_recap[' tanggal order (DateOrders)'], y=data1_sales_recap['Count'], fill='tozeroy', name=data1_name))
        fig.add_trace(go.Scatter(x=data2_sales_recap[' tanggal order (DateOrders)'], y=data2_sales_recap['Count'], fill='tozeroy', name=data2_name))
        fig.update_layout(width=600, height=200, margin=dict(l=0, r=0, b=20, t=30))
        fig.update_layout(title_text="Total sales "+segmentation_details, title_x=0, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="center",
            x=0.8
        ))
        fig.update_xaxes(title=xaxes_title)
        fig['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=data1_revenue['total Order Item'], y=data1_revenue['sum'], name=data1_name))
        fig2.add_trace(go.Scatter(x=data2_revenue['total Order Item'], y=data2_revenue['sum'], name=data2_name))
        fig2.update_layout(width=600, height=200, margin=dict(l=0, r=0, b=0, t=30), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), plot_bgcolor='rgba(255,255,255,0.01)')
        fig2.update_traces(mode='lines+markers', selector=dict(type='scatter'))
        fig2.update_layout(title_text="Total revenue "+segmentation_details, title_x=0, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
        fig2.update_layout(legend=dict(
            orientation="h",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=0.8
            ))
        fig2.update_xaxes(title=xaxes_title)
        fig2['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig2)

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=data1_profit['keuntungan Order Per Order'], y=data1_profit['sum'], name=data1_name, width=0.2))
        fig3.add_trace(go.Bar(x=data2_profit['keuntungan Order Per Order'], y=data2_profit['sum'], name=data2_name, width=0.2))
        fig3.update_layout(width=600, height=200, margin=dict(l=0, r=0, b=0, t=30), xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), plot_bgcolor='rgba(255,255,255,0.01)')
        fig3.update_traces(mode='lines+markers', selector=dict(type='scatter'))
        fig3.update_layout(title_text="Total profit "+segmentation_details, title_x=0, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), bargroupgap=0, bargap=0.45)
        fig3.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="center",
            x=0.8
            ))
        fig3.update_xaxes(title=xaxes_title)
        fig3['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig3)
        
    with col2:
        sales_sum1 = data1_sales_recap['Count'].sum()
        sales_sum2 = data2_sales_recap['Count'].sum()
        delta_sales_sum = sales_sum1-sales_sum2
        if delta_sales_sum >= 0:
            st.metric('Total Sales', "+ {:,.0f}".format(delta_sales_sum), "{:.2f} %".format(delta_sales_sum/sales_sum1*100))
        else:
            st.metric('Total Sales', "- {:,.0f}".format(abs(delta_sales_sum)), "{:.2f} %".format(delta_sales_sum/sales_sum1*100))

        profit_sum1 = df_data1['keuntungan Order Per Order'].sum()
        profit_sum2 = df_data2['keuntungan Order Per Order'].sum()
        delta_profit_sum = profit_sum1-profit_sum2
        if delta_profit_sum >= 0:
            st.metric('Total Profit', "+ ${:,.0f}".format(delta_profit_sum), "{:.2f} %".format(delta_profit_sum/profit_sum1*100))
        else:
            st.metric('Total Profit', "- ${:,.0f}".format(abs(delta_profit_sum)), "{:.2f} %".format(delta_profit_sum/profit_sum1*100))

        categories = df['Nama departemen'].unique()
        categories_sales1 = df_data1['Nama departemen'].value_counts().to_dict()
        categories_sales2 = df_data2['Nama departemen'].value_counts().to_dict()
        for x in categories:
            if x not in categories_sales1.keys():
                categories_sales1[x] = 0
            if x not in categories_sales2.keys():
                categories_sales2[x] = 0

        both_categories = pd.DataFrame({'data1':pd.Series(categories_sales1),'data2':pd.Series(categories_sales2)})
        both_categories['differences'] = (both_categories['data1'] - both_categories['data2'])/both_categories['data1']

        fig4 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                    shared_yaxes=True, vertical_spacing=0, horizontal_spacing = 0)

        fig4.append_trace(go.Bar(
            x=list(categories_sales1.values()),
            y=list(categories_sales1.keys()),
            orientation='h',
            name=data1_name
        ), 1, 1)

        fig4.append_trace(go.Bar(
            x=list(categories_sales2.values()), 
            y=list(categories_sales2.keys()),
            orientation='h',
            name=data2_name
        ), 1, 2)
        if option == 'year':
            fig4.update_layout(
                xaxis_range=[25000,0],
                xaxis2_range=[0,25000]
            )
        else:
            fig4.update_layout(
                xaxis_range=[2100,0],
                xaxis2_range=[0,2100]
            )
        fig4.update_layout(
            yaxis={"autorange": "reversed"}
        )
        fig4.update_layout(title_text="Categories sales count comparison", title_x=0)
        fig4.update_layout(width=600, height=400, margin=dict(l=0, r=0, b=0, t=50), xaxis=dict(showgrid=False), xaxis2=dict(showgrid=False), plot_bgcolor='rgba(255,255,255,0.01)')
        fig4.update_traces(texttemplate="%{x}", textposition="auto")
        fig4.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="center",
            x=0.8
            ))
        fig4['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig4)

    with col3:
        sales_revenue1 = data1_revenue['sum'].sum()
        sales_revenue2 = data2_revenue['sum'].sum()
        delta_sales_revenue = sales_revenue1-sales_revenue2
        if delta_sales_revenue >= 0:
            st.metric('Total Revenue', "+ ${:,.0f}".format(delta_sales_revenue), "{:.2f} %".format(delta_sales_revenue/sales_revenue1*100))
        else:
            st.metric('Total Revenue', "- ${:,.0f}".format(abs(delta_sales_revenue)), "{:.2f} %".format(delta_sales_revenue/sales_revenue1*100))

        avg_profit_perorder1 = df_data1['keuntungan Order Per Order'].mean()
        avg_profit_perorder2 = df_data2['keuntungan Order Per Order'].mean()
        delta_sales_avg_profit = avg_profit_perorder1-avg_profit_perorder2
        if delta_sales_avg_profit >= 0:
            st.metric('Average profit perorder', "+ ${:,.2f}".format(delta_sales_avg_profit), "{:.2f} %".format(delta_sales_avg_profit/avg_profit_perorder1*100))
        else:
            st.metric('Average profit perorder', "- ${:,.2f}".format(abs(delta_sales_avg_profit)), "{:.2f} %".format(delta_sales_avg_profit/avg_profit_perorder1*100))

    with col4:
        unique_customer1 = len(df_data1['ID pelanggan'].unique())
        unique_customer2 = len(df_data2['ID pelanggan'].unique())
        delta_unique_customer = unique_customer1-unique_customer2
        if delta_unique_customer > 0:
            st.metric('Unique Customer', "+ {:,.0f}".format(delta_unique_customer), "{:.2f} %".format(delta_unique_customer/unique_customer1*100))
        else:
            st.metric('Unique Customer', "- {:,.0f}".format(abs(delta_unique_customer)), "{:.2f} %".format(delta_unique_customer/unique_customer1*100))
