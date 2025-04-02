FROM node:21

RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcups2 \
    libxdamage1 \
    libgbm-dev \
    libxkbcommon0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    --no-install-recommends

WORKDIR /src
COPY ./src .
RUN npm install
RUN node node_modules/puppeteer/install.js

EXPOSE 9222

# Запускаем бот
CMD ["node", "/src/bot.js"]
