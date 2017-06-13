#!/usr/bin/python2.7
#
#  A small script to report statistics on the news database
#  The script relies on several views on the news database:
#       'article_views' summarizes the views for each article_views and relies
#       on a summary view of the 'log' table called 'views'
#       'writers' summarizes which article was written by which author
#       'view_errors' counts the number of '200 OK' and '404 NOT FOUND' status
#       codes and returns the percentage error rate on each date
#

import psycopg2

conn = psycopg2.connect("dbname=news")

cur = conn.cursor()

cur.execute("SELECT * FROM article_views LIMIT 3;")

rows = cur.fetchall()

print "\nThe most popular three articles so far:\n"

for row in rows:
    print row[0] + ' - ' + str(row[1]) + ' views'

cur.execute("SELECT "
            "writers.name, SUM(article_views.views) as total "
            "FROM writers INNER JOIN article_views "
            "ON writers.title = article_views.title "
            "GROUP BY writers.name ORDER BY total DESC;")

rows = cur.fetchall()

print "\nAuthor ranking so far:\n"

for row in rows:
    print row[0] + ' - ' + str(row[1]) + ' views'

cur.execute("SELECT "
            "view_date, percent_errors "
            "FROM view_errors WHERE percent_errors > 1;")

rows = cur.fetchall()

print "\nDays on which we have seen greater than 1 percent errors:\n"

for row in rows:
    print row[0].strftime("%A %d %B %Y") + ' - ' + str(row[1]) + ' %% errors'

conn.close()
