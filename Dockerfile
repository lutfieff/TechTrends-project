# base python
FROM python:3.8

# set working directory
WORKDIR app

# expose port 3111
EXPOSE 3111

# copy file and code
COPY techtrends/app.py .
COPY techtrends/init_db.py .
COPY techtrends/templates templates
COPY techtrends/requirements.txt .
COPY techtrends/schema.sql .
COPY techtrends/static static

LABEL org.opencontainers.image.created=$BUILD_DATE

# install defined package
RUN pip install -r requirements.txt

# initialize init_db
RUN python init_db.py

# command start application
CMD ["python", "app.py"]

