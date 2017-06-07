#!/usr/bin/env python3

import sqlite3

'''
A way to access to the SQLiteDB for obtaining submissions information
'''
class SubmissionDao(object):
    def __init__(self):
        self.db_file = 'reddit_crawler.db'
        self.table = 'submission'
        # Column names
        self.title_c = 'title'
        self.is_external_c = 'is_external'
        self.external_url_c = 'external_url'
        self.discussion_url_c = 'discussion_url'
        self.submitter_c = 'submitter'
        self.n_comments_c = 'number_of_comments'
        self.creation_date_c = 'creation_date'
        self.score_c = 'score'

    '''
    Create the table if it doesn't exists
    '''
    def create_table(self):
        conn = self.__create_connection()
        # Only if we have connection
        with conn:
            c = conn.cursor()
            # Prepare the query
            sql = 'CREATE TABLE IF NOT EXISTS %s (%s text, %s boolean, %s text, %s text, %s text, %s int, %s text, %s int)' %(self.table, 
                      self.title_c, self.is_external_c, self.external_url_c, self.discussion_url_c, self.submitter_c, self.n_comments_c, 
                      self.creation_date_c, self.score_c)
            c.execute(sql)
            conn.commit()
            c.close()

    '''
    Add a new row to the submission entry
    @param submission: the tupple values for a submission to add
    '''
    def add_submission(self, submission):
        conn = self.__create_connection()
        with conn:
            c = conn.cursor()
            sql = "INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?)" %self.table
            c.execute(sql, submission)
            conn.commit()
            c.close()

    '''
    Update a submission by a rowid
    @param submission_id: the rowid to update
    @param submission: the tupple values for a submission to update
    '''
    def update_submission(self, submission_id, submission):
        conn = self.__create_connection()
        # Only if we have connection
        with conn:
            c = conn.cursor()
            # Prepare the query
            sql = "UPDATE %s SET %s = ?, %s = ?, %s = ?, %s = ?, %s = ?, %s = ?, %s = ?, %s = ? WHERE rowid = ?" %(self.table, self.title_c, 
                      self.is_external_c, self.external_url_c, self.discussion_url_c, self.submitter_c, self.n_comments_c, 
                      self.creation_date_c, self.score_c)
            # Add the submission ID to the query
            submission = submission + (submission_id,)
            c.execute(sql, submission)
            conn.commit()
            c.close()

    '''
    Obtain a the list of submissions 
    @param by: order by some column
    @param limit: limit the rows to return
    @param kind: if we want to obtain only the external/internal values
    @return submission_list: the list of submissions
    '''
    def get_submissions(self, by=None, limit=None, kind=None):
        conn = self.__create_connection()
        # Prepare the ORDER BY query
        if not by:
            order_by = ''
        else:
            order_by = 'ORDER BY %s DESC' %by
        # Prepare the WHERE query
        if kind is None:
            where = ''
        else:
            where = 'WHERE %s = ?' %self.is_external_c
        # Prepare the LIMIT query
        if not limit:
            lim = ''
        else:
            lim = 'LIMIT %s' %limit
        with conn:
            c = conn.cursor()
            # Prepare the final query with the query params obtained before
            sql = "SELECT * FROM %s %s %s %s" %(self.table, where, order_by, lim)
            if kind is not None:
                c.execute(sql, (kind,))
            else:
                c.execute(sql)
            # Obtain all the submissions returned
            submission_list = c.fetchall()
            c.close()
        return self.__submission_to_dict(submission_list)

    '''
    Add or update a submission
    @param submission: the tupple values of a submission
    '''
    def add_or_update_submission(self, submission):
        submission_url = [submission[3]]
        # We consider the submission discussion URL as the immutable part of a Submission 
        conn = self.__create_connection()
        with conn:
            c = conn.cursor()
            sql = "SELECT rowid FROM %s WHERE %s = ?" %(self.table, self.discussion_url_c)
            c.execute(sql, submission_url)
            data = c.fetchone()
            submission_id = data
            c.close()
            # If we get an id, update the submission
            if submission_id:
                self.update_submission(submission_id[0], submission)
            # Otherwhise, add it
            else:
                self.add_submission(submission)
                 

    '''
    Create a database connection to the SQLite database
    specified by the db_file
    @return: conn - Connection object or None
    '''
    def __create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
 
        return None

    '''
    Make a dict out of the list of submissions with the column names
    @param submission_list: the list of submissions tupples from the DB
    @return submission_dict_list: the list of submission dicts from the DB
    '''  
    def __submission_to_dict(self, submission_list):
        submission_dict_list = [] 
        for submission in submission_list:
            submission_dict = {}
            submission_dict[self.title_c] = submission[0]
            submission_dict[self.is_external_c] = submission[1]
            submission_dict[self.external_url_c] = submission[2]
            submission_dict[self.discussion_url_c] = submission[3]
            submission_dict[self.submitter_c] = submission[4]
            submission_dict[self.n_comments_c] = submission[5]
            submission_dict[self.creation_date_c] = submission[6]
            submission_dict[self.score_c] = submission[7]
            submission_dict_list.append(submission_dict)
        return submission_dict_list

