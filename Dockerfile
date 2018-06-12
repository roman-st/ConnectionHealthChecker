FROM python:2.7.15-jessie
RUN pip install falcon waitress
COPY source ./service
EXPOSE 8080/tcp
CMD ["python", "./service/main.py", "-c", "0.0.0.0:8080"]
