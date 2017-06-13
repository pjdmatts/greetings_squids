**News Query**

***What is this code for?***

`news_query.py` is a script that displays summary statistics about the
webserver log for the newspaper website. 'news_query.py' answers the following
questions:

- What are the most popular three articles of all time?

- Who are the most popular article authors of all time?

- On which days did more than 1% of requests lead to errors?

***Where to get the files***

Download the necessary files from [this Github repository](https://github.com/pjdmatts/greetings_squids)

Add the convenience views (see details below) to your news database before running the script

***Files Included***

- `news_query.py` a script to generate summary statistics for the newspaper
website

***Requirements***

This code was written with Python 2.7.12.

Several convenience views have been written to do most of the heavy lifting
in PSQL, allowing the python script to remain relatively light. You will need to add these to your news database before running the script.

***How to use this application***

Connect to the news database:
```
$psql news
```
Create the required views as follows.

The 'views' view:

```
news=> CREATE VIEW views AS SELECT path, COUNT(path) as views FROM log GROUP BY path ORDER BY views DESC;
```
The 'article_views' view:
```
news=> CREATE VIEW article_views AS SELECT articles.title, views.views FROM articles INNER JOIN views ON articles.slug = regexp_replace(views.path, '/article/', '');
```
The 'writers' view:

```
news=> CREATE VIEW writers AS SELECT articles.title, authors.name FROM articles INNER JOIN authors ON articles.author = authors.id;
```

The 'view_errors' view:

```
news=> CREATE view view_errors AS SELECT date(log.time) as view_date, COUNT(status) AS total_views, COUNT(CASE WHEN status = '200 OK' THEN 1 END) AS ok, COUNT(CASE WHEN status = '404 NOT FOUND' THEN 1 END) AS not_found, ROUND((100.0*COUNT(CASE WHEN status = '404 NOT FOUND' THEN 1 END)/COUNT(status)), 3) AS percent_errors FROM log GROUP BY view_date ORDER BY percent_errors DESC;
```

Now from the root of the application we are free to run the script:

```
$python news_query.py
```
