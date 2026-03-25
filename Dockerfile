FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -yq \
    tzdata \
    && rm -rf /var/lib/apt/lists/* # (2) switch to (1)
# set your timezone
RUN ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime # (1) switch to (2)
RUN dpkg-reconfigure -f noninteractive tzdata

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -yq \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ~/miniconda3
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
RUN bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
RUN rm -rf ~/miniconda3/miniconda.sh
RUN ~/miniconda3/bin/conda init bash
RUN ~/miniconda3/bin/conda config --set auto_activate_base false

RUN mkdir -p /root/selenium-authenticated-proxy

# Install Chromium and Chromedriver
RUN apt-get update && apt-get install -y \
    curl unzip xvfb libxi6 libgconf-2-4 gnupg wget

# Google Chrome
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get -y update \
    && apt-get -y install google-chrome-stable \

ARG VERSION_CHROME=146.0.7680.153-1
ARG VERSION_DRIVER=146.0.7680.153
# Google Chrome
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${VERSION_CHROME}_amd64.deb \
    && dpkg -i google-chrome-stable_${VERSION_CHROME}_amd64.deb || apt-get install -fy \
    && rm google-chrome-stable_${VERSION_CHROME}_amd64.deb

# ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+') \
    && wget -N "https://storage.googleapis.com/chrome-for-testing-public/${VERSION_DRIVER}/linux64/chromedriver-linux64.zip" -P /tmp \
    && unzip /tmp/chromedriver-linux64.zip -d /usr/local/bin \
    && rm /tmp/chromedriver-linux64.zip \
    && chown root:root /usr/local/bin/chromedriver-linux64/chromedriver \
    && chmod 0755 /usr/local/bin/chromedriver-linux64/chromedriver \
    && ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \

ENV CHROME_DRIVER_PATH=/usr/local/bin/chromedriver
ENV CHROME_PATH=/usr/bin/google-chrome

WORKDIR /root/selenium-authenticated-proxy

