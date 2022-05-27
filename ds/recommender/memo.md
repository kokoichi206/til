## MEMO
- Be hands-on! Write your own code.
- Just do an experiment
- Machine Learning is Math and Programming
- Take Notes
    - take handwritten notes is better
    - Build the mind-muscle connection
- Explore-Exploit Dilemma
    - How do we strike a balance between these 2 opposing forces?


## Non-personalized recommenders
Amazon, youtube...

superviced learning can be used for recommendatioins


## How to recommend?
- Simple: just sort by average rating
- Use confidence intervals
- What if X is not normally-distributed?
    - No problem! CLT
- Bernoulli CI
    - 0 to 1
    - upvote and downvote situation
    - Wilson Interval is better!
        - difficult...

## Bayesian Ranking
- Sort by lower confidence bound?
- Sorting by fixed numbers just doesn't seem quite right
- Automatically balances need to explore and exploit
    - **random sampling using current probability**


## Links
- [code(github)](https://github.com/lazyprogrammer/machine_learning_examples/tree/master/recommenders)
- [MovieLens 20M Dataset](https://www.kaggle.com/datasets/grouplens/movielens-20m-dataset)
- [How Hacker News ranking really works: scoring, controversy, and penalties](http://www.righto.com/2013/11/how-hacker-news-ranking-really-works.html)



## English
- Python code is python code no matter where it is.
- Sit back and relax
- Don't I own my site?
