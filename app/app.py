import logging;
import datetime;
import os
import sys;
from dotenv import load_dotenv;


def run():
    load_dotenv();
    logpath = os.getenv("LOGFILE_DIR") or "";
    newspath = os.getenv("NEWSFILE_DIR") or "";
    receiver_filepath = os.getenv("RECEIVER_FILE_PATH");
    now = datetime.datetime.now();
    now_string = now.strftime("%Y-%m-%d-%H-%M-%S");
    logging.basicConfig(
        format='[%(module)s:%(lineno)d] %(asctime)s %(levelname)s\t %(message)s',
        level=logging.INFO,
        datefmt='%m/%d/%Y %I:%M:%S %p');
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout));

    if logpath:
        file_handler = logging.FileHandler(os.path.join(logpath, now_string + '.log'));
        file_handler.setLevel(logging.WARNING);
        file_handler.setFormatter(logging.Formatter(fmt='[%(module)s:%(lineno)d] %(asctime)s %(levelname)s\t %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'))
        logging.getLogger().addHandler(file_handler);

    logging.info("Started: " + now_string);

    import crawler;
    import sender;
    import util;

    try:
        content = crawler.news_crawl();

        logging.info("News Crawling Succeed");
        if newspath:
            try:
                news_log = open(os.path.join(newspath, f"news-{now_string}.txt"), mode='w');
                news_log.write(content);
                news_log.close();
                latest_log = open(os.path.join(newspath, "latest.txt"), mode="w");
                latest_log.write(content);
                latest_log.close();
                logging.info("News Log Created");
            except Exception as e2:
                logging.error(f"Failed to write news log: {e2}")
    except Exception as e:
        logging.error(f"Failed to scrap news: {e}");
        return;

    receiver_list = [];
    try:
        receiver_pref = open(receiver_filepath, mode='r', encoding='utf-8');
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
            logging.warning("Malformed receiver information! This will be skipped.");
            continue;

        name, year, month, day = split;
        logging.info(f"Sending to {name} ({year}/{month}/{day})".replace('\n', ''));
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
