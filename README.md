# Reddit Scraper

## Overview

These python scripts simply scrape a specified subreddit with Selenium and save the results to a mongodo.

## Requirements

### Python Libraries

 - beautifulsoup4
 - lxml
 - pymongo
 - pytz
 - requests
 - selenium

### Docker Environment

You can create a docker image from the Dockerfile:

    docker build -t reddit-scraper .

## Usage

If you just want to scrape a newest post from a subreddit, it's fairly simple:

    # run a docker container and access via pseudo tty
    docker run -it --rm -v $(pwd):/app -w /app /bin/bash
    # edit a scrape.py's line 92 and type a subreddit name you want to scrape
    posts = scrape_reddit('aws')
    # once saved, run the python script
    python scrape.py

If you want to save the results into a mongo db, it gets bit more complex
The following is a sample code:

    post.py --dbhost 'your.mongodb.url' --port 'your port in int' \
    --dbname 'scraped_data' --collection 'your.collection' \ 
    --dbuser 'dbuser' --dbpass 'dbuserpass' --site 'subreddit'

Each argument should be pretty selfexplanatory, but you need to have a mongo db and a collection with a user having write permission on the mongodb.
Also, this code has to be run in an environment where it can communicate with the db (weather over the wan or within the lan).
