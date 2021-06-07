FROM python:3.9
RUN pip install pipenv
#RUN pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy
COPY demoji_update.py .
RUN python  demoji_update.py 
COPY . .
CMD python bot.py
