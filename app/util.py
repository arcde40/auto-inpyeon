from datetime import datetime, timedelta;

def split_content(content, max_length=950, encoding='utf-8'):
    split_list = [];
    total_len = len(content);
    cursor = 0;
    while cursor < total_len:
        if cursor + max_length > total_len:
            split_list.append(content[cursor:]);
            break;
        else:
            split_list.append(content[cursor:cursor+max_length]);
            cursor += max_length;
    return split_list;

def get_current_date_string():
    current_date = datetime.now().date();
    return get_date_string(current_date);

def get_tomorrow_date_string():
    current_date = datetime.now().date();
    return get_date_string(current_date + timedelta(days=1));

def get_yesterday_date_string():
    current_date = datetime.now().date();
    return get_date_string(current_date - timedelta(days=1));
def get_current_hour_string():
    now = datetime.now()
    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2300"
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "00"
            else:
                base_time = str(pre_hour) + "00"
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "00"
        else:
            base_time = str(now.hour) + "00"

    return base_time

# https://dalseobi.tistory.com/130 (기상 데이터 API 활용)

def get_date_string(date):
    return date.strftime("%Y%m%d");
