FROM python:3.10-slim
ENV TOKEN='7051565658:AAGNKHesOY5SqOXM1csY89rN298agX1UZMs'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "telegram_bot.py" ]