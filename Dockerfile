FROM STARK-LUCIFER/Music:slim-buster

RUN git clone https://github.com/STARK-LUCIFER/Music.git /root/userbot
WORKDIR /root/userbot

## Install requirements
RUN pip3 install -U -r requirements.txt

ENV PATH="/home/userbot/bin:$PATH"

CMD ["python3","-m","userbot"]
