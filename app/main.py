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

for item in receiver_list:
    if item.startswith('#'):
        continue;
    split = item.split('/');
    if len(split) != 4:
        logging.info("Malformed receiver information! This will be skipped.");
        continue;

    name, year, month, day = split;
    logging.info(f"Sending to {name} ({year}/{month}/{day})".replace('\n',''));
    logging.info(f"Sending {len(content_list)} letter(s)");
    index = 1;
    for content in content_list:
        code = sender.senderRetry(content, name, int(year), int(month), int(day), index);
        if code != 0:
            logging.error(f"Failed to send letter {index}/{len(content_list)}");
        else:
            logging.info(f"Sent letter {index}/{len(content_list)}");
        index += 1;

    logging.info("Done!");

logging.info("Successfully sent all letters, Terminating...");
