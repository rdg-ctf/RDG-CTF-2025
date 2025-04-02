FROM node:14

RUN apt-get update && \
    apt-get install -y pandoc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY server/package*.json ./

RUN npm install

COPY server /app

RUN echo "rdg{n3wl1n3_m4y_l34d_t0_rc3}" > /tmp/flag.txt
RUN chmod 444 /tmp/flag.txt

EXPOSE 3000

CMD ["npm", "start"]

