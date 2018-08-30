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

The following is based on the keyword "berkeley"


| all               | politics          | the_donald      | applyingtocollege | science          | 
|-------------------|-------------------|-----------------|-------------------|------------------| 
| student (2600)    | violence (456)    | trump (278)     | cs (437)          | emission (57)    | 
| year (2279)       | wage (446)        | riot (196)      | gpa (353)         | gene (51)        | 
| city (1441)       | trump (297)       | police (181)    | cornell (253)     | co2 (43)         | 
| state (1372)      | speech (274)      | pd (170)        | admission (238)   | hominid (32)     | 
| college (1366)    | policy (197)      | battle (156)    | score (217)       | evolution (21)   | 
| day (1179)        | antifa (182)      | antifa (149)    | engineering (214) | carbon (20)      | 
| speech (1161)     | nazi (164)        | rally (140)     | ivy (203)         | greenhouse (17)  | 
| police (1130)     | rally (158)       | bamn (132)      | acceptance (195)  | dioxide (17)     | 
| gt (1101)         | domain (153)      | supporter (108) | ucla (179)        | forcing (15)     | 
| group (1080)      | government (148)  | pes (83)        | stats (167)       | dna (15)         | 
| california (1077) | economist (148)   | maga (83)       | regent (164)      | muller (15)      | 
| trump (1003)      | supremacist (138) | soros (78)      | application (157) | trait (15)       | 
| job (973)         | tax (137)         | cucks (75)      | reach (150)       | biology (14)     | 
| system (961)      | economy (135)     | democrat (70)   | essay (145)       | specie (13)      | 
| class (955)       | president (133)   | patriot (64)    | mit (145)         | intensity (13)   | 
| place (951)       | increase (133)    | cnn (61)        | applicant (143)   | emeritus (13)    | 
| right (932)       | right (127)       | flag (51)       | cmu (143)         | disease (12)     | 
| point (919)       | coulter (125)     | chief (49)      | caltech (142)     | temperature (12) | 
| campus (918)      | left (123)        | commie (49)     | stanford (128)    | chemist (12)     | 
| guy (905)         | protester (116)   | yvette (44)     | ec (125)          | protein (11)     | 
