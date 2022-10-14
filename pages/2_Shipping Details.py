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
    st.markdown('<p class="big-font">SHIPPING DETAILS</p>', unsafe_allow_html=True)
    option = st.selectbox('Select data to display', years, index=0)
    st.write('You selected ', option)
    st.write("")

container2 = st.container()

with container2:
    if option == 'Total':
        df_year = df
    else:
        df_year = df[(df[' tanggal order (DateOrders)'] >= str(option)+'-01-01') & (df[' tanggal order (DateOrders)'] < str(option+1)+'-01-01')]
    
    df_year['day late'] = df_year['Lama Pengiriman (real)'] - df_year['Lama Pengiriman (jadwal)']
    col1, col2, col3 = st.columns(3)
    delivery_details = df_year['Status terkirim'].value_counts()
    lateness_percentage = len(df_year['Negara order'].loc[df_year['Risiko keterlambatan pengiriman'] == 1])/len(df_year)*100
    canceled_shipping = delivery_details[3]/len(df_year)*100
    average_lateness = df_year.loc[(df_year['day late'] > 0) & (df_year['Status terkirim'] == 'Late delivery'), 'day late'].mean()
    with col1:
        st.markdown('<p class="big-font">{:,.1f} %</p>'.format(lateness_percentage), unsafe_allow_html=True)
        st.markdown('<p class="medium-font">Shipping Late</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="big-font">{:,.1f} %</p>'.format(canceled_shipping), unsafe_allow_html=True)
        st.markdown('<p class="medium-font">Shipping Canceled</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="big-font">{:,.1f} days</p>'.format(average_lateness), unsafe_allow_html=True)
        st.markdown('<p class="medium-font">Average Lateness</p>', unsafe_allow_html=True)

container3 = st.container()

with container3:
    st.markdown("#")
    late_country_rank = df_year['Negara order'].loc[df_year['Risiko keterlambatan pengiriman'] == 1].value_counts(normalize=True)[:20]*100
    fig = px.bar(late_country_rank, width=1200, height=550, text=late_country_rank.values)
    fig.update_layout(title_text="Top 20 Country with Shipping Problems", title_x=0.5, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                    plot_bgcolor='rgba(255,255,255,0)')
    fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
    fig['layout']['title']['font'] = dict(size=20)
    fig.update_traces(texttemplate='%{text:.2f} %',textposition='outside')
    fig.update_xaxes(type='category')
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title='')
    fig.update_xaxes(title='')
    fig.update_xaxes(tickangle=330)
    st.plotly_chart(fig)   

container4 = st.container()

with container4:
    col1, col2 = st.columns(2)
    with col1:
        ship_mode_late = df_year['Shipping Mode'].loc[df_year['Risiko keterlambatan pengiriman'] == 1].value_counts()
        fig2 = px.pie(ship_mode_late, names=ship_mode_late.index, values=ship_mode_late.values, height=550, width=575)
        fig2.update_traces(textfont_size=20)
        fig2.update_layout(margin={"l":0})
        fig2.update_layout(title_text="Shipping Late by Mode", title_x=0.5)
        fig2['layout']['title']['font'] = dict(size=20)
        st.plotly_chart(fig2) 
    with col2:
        date_lateness = df_year['Risiko keterlambatan pengiriman'].groupby(df_year['shipping date (DateOrders)'].dt.day).mean()
        fig3 = px.line(date_lateness, width=600, height=250)
        fig3.update_layout(margin={"l":0, "b":0}, yaxis_tickformat = '.0%')
        fig3.update_layout(title_text="Shipping Lateness Rate", title_x=0.5, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        plot_bgcolor='rgba(255,255,255,0)')
        fig3.update_yaxes(title='')
        fig3.update_xaxes(title='By Date')
        fig3.update_xaxes(type='category')
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3) 

        month_lateness = df_year['Risiko keterlambatan pengiriman'].groupby(df_year['shipping date (DateOrders)'].dt.month).mean()
        month_lateness.index = pd.to_datetime(month_lateness.index, format="%m").month_name()
        fig4 = px.line(month_lateness, width=600, height=250)
        fig4.update_layout(margin={"l":0, "t":0}, yaxis_tickformat = '.0%')
        fig4.update_layout(title_text="", title_x=0.5, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                        plot_bgcolor='rgba(255,255,255,0)')
        fig4.update_yaxes(title='')
        fig4.update_xaxes(title='By Month')
        fig4.update_xaxes(type='category')
        fig4.update_xaxes(tickangle=330)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4) 

    
