FROM python:3.8
WORKDIR /app
COPY req.txt .
RUN pip3 install -r /app/req.txt --no-cache-dir
COPY /grocery_assistant .
CMD ["gunicorn", "grocery_assistant.wsgi:application","--bind","0.0.0.0:8000"]