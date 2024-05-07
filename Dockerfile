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

# Set environment variables for Chromium and Chromedriver paths
ENV CHROME_PATH="/usr/bin/chromium"
ENV CHROME_DRIVER_PATH="/usr/bin/chromedriver"

# Install Chromium and Chromedriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/selenium-authenticated-proxy

