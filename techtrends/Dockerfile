# base python
FROM python:3.8

# set working directory
WORKDIR app

# expose port 3111
EXPOSE 3111

# copy file and code
COPY app.py .
COPY init_db.py .
COPY templates templates
COPY requirements.txt .
COPY schema.sql .

# install defined package
RUN pip install -r requirements.txt

# initialize init_db
RUN python init_db.py

# command start application
CMD ["python", "app.py"]

