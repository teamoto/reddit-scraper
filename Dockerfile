FROM python:latest

# download and instlal chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
  apt update -y && \
  apt install -y google-chrome-stable unzip python3-lxml && \
  # install nencessary python packages
  pip install --no-cache-dir selenium requests BeautifulSoup4 lxml pytz pymongo && \
  # download and install chrome driver
  cd /opt/google/chrome && \
  wget https://chromedriver.storage.googleapis.com/81.0.4044.69/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip && rm -f chromedriver_linux64.zip && \
  # remove the apt cache
  rm -rf /var/lib/apt/lists/*

ENV PATH /opt/google/chrome:$PATH
CMD [ "python" ]
