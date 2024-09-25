import logging
import os

from bs4 import BeautifulSoup;
import requests;
import re;
import util;
import xmltodict;
import pandas as pd;


def news_connect(category):
    url = f'https://news.naver.com/section/{category}';
    response = requests.get(url); # 현재 페이지 코드 읽어오기

    if response.status_code != 200:
        logging.error(f"News Connection failed: {response.status_code}");
        return '<뉴스 정보를 불러오는데 실패했습니다>';
    else:
        return news_crop(response.content);


def news_crop(html):
    soupCB = BeautifulSoup(html, 'html.parser');

    res = soupCB.select_one("#ct_wrap > div.ct_scroll_wrapper > div.column0 > div > h2 > a");
    category_str = res.text;

    res = soupCB.select("li.sa_item._SECTION_HEADLINE");
    list = [];
    for item in res[:10]:
        headline = item.select_one("div>div>div.sa_text>a>strong");
        list.append(re.sub("\[.*?\]", "", headline.text));

    str = category_str + ' > ' + ' / '.join(list);

    return str;

def news_sport_crawl():
    url = f'https://sports.news.naver.com/index';
    response = requests.get(url);  # 현재 페이지 코드 읽어오기

    if response.status_code != 200:
        logging.error(f"News Connection failed: {response.status_code}");
        return '<뉴스 정보를 불러오는데 실패했습니다>';

    html = response.content;

    soupCB = BeautifulSoup(html, 'html.parser');

    category_str = '스포츠';

    res = soupCB.select("#content > div > div.today_section.type_no_da > ul > li");
    list = [];
    for item in res:
        headline = item.select_one("a > div.text_area > strong");
        list.append(re.sub("\[.*?\]", "", headline.text));

    str = category_str + ' > ' + ' / '.join(list);

    return str;

def news_sport_football_ranking_crawl():
    url = f'https://sports.news.naver.com/wfootball/index';
    response = requests.get(url);  # 현재 페이지 코드 읽어오기

    if response.status_code != 200:
        logging.error(f"News Connection failed: {response.status_code}");
        return '<뉴스 정보를 불러오는데 실패했습니다>';

    html = response.content;

    soupCB = BeautifulSoup(html, 'html.parser');

    category_str = '프리미어리그 랭킹';

    res = soupCB.select("#_team_rank_epl > table > tbody > tr");
    list = [];
    index = 1;
    for item in res:
        headline = item.select_one("td > div > div.info > span");
        list.append(f'{index}위 '+re.sub("\[.*?\]", "", headline.text));
        index += 1;

    str = category_str + ' > ' + ' / '.join(list);
    return str;

def weather_crawl():
    keys = os.getenv("WEATHER_API_KEY");
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst';
    params = {'serviceKey': keys,
              'pageNo': '1',
              'numOfRows': '1000',
              'dataType': 'XML',
              'base_date': util.get_yesterday_date_string(),
              'base_time': '0500',
              'nx': '81',
              'ny': '76'}; # x=81 y=76 진주시 금산면 (From API Manual)

    response = requests.get(url, params=params);
    xml_data = response.text;
    dict_data = xmltodict.parse(xml_data);

    date = util.get_tomorrow_date_string();

    weather_data = dict({
        'tmp': dict(),
        'sky': dict(),
        'pty': dict(),
        'pop': dict()
    });

    for item in dict_data['response']['body']['items']['item']:
        if item['fcstDate'] != date:
            continue;
        if int(item['fcstTime']) < 500 or int(item['fcstTime']) > 2300:
            continue;

        fcstTime = int(item['fcstTime']);
        # 기온
        if item['category'] == 'TMP':
            weather_data['tmp'][fcstTime] = item['fcstValue'];
        # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
        if item['category'] == 'SKY':
            weather_data['sky'][fcstTime] = item['fcstValue'] ;
        # 강수형태: 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7)
        if item['category'] == 'PTY':
            weather_data['pty'][fcstTime] = item['fcstValue'];
        if item['category'] == 'POP':
            weather_data['pop'][fcstTime] = item['fcstValue'];

    # Urgh... I hate this code

    df = pd.DataFrame(weather_data);
    df['tmp'] = pd.to_numeric(df['tmp']);

    min = df['tmp'].min();
    max = df['tmp'].max();
    pop = df['pop'].max();
    match int(df['sky'].mode().iloc[0]):
        case 1: sky = "맑음";
        case 3: sky = "구름 많음";
        case 4: sky = "흐림";

    str = f'내일 날씨 > 기온: {min}도 ~ {max}도 / 강수 확률: {pop}% / {sky}'
    return str;

def news_entertain_crawl():
    url = f'https://entertain.naver.com/home';
    response = requests.get(url);  # 현재 페이지 코드 읽어오기

    if response.status_code != 200:
        logging.error(f"News Connection failed: {response.status_code}");
        return '<뉴스 정보를 불러오는데 실패했습니다>';

    html = response.content;

    soupCB = BeautifulSoup(html, 'html.parser');

    category_str = '연예';

    res = soupCB.select("#ranking_news > div > div.rank_lst > ul > li");
    list = [];
    for item in res:
        headline = item.select_one("a");
        # remove em tag
        headline.find("em").extract();
        list.append(re.sub("\[.*?\]", "", headline.text));

    str = category_str + ' > ' + ' / '.join(list);
    return str;


def news_crawl(crawl_category = [100, 101, 102, 104, 105, 106, 109, 107, 108]):
    content = [];
    for i in crawl_category:
        match i:
            case 106: # sports
                content.append(news_sport_crawl());
            case 107: # premier league ranking
                content.append(news_sport_football_ranking_crawl());
            case 108: # weather
                content.append(weather_crawl());
            case 109: # entertain
                content.append(news_entertain_crawl());
            case _:
                content.append(news_connect(i));
    return ' // \n'.join(content);
