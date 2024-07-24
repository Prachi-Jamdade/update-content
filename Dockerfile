FROM python:3.9

COPY fetch_recent_content.py /fetch_recent_content.py
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "/fetch_recent_content.py"]
