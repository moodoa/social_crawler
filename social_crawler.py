import re
import tweepy
import instaloader

from facebook_scraper import get_posts
from datetime import datetime, timedelta


class SOCIALCRAWLER:
    def get_fb_articles(self, fan_pages, last_x_mins, account, password):
        wanted_articles = []
        for fan_page in fan_pages:
            for post in get_posts(fan_page, pages=2, credentials=(account, password)):
                wanted_article = {}
                print(post)
                if (
                    post["time"] > datetime.now() + timedelta(minutes=int(last_x_mins))
                    and post["text"]
                ):
                    wanted_article["author"] = post["username"]
                    wanted_article["text"] = f"{post['text'][:50]}..."
                    wanted_article["time"] = post["time"]
                    wanted_article["comments"] = post["comments"]
                    wanted_article["likes"] = post["likes"]
                    wanted_article["post_url"] = post["post_url"]
                    wanted_articles.append(wanted_article)
        return wanted_articles

    def get_ig_articles(self, accounts, last_x_mins):
        wanted_articles = []
        insta = instaloader.Instaloader()
        for account in accounts:
            profile = instaloader.Profile.from_username(insta.context, account)
            check_time = datetime.now() + timedelta(minutes=int(last_x_mins))
            posts = profile.get_posts()
            try:
                for post in posts:
                    if check_time < post.date_local and post.caption:
                        wanted_article = {}
                        wanted_article["author"] = post.profile
                        wanted_article["text"] = f"{post.caption[:50]}..."
                        wanted_article["time"] = post.date_local
                        wanted_article["comments"] = post.comments
                        wanted_article["likes"] = post.likes
                        wanted_article[
                            "post_url"
                        ] = f"https://www.instagram.com/p/{post.shortcode}/"
                        wanted_articles.append(wanted_article)
                    else:
                        break
            except:
                pass
        return wanted_articles

    def get_twitter_articles(
        self,
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret,
        accounts,
        last_x_mins,
    ):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        tweet_infos = []
        for account in accounts:
            try:
                status = api.user_timeline(account, tweet_mode="extended")
                for idx in range(0, len(status)):
                    if not status[idx]._json["entities"]["user_mentions"]:
                        tweet_info = {}
                        time_string = (
                            status[idx]._json["created_at"].replace("+0000 ", "")
                        )
                        t_format = datetime.strptime(
                            time_string, "%a %b %d %H:%M:%S %Y"
                        ) + timedelta(hours=8)
                        if t_format > datetime.now() + timedelta(
                            minutes=int(last_x_mins)
                        ):
                            tweet_info["create_time"] = t_format
                            tweet_info["retweet_count"] = str(
                                status[idx]._json["retweet_count"]
                            )
                            tweet_info["favorite_count"] = str(
                                status[idx]._json["favorite_count"]
                            )
                            tweet_info["user_name"] = status[idx]._json["user"]["name"]
                            tweet_info["link_tweet"] = (
                                f"https://twitter.com/{account}/status/"
                                + status[idx]._json["id_str"]
                            )
                            tweet_info["tweet_content"] = "\n".join(
                                re.split(r"\n+", status[idx]._json["full_text"])
                            )
                            tweet_infos.append(tweet_info)
                        else:
                            break
            except Exception as e:
                print(e)
                pass
        return tweet_infos


if __name__ == "__main__":
    crawler = SOCIALCRAWLER()
    print(
        crawler.get_fb_articles(
            ["dcard.tw"], "-300", "fb_account", "fb_password"
        )
    )
    print(crawler.get_ig_articles(["dcard.tw"], "-300"))
    print(
        crawler.get_twitter_articles(
            "c_key", "c_secret", "a_token", "a_secret", ["NBA"], "-300"
        )
    )
