# social_crawler
爬取 facebook, instagram, twitter 指定帳號的發文

![alt text](https://media.disrn.com/articles/a60e5f49-1277-4815-ad4a-2e56d51b2cf6.jpg)

## social_crawler.py
* 在 `facebook`、`instagram`、`twitter` 三大社群平台上蒐集指定帳號的發文。
* 蒐集回來的資料以 JSON 格式儲存。
* get_fb_articles 參數 : 目標帳號(list), 過去X分鐘的發文(str), FB帳號(str), FB密碼(str)。
* get_ig_articles 參數 : 目標帳號(list), 過去X分鐘的發文(str)。
* get_twitter_articles 參數 : consumer_key, consumer_secret, access_token, access_token_secret(這四項在 twitter 申請), 目標帳號(list), 過去X分鐘的發文(str)。

## Requirements
python 3.7

## Installation
`pip install -r requriements.txt`

## usage
```
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
```
