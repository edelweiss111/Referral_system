FROM python:3

WORKDIR /Referral_system

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .