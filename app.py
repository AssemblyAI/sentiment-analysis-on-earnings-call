import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# load json data
response = open('./json/response.json')
data = json.load(response)
sar = data['sentiment_analysis_results']
# save sentiment data to dataframe for ease of visualization
sen_df = pd.DataFrame(sar)

## body
st.title('Sentiment Analysis of an Earnings Call')
st.subheader('Analyze the sentiment of an earnings call using AssemblyAI.')
st.video('https://youtu.be/UA-ISgpgGsk')

# sidebar
st.sidebar.header('Transcript of the call')
st.sidebar.markdown(data['text'])

st.header('Amazon Earnings Call Q3 2021')

## Visualizations
st.markdown('### Number of Sentences: ' + str(sen_df.shape[0]))

grouped = pd.DataFrame(sen_df['sentiment'].value_counts()).reset_index()
grouped.columns = ['sentiment','count']
col1, col2 = st.columns(2)

# Display number of positive, negative, and neutral sentiments
fig = px.bar(grouped, x='sentiment', y='count', color='sentiment', color_discrete_map={'NEGATIVE':'firebrick','NEUTRAL':'navajowhite','POSITIVE':'darkgreen'})

fig.update_layout(
	showlegend=False,
    autosize=False,
    width=400,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    )
)

col1.plotly_chart(fig)

## Display sentiment score
pos_perc = grouped[grouped['sentiment']=='POSITIVE']['count'].iloc[0]*100/sen_df.shape[0]
neg_perc = grouped[grouped['sentiment']=='NEGATIVE']['count'].iloc[0]*100/sen_df.shape[0]
neu_perc = grouped[grouped['sentiment']=='NEUTRAL']['count'].iloc[0]*100/sen_df.shape[0]

sentiment_score = neu_perc+pos_perc-neg_perc

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode = 'delta',
    value = sentiment_score,
    domain = {'row': 1, 'column': 1}))

fig.update_layout(
	template = {'data' : {'indicator': [{
        'title': {'text': 'Sentiment Score'},
        'mode' : 'number+delta+gauge',
        'delta' : {'reference': 50}}]
                         }},
    autosize=False,
    width=400,
    height=500,
    margin=dict(
        l=20,
        r=50,
        b=50,
        pad=4
    )
)

col2.plotly_chart(fig)

## Display sentence location of sentiments
fig = px.scatter(sar, y='sentiment', color='sentiment', size='confidence', hover_data=['text'], color_discrete_map={'NEGATIVE':'firebrick','NEUTRAL':'navajowhite','POSITIVE':'darkgreen'})

fig.update_layout(
    title="Location of Sentiments",
	showlegend=False,
    autosize=False,
    width=800,
    height=300,
    margin=dict(
        l=50,
        r=50,
        b=50,
        t=50,
        pad=4
    )
)

st.plotly_chart(fig)
