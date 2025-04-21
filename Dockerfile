FROM python:3.10-slim

WORKDIR /app

RUN apt update && \
	apt -y install ffmpeg libsm6 libxext6

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

ENTRYPOINT streamlit run /app/src/face_matcher/app.py
