FROM python:3
LABEL authors="GGwM"
COPY . /tema
WORKDIR /tema
RUN pip install -r requirements.txt
CMD ["python3", "tema_complete.py"]
