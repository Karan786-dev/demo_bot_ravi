FROM python:3.9

WORKDIR .
ENV PYTHONUNBUFFERED=1


COPY requirements.txt .

RUN pip3 install -r requirements.txt 


 
 
COPY . .
CMD ["python3","bot.py"]
