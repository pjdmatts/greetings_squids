#!/usr/bin/python2.7
#
#  A small script to report statistics on the news database
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
