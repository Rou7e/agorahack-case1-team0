# syntax=docker/dockerfile:1
FROM python:3.9
ADD . .
EXPOSE 8100

RUN pip install pandas numpy tqdm tensorflow matplotlib nltk pymorphy2 sklearn 
CMD ["python", "./main.py"] 