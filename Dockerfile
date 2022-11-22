FROM python:3.10-bullseye

WORKDIR /bot

COPY Pipfile Pipfile.lock /bot

RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*
RUN apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata
RUN python -m pip install --no-cache --upgrade pip pipenv
RUN pipenv lock && pipenv --clear && pipenv --rm
RUN pipenv install --deploy --system

COPY . /bot
CMD ["python", "-u", "bot.py"]

