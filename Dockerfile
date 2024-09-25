FROM python:3.10
WORKDIR /usr/src
RUN apt-get -y update
RUN apt install wget
RUN apt install unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://storage.googleapis.com/chrome-for-testing-public/` curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE`/linux64/chromedriver-linux64.zip
RUN mkdir chrome
RUN unzip -j /tmp/chromedriver.zip chromedriver-linux64/chromedriver -d /usr/src/chrome
RUN mkdir log
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY receiver.txt ./
COPY template.txt ./
ENV CHROME_DRIVER=/usr/src/chrome/chromedriver
CMD [ "python", "app/main.py" ]
