FROM python:3.9-slim
LABEL Author="Rupert Broad - Ohpen B.v."

ENV APP_DIR=/mvdb
WORKDIR $APP_DIR

RUN apt update \
  && apt install -y jq curl

# Install requirements
COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install -r requirements.txt 

# Copy api code
COPY ./app $APP_DIR/

CMD ["python3", "server.py"]
