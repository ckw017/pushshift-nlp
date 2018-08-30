# pushshift-nlp
Tools built from Python's Natural Language Toolkit to track trends in reddit comments through the pushshift API.

**Note**: Because of problems with the pushshift API, all comment scores after ~April 5th, 2018 are inaccurate. Because of this, data depending on the scoring threshold past that date is not used.

## keyword_sentiment
Tracks the weekly composite sentiment score for all comments mentioning the given keyword. Gives the option to stratify by subreddit, and output data with rolling averages.

The following graphs are based on weekly comments containing the keyword "musk"
![](https://s8.postimg.cc/edl1xuv0z/Sentiment_vs_Time.png)
![](https://s8.postimg.cc/xvfpdsk8z/Sentiment_vs_Time_10_Week_Rolling_Average.png)

## related_words
Tracks most common words associated with a given keyword in reddit comments. Processes comments in batches of 1000, in descending order of score. Just like with keyword_sentiment, the output can be stratified by subreddit.
