from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import lxml


def get_time(posted_time):
    t = int(posted_time[0])
    if "hour" in posted_time:
        return datetime.now() - timedelta(hours=t)
    elif "minute" in posted_time:
        return datetime.now() - timedelta(minutes=t)


def scrape_reddit(subreddit):

    # reddit base url
    base_url = "https://www.reddit.com"
    # create a url for the target subreddit
    url = base_url + "/r/" + subreddit + "/new"
    # define wait time to load
    wait_time = 1
    # define list to store results
    recent_posts = []
    # initiate webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    # connect the url using the webdriver
    print('Accessing ' + url)
    driver.get(url)
    # wait
    time.sleep(wait_time)
    # parsing
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # define selector to get body containing posts
    selector = "html>body>div:nth-of-type(1)>div>div>div>div:nth-of-type(2)"
    selector += ">div>div>div>div:nth-of-type(2)>div:nth-of-type(3)"
    selector += ">div:nth-of-type(1)>div:nth-of-type(4)"
    # start persing html content
    try:
        body = soup.select(selector)

        # get posts currently shown on the browser
        posts = body[0].find_all("div", class_="scrollerItem")
        # loop through the posts
        for post in posts:
            title = post.find("h3")
            # filter unnecessary posts
            if title is not None:
                posted_time = post.find("a", attrs={
                    "data-click-id": True
                }).get_text().strip()
                if "day" not in posted_time.lower():
                    recent_post = dict()
                    recent_post['title'] = title.get_text().strip()
                    posted_time = post.find("a", attrs={
                        "data-click-id": True
                    }).get_text().strip()
                    recent_post['posted'] = get_time(posted_time)
                    url = post.find("a",
                                    attrs={"data-click-id": "body"},
                                    href=True)['href'].strip()
                    recent_post['url'] = base_url + url
                    recent_post['comments'] = post.find(
                        "a", attrs={
                            "data-click-id": "comments"
                        }).get_text().strip()[0]
                    recent_post['site'] = subreddit
                    # append the result to the list
                    recent_posts.append(recent_post)

        driver.quit()
        return recent_posts

    except IndexError as e:
        # mostly this error happens when non-existing subreddit is selected
        print(f"Error: {e}")
        print("Most likely you specified a non-existing subreddit")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # testing
    # specify the subreddit
    posts = scrape_reddit('aws')
    if posts is not None:
        for post in posts:
            print(post)
    else:
        print("No results...")
