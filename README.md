# Auto-Inpyeon
Simple python program that scraps news and sends it through ROKAF website

## How to Run
receiver.txt 파일에 수신자를 '이름/생년/월/일' 형태로 넣어주세요. 여러 줄에 걸쳐 다수의 수신자를 지정할 수도 있습니다. # 붙여 주석 처리할 수 있습니다.

기상청 예보 기능을 사용하기 위해선 기상청 Open AI API Key가 필요합니다.
### Docker
Docker을 이용해 쉽게 배포할 수 있습니다. 이 방법을 사용 시 Build 과정에서 자동으로 최신 버전의 Chrome Driver을 다운로드합니다.


```shell
# 먼저 .env 파일에 다음 내용을 채워주세요.
# WEATHER_API_KEY="<API KEY>"
docker build -t auto-inpyeon .
docker run --name auto-inpyeon -d
```

### Direct Install
직접 Repo를 Clone하여 사용할 수 있습니다. 이 경우 .env 파일에 다음 항목을 추가해야 합니다.
```text
CHROME_DRIVER="<chromedriver 경로>"
WEATHER_API_KEY="<API KEY>"
```

## Disclaimer
이 프로젝트는 보라매인편 (https://github.com/k4sud0n/borame-letter)의 소스코드를 참고하여 제작되었습니다.