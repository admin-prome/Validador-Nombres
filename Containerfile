FROM python:3.10
RUN python3 -m venv /opt/venv
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN . /opt/venv/bin/activate && pip install -r requirements.txt
COPY . /app
CMD . /opt/venv/bin/activate && exec python src/app.py
EXPOSE 5000