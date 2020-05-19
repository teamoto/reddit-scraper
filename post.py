import scrape
import mongo
import datetime
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dbhost', help='hostname to connect a mongodb')
    parser.add_argument('--port',
                        help='port number to connect a mongodb',
                        type=int)
    parser.add_argument('--collection', help='collection in the db')
    parser.add_argument('--dbname', help='database name')
    parser.add_argument('--dbuser', help='username to connect a mongodb')
    parser.add_argument('--dbpass', help='password to connect a mongodb')
    parser.add_argument('--site', help='site to scrape')
    return parser.parse_args()


if __name__ == "__main__":

    args = get_args()
    db = mongo.connect_mongodb(args.dbhost, args.port, args.dbname,
                               args.dbuser, args.dbpass)
    collection = db[args.collection]
    if args.site != '':
        articles = scrape.scrape_reddit(args.site)

    for article in articles:
        # check if the post is already in the db by using url
        # add the post only if the entry does not exist in the db
        if mongo.check_post(collection, article['url']):
            # add date
            article['posted'] = datetime.datetime.now()
            mongo.insert_document(collection, article)
        else:
            print(f"{article['title']} is already in db")
