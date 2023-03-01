FROM python:3.6

COPY src/ /opt/src
WORKDIR /opt/src

RUN pip install -r requirements.txt
CMD ["python", "gearman_worker_test.py"]
#CMD ["python", "gearman_client_test.py"]