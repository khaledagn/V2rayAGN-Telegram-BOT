FROM python:3.10-slim

WORKDIR /app

COPY . /app




RUN apt-get update && apt-get install -y cron && pip install --no-cache-dir -r requirements.txt

RUN echo "*/10 * * * * /app/scheduler.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/scheduler-cron \
    && chmod 0644 /etc/cron.d/scheduler-cron \
    && crontab /etc/cron.d/scheduler-cron

RUN touch /var/log/cron.log

EXPOSE 8443

CMD cron && tail -f /var/log/cron.log



RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8443

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8443", "--ssl-certfile", "fullchain.pem", "--ssl-keyfile", "privkey.pem"]
