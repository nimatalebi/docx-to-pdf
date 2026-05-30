FROM mirror-docker.runflare.com/libreofficedocker/libreoffice-unoserver:3.18

USER root

RUN apk add --no-cache \
    python3 \
    py3-pip \
    font-noto \
    ttf-dejavu \
    wget

RUN mkdir -p /usr/share/fonts/custom

COPY fonts/ /usr/share/fonts/custom/

RUN fc-cache -fv

RUN libreoffice --headless --version



WORKDIR /app

COPY requirements.txt .

RUN pip3 install -i https://mirror2.chabokan.net/pypi/simple  \
    --break-system-packages \
    --no-cache-dir \
    -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]