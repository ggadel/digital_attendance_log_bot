FROM python:3.12.7
RUN py -m venv venv
RUN source venv/bin/activate
COPY . .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]