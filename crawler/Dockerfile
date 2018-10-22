FROM ubuntu
RUN apt update && apt install -y python3 python-pip wget unzip openjdk-8-jre-headless xvfb libxi6 libgconf-2-4
RUN pip install selenium
RUN wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv -f chromedriver /usr/local/bin/
RUN chmod 0755 /usr/local/bin/chromedriver
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -yf

RUN mkdir /app

RUN pip install boto3 awscli
RUN wget https://s3.amazonaws.com/aws-cloudwatch/downloads/latest/awslogs-agent-setup.py
RUN apt install -y cron systemd
ADD awslogs.conf /app/
RUN mkdir /var/lib/awslogs
RUN python ./awslogs-agent-setup.py --region eu-west-1 --non-interactive --configfile /app/awslogs.conf
ADD awslogs.service /etc/systemd/system/
RUN systemctl enable awslogs.service

ADD crawl.py /app/
ADD show.py /app/
ADD start.sh /app/start.sh.orig
RUN cat /app/start.sh.orig | tr -d '\r' > /app/start.sh
WORKDIR /app/