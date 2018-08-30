import requests
from datetime import datetime
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as SIA
import re

#base query url
#maximum size is 1000, increasing will not change number of comments returned
#score threshold set to greater than 1 to avoid problems with normalizing sentiment
base_url = "https://api.pushshift.io/reddit/search/comment/" + \
            "?q={}&" + \
            "{}" + \
            "after={}&" + \
            "before={}&" + \
            "score=>1&" + \
            "sort_type=score&" + \
            "sort=desc&" + \
            "size=1000"

analyzer = SIA()

KEYWORD = "musk"
SUBREDDITS = ["all", "politics", "the_donald", "space"]

#formats the desired subreddits to match REST query
def format_subreddit(sub):
    if sub == "all":
        return ""
    return "subreddit={}&".format(sub)

#converts unix time to string
def utc_to_str(utc_time):
    utc_time = int(utc_time)
    return datetime.utcfromtimestamp(utc_time).strftime('%Y/%m/%d')

#returns sentiment normalized by the posts score
def get_normalized_sentiment(comments):
    if len(comments) < 10:
        return 0 #ignore weeks with less than 10 mentions
    total_score, total_sent = 0, 0
    for comment in comments:
        body = comment.get('body', '')
        score = comment.get('score', 1)
        total_score += score
        total_sent += analyzer.polarity_scores(body)['compound'] * score

    #Normalized sentiment formula: total_sentiment / (total_comments * total_score)
    normalized_sentiment = total_sent / (len(comments) or 1) / (total_score or 1)
    return normalized_sentiment

#makes appropriate headers for given subreddits
def make_header(subreddits):
    header = ["Date"]
    header += ["/r/{}".format(sub) for sub in subreddits]
    return header

#appends a moving average of the indicated column to the data-
def add_moving_average(full_data, column, period = 10):
    header = full_data[0]
    move_av_head = "{} moving average".format(header[column])
    header.append(move_av_head)

    curr_vals = []
    for row in range(1, len(full_data)):
        curr_row = full_data[row]
        curr_vals.append(curr_row[column])
        average = sum(curr_vals) / min(row, period)
        curr_row.append(average)
        if len(curr_vals) >= period:
            curr_vals.pop(0)

if __name__ == "__main__":
    sub_queries = list(map(format_subreddit, SUBREDDITS))
    start_time = 1451635200 #01/01/16, 8 AM GMT

    #04/05/18 pushshift API scores become inaccurate
    max_time = int(datetime(2018, 4, 5).strftime("%s"))
    increment = 7 * 24 * 60 * 60 #Increment in 1 week intervals

    header = make_header(SUBREDDITS)
    full_data = [header]
    while start_time < max_time:
        curr_row = [utc_to_str(start_time)]
        print("Querying the week of {}".format(utc_to_str(start_time)))
        for subreddit in sub_queries:
            end_time = start_time + increment
            curr_url = base_url.format(KEYWORD, subreddit, start_time, end_time)
            print(curr_url)
            comments = requests.get(curr_url).json()['data']
            curr_row.append(get_normalized_sentiment(comments))
        full_data.append(curr_row)
        start_time = end_time

    for col in range(1, len(sub_queries) + 1):
        add_moving_average(full_data, col)

    fname = "output/{}_sentiment.csv".format(KEYWORD)
    with open(fname, "wt") as f:
        writer = csv.writer(f)
        for row in full_data:
            writer.writerow(row)
