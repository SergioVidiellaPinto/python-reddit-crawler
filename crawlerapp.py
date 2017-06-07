#!/usr/bin/env python3

from flask import Flask
from flask import jsonify
from src.redditcrawler import PythonRedditCrawler
import sys

# Get a sequence from command line
if sys.argv[1]:
    deep = int(sys.argv[1])
else:
    depp = 1

app = Flask(__name__)
crawler = PythonRedditCrawler(deep)

@app.route('/api/v1.0/update', methods=['GET'])
def update_submissions():
    crawler.crawl()
    return jsonify({'result': 'ok'})

@app.route('/api/v1.0/top/score', methods=['GET'])
def get_submissions_by_top_score():
    submissions = crawler.get_top_submissions_by_score()
    return jsonify({'submissions': submissions})

@app.route('/api/v1.0/top/score/external', methods=['GET'])
def get_submissions_by_top_score_external():
    submissions = crawler.get_top_submissions_by_score_external()
    return jsonify({'submissions': submissions})

@app.route('/api/v1.0/top/score/internal', methods=['GET'])
def get_submissions_by_top_score_internal():
    submissions = crawler.get_top_submissions_by_score_internal()
    return jsonify({'submissions': submissions})

@app.route('/api/v1.0/top/comments', methods=['GET'])
def get_submissions_by_top_comments():
    submissions = crawler.get_top_submissions_by_comments()
    return jsonify({'submissions': submissions})

@app.route('/api/v1.0/top/comments/external', methods=['GET'])
def get_submissions_by_top_comments_external():
    submissions = crawler.get_top_submissions_by_comments_external()
    return jsonify({'submissions': submissions})

@app.route('/api/v1.0/top/comments/internal', methods=['GET'])
def get_submissions_by_top_comments_internal():
    submissions = crawler.get_top_submissions_by_comments_internal()
    return jsonify({'submissions': submissions})


if __name__ == '__main__':
    crawler.crawl()
    app.run(debug=True)
