# python-reddit-crawler

# Requirements
python3
flask
sqlite3

# Usage
./crawlerapp.py [number_of_pages]

It will run get all the submissions data from the [number_of_pages] specified and store them in an SQLite DB
After first iteration, it will set up a Rest API at localhost:5000

# API methods
* /api/v1.0/update [GET]
It updates the submissions of the current N pages

* /api/v1.0/top/comments [GET]
 It returns the top 10 submissions by comment

* /api/v1.0/top/comments/external [GET]
 It returns the top 10 external submissions by comment

* /api/v1.0/top/comments/internal [GET]
 It returns the top 10 internal submissions by comment

* /api/v1.0/top/score [GET]
 It returns the top 10 submissions by score

* /api/v1.0/top/score/external [GET]
 It returns the top 10 external submissions by score

* /api/v1.0/top/score/internal [GET]
 It returns the top 10 internal submissions by score
