#!/usr/bin/env python3

from urllib.parse import urlparse
from urllib import request
from bs4 import BeautifulSoup
from src.submissionDao import SubmissionDao

class PythonRedditCrawler(object):  
    def __init__(self, depth=2):
        """
        depth: How many pages will analyze
        """
        self.main_url = 'https://www.reddit.com/r/Python'
        self.depth = depth
        self.submissionDao = SubmissionDao()
        self.submissionDao.create_table()

    def crawl(self):
        u_parse = urlparse(self.main_url)
        self.domain = u_parse.netloc
        self.scheme = u_parse.scheme
        self._crawl_pages(self.main_url)

    def _crawl_pages(self, init_page):
        """
        Iteratively crawl the pages until the max depth
        """
        current_page = init_page
        for page_number in range(0, self.depth):
            next_page = self._crawl_page(current_page)
            current_page = next_page

    def _crawl_page(self, page):
        """
        From a given page URL crawl all the blog entries
        page: Url to analyze
        """
	# Prepare the request
        req = request.Request(page, headers={ 'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        response = request.urlopen(req)
        html_page = response.read().decode('ascii', 'ignore')

	# Parse the HTML with BeautifulSoup and obtain the submissions table (id='siteTable')
        soup = BeautifulSoup(html_page, 'html.parser')
        body = soup.find(id="siteTable")

        # Obtain the next page URL
        next_page = body.find("span", { "class" : "next-button" }).a.get('href')

        # Obtain the list of submissions of the page
        submissions_html = body.find_all("div", class_="thing")
        
        # Iterate over the list of submissions
        for submission_html in submissions_html:
            interest_data = dict()
            # Obtain the relevant data
            entry = submission_html.find("div", class_="entry")
            comments_section = entry.find("a", { "data-event-action" : "comments" })

            score =  submission_html.find("div", { "class" : "score unvoted" } ).text
            # If no score, a '•' will be informed. Turn it into a 0
            if score == '•':
                score = '0'

            external_url = entry.a.get('href')

            is_external = False
            # If the external URL starts with /r/Python add the reddit domain
            if external_url.startswith('/r/Python'):
                is_external = False
            else:
                is_external = True

            title = entry.a.text
            external_url = entry.a.get('href')
            discussion_url = comments_section.get('href')
            submitter = entry.find("a", class_="author").text
            number_of_comments = comments_section.text.split(' ')[0]
            if number_of_comments == "comment":
                number_of_comments = 0
            creation_date = entry.time.get("datetime")
            
            # Get all the information in a list in order to store it. The order is important, as it will be the order of the DB rows 
            submission = (title, is_external, external_url, discussion_url, submitter, number_of_comments, creation_date, score)
            self.submissionDao.add_or_update_submission(submission) 

        return next_page

    def get_top_submissions_by_score(self, num=10):
        return self.submissionDao.get_submissions('score', num) 

    def get_top_submissions_by_score_external(self, num=10):
        return self.submissionDao.get_submissions('score', num, True)

    def get_top_submissions_by_score_internal(self, num=10):
        return self.submissionDao.get_submissions('score', num, False)

    def get_top_submissions_by_comments(self, num=10):
        return self.submissionDao.get_submissions('number_of_comments', num)

    def get_top_submissions_by_comments_external(self, num=10):
        return self.submissionDao.get_submissions('number_of_comments', num, True)

    def get_top_submissions_by_comments_internal(self, num=10):
        return self.submissionDao.get_submissions('number_of_comments', num, False)
