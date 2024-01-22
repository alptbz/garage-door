FROM python:3.9
LABEL authors="philipp"

COPY . .

EXPOSE 5000/tcp

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]