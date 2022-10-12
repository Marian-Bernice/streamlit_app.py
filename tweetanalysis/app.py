import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image
from collections import Counter

# Set page to wide
st.set_page_config(layout='wide')

st.title('#QueensFuneral Tweet Analytics :bird:')

# change font
streamlit_style = """<style>
			@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100&display=swap');
			html, body, [class*="css"]  { font-family: 'Montserrat', sans-serif; } </style>"""
st.markdown(streamlit_style, unsafe_allow_html=True)

# CSS file
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Data
tweets = pd.read_excel('#QueensFuneral Tweets Dataset.xlsx')

sentiments = pd.DataFrame(tweets.groupby('Overall Sentiment')['#'].count())
sentiments = sentiments.reset_index(level=0)

dateCount = pd.DataFrame(tweets.groupby('Date Posted')['#'].count())
dateCount = dateCount.reset_index(level=0)

ordered_tweets = tweets.sort_values('Retweets', ascending=False)
ordered_tweets = ordered_tweets.head(5)

# Top 20 words in the dataset
tweets['temp'] = tweets['Post Text'].apply(lambda x : str(x).split())
x = tuple(tweets['temp'])
counts = Counter(item for sublist in x for item in sublist)
top20 = pd.DataFrame(counts.most_common(20))
top20.columns = ['Common words', 'Count']

# Stop words
N = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 
     'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 
     'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 
     'who', 'ass', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 
     'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 
     'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 
     'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 
     'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 
     'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 
     'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 
     'further', 'was', 'here', 'than', 'the',"it's", 'and', 'it.', 'rt']

def stopwords_remover(x):
    return [word for word in x if word.lower() not in N]

# removal of stopwords
tweets['temp'] = tweets['temp'].apply(lambda x: stopwords_remover(x))
x1 = tuple(tweets['temp'])
counts1 = Counter(item.lower().strip() for sublist in x1 for item in sublist)
top20w = pd.DataFrame(counts1.most_common(20))
top20w.columns = ['Common words', 'Count']

# positive words
positives = tweets[tweets['Overall Sentiment'] == 'Positive']
x2 = tuple(positives['temp'])
counts2 = Counter(item.lower().strip() for sublist in x2 for item in sublist)
top20p = pd.DataFrame(counts2.most_common(20))
top20p.columns = ['Common words', 'Count']

# negative words
negatives = tweets[tweets['Overall Sentiment'] == 'Negative']
x3 = tuple(negatives['temp'])
counts3 = Counter(item.lower().strip() for sublist in x3 for item in sublist)
top20n = pd.DataFrame(counts3.most_common(20))
top20n.columns = ['Common words', 'Count']

# View
# Sidebar
st.sidebar.image(Image.open('Government-Digital-Service-logo.png'), width= 150)
st.sidebar.markdown("**Use this dashboard for tweet analytics #QueensFuneral**")
st.sidebar.header("Menu")
dataset_name = st.sidebar.selectbox(
    'Select a Metric for analysis',
    ('Sentiments', 'Date Posted', 'Common Words')
)


# Row A
# Split Page
a1, a2, a3 = st.columns(3)
a1.metric("Total Tweets", tweets.shape[0])
a2.metric("Average number of Retweets", round(tweets['Retweets'].mean(),2))
a3.metric("General Feeling", "Neutral")
st.markdown('''
<style>
/*center metric label*/
[data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
    padding: 3% 3% 3% 3%;

}

/*center metric value*/
[data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
    padding: 3% 3% 3% 3%;

}
</style>
''', unsafe_allow_html=True)

# Row B
st.write(f"## Analysis by {dataset_name} ")

if 'Sentiments' in dataset_name:
    st.caption('''Here, you can see the total number of sentiments, categorized into Positive, Negative and Neutral for all tweets with the hashtag #QueensFuneral. 
    It gives a general depiction of how tweeters felt about the Queens Passing''')
    hist1 = px.histogram(sentiments, x='Overall Sentiment', y='#', hover_data=['#'], height=300, color="Overall Sentiment",
            color_discrete_map={"Negative":"lightgreen", "Neutral":"#00CCFF", "Positive":"#FFFF00"})
    st.plotly_chart(hist1, use_container_width=True)
elif 'Date Posted' in dataset_name:
    st.caption('''Here, you can see the number of tweets recorded per day with the hashtag #QueensFuneral. 
    ''')
    hist2 = px.histogram(dateCount, x='Date Posted', y='#', hover_data=['#'], height=300, color_discrete_sequence=["#00CCFF"])
    st.plotly_chart(hist2, use_container_width=True)

    st.write(f"## Analysis of Ordered tweets by the Day ")
    st.caption('''Here, you can see the days with the most tweets and retweets with the hashtag #QueensFuneral, ordered in ascending order. 
    ''')
    hist3 = px.histogram(ordered_tweets, x='Date Posted', y='#', hover_data=['#'], height=300, color_discrete_sequence=["#00CCFF"])
    st.plotly_chart(hist3, use_container_width=True)
else:
    # Top 20 words found in the dataset
    st.caption('''Here, you can see the top 20 common words found in the #QueensFuneral tweets. 
    ''')
    st.table(top20)

    st.write("## Breakdown into Positive & Negative Sentiments ")
    st.caption('''Here, we take out words that are most common in tweets but make no contribution to sentiment - termed STOP WORDS.
                It gives the 20 most common words that are either positive or negative.
    ''')

    # Split page
    b1, b2 = st.columns(2)
    # positive   
    b1.write("**Words in POSITIVE sentiment**")
    b1.bar_chart(top20p, x='Common words', y='Count', use_container_width=True)

    # negative
    b2.write("**Words in NEGATIVE sentiment** ")
    b2.bar_chart(top20n, x='Common words', y='Count', use_container_width=True)
