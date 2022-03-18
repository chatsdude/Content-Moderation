FROM python:3.7-slim

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile","Pipfile.lock","./"]

RUN pipenv install --system --deploy
RUN pipenv run spacy download en_core_web_md

COPY ["ContentModeration.py","ArticleScraper.py","AIEngine.py","Voting.pkl","./"]

EXPOSE 5000

ENTRYPOINT ["gunicorn", "--threads","10","--bind","0.0.0.0:5000","--timeout","1000","ContentModeration:api"]