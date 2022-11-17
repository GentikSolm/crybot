FROM python:3.10-bullseye

WORKDIR /bot

COPY Pipfile Pipfile.lock /bot

RUN apt-get update && apt-get -y install cron && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache --upgrade pip pipenv
RUN pipenv lock && pipenv --clear && pipenv --rm
RUN pipenv install --deploy --system

COPY . /bot
CMD ["python", "bot.py"]

