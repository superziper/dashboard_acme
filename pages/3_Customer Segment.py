import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

container1 = st.container()
st.markdown("""<style>.big-font {font-size:70px !important;text-align: center;}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.medium-font {font-size:40px !important;text-align: center;}</style>""", unsafe_allow_html=True)
    
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

years = ['Total']+sorted(df[" tanggal order (DateOrders)"].dt.year.unique(),reverse=True)

with container1:
    st.markdown('<p class="big-font">CUSTOMER SEGMENT</p>', unsafe_allow_html=True)
    option = st.selectbox('Select data to display', years, index=0)
    st.write('You selected ', option)
    if option == 'Total':
        df_year = df
    else:
        df_year = df[(df[' tanggal order (DateOrders)'] >= str(option)+'-01-01') & (df[' tanggal order (DateOrders)'] < str(option+1)+'-01-01')]
    st.write("")
    
container2 = st.container()

with container2:
    col1, col2 = st.columns(2)
    with col1:
        customer_segment = df_year['Customer Segment'].value_counts()
        fig = px.pie(customer_segment, names=customer_segment.index, values=customer_segment.values, height=550, width=550, labels=customer_segment.index, hole=.3)
        fig.update_traces(textfont_size=20, textposition='inside', textinfo='percent+label')
        fig.update_layout(title_text="Customer type", title_x=0.5)
        fig['layout']['title']['font'] = dict(size=20)
        fig.update_layout(showlegend=False)
        fig.add_layout_image(
            dict(
                source="https://img.icons8.com/color/344/administrator-male-skin-type-3.png",
                xref="paper", yref="paper",
                x=0, y=0
            ))
        st.plotly_chart(fig) 

    with col2:
        payment_type = df_year['Tipe'].value_counts()
        fig2 = px.pie(payment_type, names=payment_type.index, values=payment_type.values, height=550, width=550, labels=payment_type.index, hole=.3)
        fig2.update_traces(textfont_size=20, textposition='inside', textinfo='percent+label')
        fig2.update_layout(title_text="Payment type", title_x=0.5)
        fig2['layout']['title']['font'] = dict(size=20)
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2) 

container3 = st.container()

with container3:
    col1, col2, col3, col4= st.columns([1, 1, 1, 3])
    with col1:
        unique_customer = df_year['ID pelanggan'].value_counts()
        st.write("Unique Customers")
        st.header("{:,.0f}".format(len(unique_customer)))
        avg_sales_perorder = df_year['total Order Item'].mean()
        st.write("Average sales per order")
        st.header("${:,.2f}".format(avg_sales_perorder))
    
    with col2:
        repeated_orders = len(unique_customer[unique_customer != 1])/len(unique_customer)*100
        st.write("Customers repeat order")
        st.header("{:,.2f}%".format(repeated_orders))
        avg_profit = df_year['rasio keuntungan Order Item'].mean()*100
        st.write("Average profit per order")
        st.header("{:,.2f}%".format(avg_profit))
        

    with col3:
        avg_repeated_order = unique_customer[unique_customer != 1].mean()
        st.write("Average repeated orders")
        st.header("{:,.0f}".format(avg_repeated_order))
        avg_discount = df_year['rata rata disko Order Item Diskon'].mean()*100
        st.write("Average discount used")
        st.header("{:,.2f}%".format(avg_discount))

    with col4:
        hourly_order = df_year[' tanggal order (DateOrders)'].groupby(df_year[' tanggal order (DateOrders)'].dt.hour).agg('count')
        fig3 = px.line(hourly_order, width=700, height=300, markers=True)
        graph_title = 'Order count hourly in ' + str(option)
        fig3.update_layout(showlegend=False)
        fig3.update_xaxes(type='category')
        fig3.update_layout(margin={"l":0, "t":20})
        fig3.update_yaxes(title='')
        fig3.update_xaxes(title='Hour')
        fig3.update_layout(title_text=graph_title, title_x=0.5, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), plot_bgcolor='rgba(255,255,255,0.05)')
        fig3['layout']['title']['font'] = dict(size=15)
        st.plotly_chart(fig3)

container4 = st.container()

with container4:
    col1, col2, col3 = st.columns([1, 1, 1.4])
    with col1:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        canceled_order = len(df_year['Status terkirim'].loc[df_year['Status terkirim'] == 'Shipping canceled'])/len(df_year['Status terkirim'])*100
        st.markdown('<p class="big-font">{:,.2f} %</p>'.format(canceled_order), unsafe_allow_html=True)
        st.markdown('<p class="medium-font">Order Canceled</p>', unsafe_allow_html=True)
    with col2:
        st.markdown("#")
        st.markdown("#")
        st.markdown("#")
        total_profit_canceled = df_year['keuntungan Order Per Order'].loc[df['Status terkirim'] == 'Shipping canceled'].sum()
        st.markdown('<p class="big-font">${:,.0f}</p>'.format(total_profit_canceled), unsafe_allow_html=True)
        st.markdown('<p class="medium-font">Total Profit Canceled</p>', unsafe_allow_html=True)
    with col3:
        status_canceled = (df_year['Order Status'].loc[df_year['Status terkirim'] == 'Shipping canceled']).value_counts()
        fig4 = px.pie(status_canceled, names=status_canceled.index, values=status_canceled.values, height=500, width=500, labels=status_canceled.index)
        fig4.update_traces(textfont_size=20, textposition='inside', textinfo='percent')
        fig4.update_layout(title_text="Cause of cancellation", title_x=0.25)
        fig4.update_layout(margin={"l":0})
        fig4['layout']['title']['font'] = dict(size=20)
        fig4.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ))
        st.plotly_chart(fig4) 
            

        



