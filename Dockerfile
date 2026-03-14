FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir aiogram==3.7.0 aiohttp==3.9.5 aiohttp-socks==0.8.4
COPY . .
CMD ["python", "bot.py"]
