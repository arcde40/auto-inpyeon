import logging;
import datetime;
import sys;

now = datetime.datetime.now();
now_string = now.strftime("%Y-%m-%d-%H-%M-%S");
logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='log/'+now_string + '.log');
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout));

logging.info("Started: " + now_string);

import crawler;
import sender;
import util;

try:
    content = crawler.news_crawl();

    logging.info("News Crawling Succeed");

    news_log = open(f"log/news/news-{now_string}.txt", mode='w');
    news_log.write(content);
    news_log.close();
    latest_log = open("log/news/latest.txt", mode="w");
    latest_log.write(content);
    latest_log.close();
    logging.info("News Log Created");
except Exception as e:
    logging.error(f"Failed to create news log: {e}");

receiver_list = [];
try:
    receiver_pref = open("receiver.txt", mode='r', encoding='utf-8');
    receiver_list = receiver_pref.readlines();
except Exception as e:
    print(e);
    logging.error("No receiver list!");

content_list = util.split_content(content, max_length=950);

print(content_list);
