FROM python:3.8
EXPOSE 5000
WORKDIR /app

# Update and install dependency for opencv (ofter already in normal computer)
RUN apt-get update && apt-get install -y libgl1

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]