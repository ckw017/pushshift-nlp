#!/bin/python3
import re
import csv
import requests
import nltk
from datetime import datetime
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

TOPIC = "musk"
SUBREDDITS = ["", "cars", "space", "futurology", "wallstreetbets", "politics"]
FILTER = [TOPIC, "elon"] #Filter out "obviously" related words, for example "elon" when analyzing "musk"
N_QUERIES = 10 #Number of queries. Note that each query returns to 1000 comments
MATCH_COUNTS = 20 #The number of keywords per call to get_common


#Format order: Query, Score threshold, subreddit (if any)
#Maximum query size is 1000, increasing past 1000 will not give more data
base_url = "https://api.pushshift.io/reddit/search/comment/" + \
            "?q={}&" + \
            "score=<{}&" + \
            "sort_type=score&" + \
            "sort=desc&" + \
            "{}" + \
            "size=1000"

lemmatizer = WordNetLemmatizer()

#Common words/typos that are generally unrelated to keyword in question
stop_words = set(["im", "hes", "shes", "someone", "anyone", "everyone", "thing", "things", "lot", "youre", "with", "but", "as", "have", "not", "like", "its", "way", "at", "if", "time", "we", "will", "so", "all", "about", "just", "from", "an", "people", "what", "has", "it", "for", "on", "be", "the", "to", "and", "of", "is", "are", "was", "a", "that", "this", "i", "in", "you", "or", "they", "his", "her", "he", "she", "on" "it", "something", "way"])
stop_words.update(stopwords.words("english"))
stop_words.update(FILTER)
#Merge with nltk's stopword corpus

#Returns the {count} most common words associated with the topic
#normalize subtracts universally common words to focus on relations unique to the given subreddit
def get_common(topic, subreddit, count, normalize = Counter()):
    counter = Counter()
    sub_query = "subreddit={}&".format(subreddit) if subreddit else ""
    max_score = 1000000000 #1 magnitude higher than current top scoring submission
    for i in range(N_QUERIES):
        curr_url = base_url.format(topic, max_score, sub_query)
        print("Query {}: ".format(i), curr_url)
        comments = requests.get(curr_url).json()["data"]

        #End process after running out of data to query
        if not comments:
            break

        for comment in comments:
            keywords = filter_body(comment)
            for kw in keywords:
                kw = lemmatizer.lemmatize(kw)
                counter[kw] += 1
        #Next query should find all comments less than or equal to lowest scored comment of this query
        max_score = int(comments[-1]["score"])
    counter -= normalize
    return counter

#lemmatizes and filters the body of the comment
def filter_body(comment):
    body = comment.get("body", "")
    body = nltk.word_tokenize(body)
    tagged = nltk.pos_tag(body)

    #include only nouns
    tagged = filter(lambda w: 'NN' in w[1], tagged)
    tagged = [entry[0] for entry in tagged]

    #remove stopwords
    filtered = filter(lambda w: w not in stop_words, tagged)
    return filtered

def counter_to_row(row_name, counter):
    common = counter.most_common(MATCH_COUNTS)
    row = [subreddit or "all"]\
    #Entry format: (keyword, count)
    row += [entry[0] + " ({})".format(entry[1]) for entry in common] #Converts each entry to format "key_word (count)"
    return row

if __name__ == "__main__":
    normalize = Counter()
    fname = "output/{}_keywords.csv".format(TOPIC) #default file name, eg "musk_keywords.csv"
    with open(fname, "wt") as f:
        writer = csv.writer(f)
        for subreddit in SUBREDDITS:
            result = get_common(TOPIC, subreddit, N_QUERIES, normalize)
            if not subreddit:
                normalize = result
            row = counter_to_row(subreddit, result)
            print(row)
            writer.writerow(row)
