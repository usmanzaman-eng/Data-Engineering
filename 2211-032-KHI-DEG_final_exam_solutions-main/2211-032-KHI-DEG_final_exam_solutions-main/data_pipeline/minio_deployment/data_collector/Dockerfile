FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install pyyaml ua-parser user-agents
COPY data_collector.py data_collector.py
ENV PYTHONPATH /app
CMD [ "python3", "data_collector.py"]
