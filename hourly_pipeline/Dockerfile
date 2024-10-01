FROM python:latest
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY extract.py .
COPY transform.py .
COPY load.py .
COPY main.py .
CMD ["python3", "main.py"]
