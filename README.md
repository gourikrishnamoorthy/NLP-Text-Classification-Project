# NLP Text Classification Project

1. Using [Pushshift's](https://github.com/pushshift/api) API, collect posts from r/Creation, r/evolution and r/DebateEvolution.
2. Then use NLP to train a classifier on which subreddit a given post came from. This is a binary classification problem.

## Problem Statement

To allow users/moderators to classify posts on various channels based on their preferences
E.g. A science moderator may want to keep the conversation focus on the science side where as a Creationist moderator may want to keep the conversation focus on the creationist side

### Steps

* Download recent `1000` posts from `r/evolution`  and set the `Target value` as `0` 
* Download recent `1000` posts from `r/Creation`   and set the `Target value` as `1`
* Study the posts from both the subreddits. Combine comments to increase the data set.
* Combine both the posts as one data set. Then allot `70%` as `train data` set and `30%` as test.
* EDA - using different data visualizations
* Use NLP to tokenize, process (lemmatize/stemming/stopwords) and extract meaningful words to define a `quanitative language pattern shape` from both the posts. This will enable a model to predict which post came from which reddit.
* Train a model to 1st predict 1 and 0 
* Use mutiple predictor model combinations to classify the data and choose the best estimator by evaluating each model using classifier metrics like accuracy , sensitivity , specificity , precision, mis calculation and roc acu 
* Download recent `1000` posts from DebateEvolution
* Use the best estimator to identify posts from DebateEvolution as `pro evolution` or `pro Creation & Intelligent Design`. This part is an `unsupervised prediction` to see if the model is able to `detect a language pattern`.
* Present findings

### Findings

##### Best model out of 8640 models


* Vectorizer : 
```
TfidfVectorizer()
```
* Parameters : 
```
5000 - max features
(1,3) -n_gram range
English - stopwords 
```

* Classifier:
```
LogisticRegressionCV():
```
* Parameters:
```
0.1 - C
500 - max iteration
12 - penalty
```

## Score
* Baseline score: .50
* CV Score : .81
* Train Score: .91
* Test Score:.82
* loss function (log loss): 6.54

## Columns used:
* Title
* Selftext
* Comment body



## Used the best model on the texts from r/DebateEvolution

* 1288 posts got classified as Creation posts
* 712 posts got classified as Evolution posts


* E.g. Evolution posts :    Programmed Cell Death Is Vital to Life, but Where'd It Come From?
* E.g Creation posts:       Giving Up Darwin

### Sentiment Intensity Analysis on all the subreddits

* More than 70% had a  neutral tone. 
* Less than 20% posts had a negative tone. 


### Next Steps

* Identify words/phrases commonly used by popular discussions from both the sides
* To find out if there is a way to flag a post if the words are leaning towards an abusive language 
* Identify key arguments used to refute evolution


## Presentation

* [Link](./Debate_Evolution.pdf) 
