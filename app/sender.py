import os
import logging;

from selenium import webdriver;
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By;
from selenium.webdriver.chrome.service import Service;
from selenium.webdriver.support.ui import WebDriverWait;
from selenium.webdriver.support import expected_conditions as EC;
from datetime import datetime;

chromedriver = os.getenv("CHROME_DRIVER");

options = webdriver.ChromeOptions();
options.add_argument('--headless');
options.add_argument('--no-sandbox');
options.add_argument('--disable-dev-shm-usage');
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36");


def senderRetry(content, p_name, p_birth_year, p_birth_month, p_birth_day, index):
    for i in range(0,3):
        ret = sender_with_title(content, p_name, p_birth_year, p_birth_month, p_birth_day, index);
        if ret == 0:
            return 0;
        logging.warning(f"Failed to send letter.. Retrying ({i}/3)");
    return -1;


def sender_with_title(content, p_name, p_birth_year, p_birth_month, p_birth_date, page):
    title = f'오늘의 뉴스 헤드라인: {datetime.now().strftime("%m월 %d일")} ({page})';
    logging.info(f'Sending letter: {title}');
    return sender(title, content, p_name, p_birth_year, p_birth_month, p_birth_date);

def sender(title, content, p_name, p_birth_year, p_birth_month, p_birth_date):
    wd = webdriver.Chrome(service=Service(os.getenv("CHROME_DRIVER")), options=options);
    wd.implicitly_wait(30);

    wait = WebDriverWait(wd, 30);
    try:
        # 브라우저에 해당 도메인 열기
        wd.get('https://www.airforce.mil.kr/user/indexSub.action?codyMenuSeq=156893223&siteId=last2&menuUIType=sub');

        logging.info("접속 성공");
        name = wd.find_element(By.XPATH, "//*[@id='searchName']");
        name.send_keys(p_name);
        birth_year = wd.find_element(By.XPATH, "//*[@id='birthYear']");
        birth_year.send_keys(str(p_birth_year));
        birth_month = wd.find_element(By.XPATH, "//*[@id='birthMonth']");
        birth_month.send_keys(str("%02d" %(p_birth_month)));
        birth_date = wd.find_element(By.XPATH, "//*[@id='birthDay']");
        birth_date.send_keys(str("%02d" %(p_birth_date)));

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnNext']")));
        search_button = wd.find_element(By.XPATH, "//*[@id='btnNext']");
        search_button.click();

        logging.info("훈련병 찾기 버튼 클릭 성공");

        try:
            # Popup
            wd.switch_to.window(wd.window_handles[1]);
        except Exception as e:
            logging.error("팝업이 출력되지 않았습니다!");
            raise Exception;

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailPic-container"]/ul/li/input')));
            confirm_button = wd.find_element(By.XPATH, '//*[@id="emailPic-container"]/ul/li/input');
            confirm_button.click();
            logging.info("훈련병 선택 성공");
        except TimeoutException as e:
            logging.error("훈련병을 찾지 못했습니다!");
            raise Exception;

        # Return
        wd.switch_to.window(wd.window_handles[0]);

        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='btnNext']")));
        search_button = wd.find_element(By.XPATH, "//*[@id='btnNext']");
        search_button.click();

        logging.info("다음 버튼 선택 성공");

        # List

        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailPic-container"]/div[3]/span/input')));
            write_button = wd.find_element(By.XPATH, '//*[@id="emailPic-container"]/div[3]/span/input');
            write_button.click();
            logging.info("편지작성 버튼 선택 성공");
        except TimeoutException as e:
            logging.error("편지 작성 기간이 아닙니다!");
            raise Exception;

        # 우편번호 검색 버튼 클릭 후 창 전환
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="emailPic-container"]/form/div[1]/table/tbody/tr[3]/td/div[1]/span/input')))
        wd.find_element(By.XPATH,
                            '//*[@id="emailPic-container"]/form/div[1]/table/tbody/tr[3]/td/div[1]/span/input').click()
        wd.switch_to.window(wd.window_handles[1])
        logging.info('우편번호 검색 버튼 클릭 후 창 전환 성공')

        # 주소 검색
        wait.until(EC.presence_of_element_located((By.ID, "keyword")))
        wd.find_element(By.ID, 'keyword').send_keys('경남 진주시 금산면 송백로 46')
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchContentBox"]/div[1]/fieldset/span/input[2]')))
        wd.find_element(By.XPATH, '//*[@id="searchContentBox"]/div[1]/fieldset/span/input[2]').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="roadAddrTd1"]/a')))
        wd.find_element(By.XPATH, '//*[@id="roadAddrTd1"]/a').click()
        logging.info('주소 검색 성공')

        # 상세주소 입력 후 창 전환
        wd.find_element(By.ID, 'rtAddrDetail').send_keys('경남 진주시 금산면 송백로 46')
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="resultData"]/div/a')))
        wd.find_element(By.XPATH, '//*[@id="resultData"]/div/a').click()
        wd.switch_to.window(wd.window_handles[0])
        logging.info('상세주소 입력 후 창 전환 성공')

        # 발신자 이름, 관계 입력
        wd.find_element(By.ID, 'senderName').send_keys('네이버뉴스')
        wd.find_element(By.ID, 'relationship').send_keys('언론사')
        logging.info('발신자 이름, 관계 입력 성공')

        # 제목 입력
        wd.find_element(By.ID, 'title').send_keys(title)
        logging.info('제목 입력 성공')

        # 내용 입력
        wd.find_element(By.ID, 'contents').send_keys(content);
        logging.info('내용 입력 성공')

        # 비밀번호 입력
        wd.find_element(By.ID, 'password').send_keys(str(os.environ.get('LETTER_PASSWORD')));
        logging.info('비밀번호 입력 성공')

        # 편지쓰기 클릭
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="emailPic-container"]/form/div[2]/span[1]/input')))
        wd.find_element(By.XPATH, '//*[@id="emailPic-container"]/form/div[2]/span[1]/input').click()
        logging.info('편지쓰기 클릭 성공')
    except Exception as e:
        print(e);
        wd.quit();
        return -1;

    wd.quit();
    return 0;