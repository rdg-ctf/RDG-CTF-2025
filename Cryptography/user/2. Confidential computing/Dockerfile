FROM python:3.9-alpine

RUN apk add --no-cache socat

RUN adduser -D -u 1000 ctf

WORKDIR /home/ctf

COPY --chown=ctf:ctf . .

RUN if [ -f requirements.txt ]; then \
    pip install --no-cache-dir -r requirements.txt; \
    fi

RUN chmod 440 flag.txt && \
    chmod 550 server.py && \
    chown root:ctf flag.txt server.py

EXPOSE 7777
USER ctf
CMD ["socat", "tcp-l:7777,reuseaddr,fork", "EXEC:'python3 server.py',pty,stderr"]