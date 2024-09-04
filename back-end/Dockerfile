FROM python:3.11-slim

RUN mkdir -p /home/app

RUN addgroup --system app && adduser --system --group app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chown -R app:app $APP_HOME

USER app

CMD ["uvicorn", "app_factory:create_app", "--proxy-headers", "--factory", "--host", "0.0.0.0", "--port", "5000"]

