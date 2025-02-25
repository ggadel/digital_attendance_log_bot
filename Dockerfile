FROM python:3.12.7
COPY . .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]