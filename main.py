import streamlit as st
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns

consumerKey ="U3GdWYpVcBmg7IL3kUrxSaLky"
consumerSecret = "8EUzEQUu5nYTUUZ3g4dXoyoW4qlSRtg36KjmSGSlHQL1TtzFfW"
accessToken ="714172280876568576-su24ZlJYRp3nGDO4MyFr96NwewFqvCN"
accessTokenSecret ="KInundM39JZjkOAs4YMffWXNZiwQ5fWwUfsV9bKwgcvp5"

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumerKey, consumerSecret)

# Set the access token and access token secret
authenticate.set_access_token(accessToken, accessTokenSecret)

# Creating the API object while passing in auth information
api = tweepy.API(authenticate, wait_on_rate_limit=True)



def app():
    st.image("https://1000logos.net/wp-content/uploads/2021/04/Twitter-logo.png",width=100)
    st.title("Welcome to Twitter Data Analysis Portal ")

    activities=["Specific User" , "Specific Keyword"]
    choice=st.sidebar.selectbox("Analysis of ",activities)

    if choice=="Specific User":
        raw_text = st.text_area("Enter your Search : (twitter handle without @)")

        Analyzer_choice = st.selectbox("Select the Activities", ["Recent Tweets", "Visualize the Sentiment Analysis"])

        if st.button("Analyze"):

            if Analyzer_choice == "Recent Tweets":

                st.success("Fetching last 5 Tweets")

                def Recent_Tweets(raw_text):

                    # Extract 100 tweets from the twitter user
                    posts = api.user_timeline(screen_name=raw_text, count=100, lang="en", tweet_mode="extended")

                    def get_tweets():
                        l = []
                        i = 1
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i = i + 1
                        return l

                    recent_tweets = get_tweets()
                    return recent_tweets

                recent_tweets = Recent_Tweets(raw_text)

                st.write(recent_tweets)

            else:

                def Plot_Analysis():

                    st.success("Generating Visualisation for Sentiment Analysis")

                    posts = api.user_timeline(screen_name=raw_text, count=100, lang="en", tweet_mode="extended")

                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

                    # Create a function to clean the tweets
                    def cleanTxt(text):
                        text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
                        text = re.sub('#', '', text)  # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text)  # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink

                        return text

                    # Clean the tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)

                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity

                   # Create a function to get the polarity
                    def getPolarity(text):
                        return TextBlob(text).sentiment.polarity

                    # Create two new columns 'Subjectivity' & 'Polarity'
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)

                    def getAnalysis(score):
                        if score < 0:
                            return 'Negative'
                        elif score == 0:
                            return 'Neutral'
                        else:
                            return 'Positive'

                    df['Analysis'] = df['Polarity'].apply(getAnalysis)

                    return df

                df = Plot_Analysis()

                st.write(sns.countplot(x=df["Analysis"], data=df))

                st.pyplot(use_container_width=True)

    else:
        raw_text = st.text_area("Enter your Search : ( Keyword )")

        Analyzer_choice = st.selectbox("Select the Activities", ["Recent Tweets", "Visualize the Sentiment Analysis"])

        if st.button("Analyze"):

            if Analyzer_choice == "Recent Tweets":

                st.success("Fetching last 5 Tweets")

                def Recent_Tweets(raw_text):

                    # Extract 100 tweets from the twitter user
                    posts = api.search(q=raw_text, lang="en" , tweet_mode="extended")

                    def get_tweets():
                        l = []
                        i = 1
                        for tweet in posts[:5]:
                            l.append(tweet.full_text)
                            i = i + 1
                        return l

                    recent_tweets = get_tweets()
                    return recent_tweets

                recent_tweets = Recent_Tweets(raw_text)

                st.write(recent_tweets)

            else:

                def Plot_Analysis():

                    st.success("Generating Visualisation for Sentiment Analysis")

                    posts = api.search(q=raw_text, lang="en", tweet_mode="extended")

                    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

                    # Create a function to clean the tweets
                    def cleanTxt(text):
                        text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
                        text = re.sub('#', '', text)  # Removing '#' hash tag
                        text = re.sub('RT[\s]+', '', text)  # Removing RT
                        text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink

                        return text

                    # Clean the tweets
                    df['Tweets'] = df['Tweets'].apply(cleanTxt)

                    def getSubjectivity(text):
                        return TextBlob(text).sentiment.subjectivity

                   # Create a function to get the polarity
                    def getPolarity(text):
                        return TextBlob(text).sentiment.polarity

                    # Create two new columns 'Subjectivity' & 'Polarity'
                    df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
                    df['Polarity'] = df['Tweets'].apply(getPolarity)

                    def getAnalysis(score):
                        if score < 0:
                            return 'Negative'
                        elif score == 0:
                            return 'Neutral'
                        else:
                            return 'Positive'

                    df['Analysis'] = df['Polarity'].apply(getAnalysis)

                    return df

                df = Plot_Analysis()

                st.write(sns.countplot(x=df["Analysis"], data=df))

                st.pyplot(use_container_width=True)

st.set_option('deprecation.showPyplotGlobalUse', False)
if __name__ == "__main__":
    app()
