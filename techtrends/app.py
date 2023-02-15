import sqlite3
import logging
import json

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    #logging.info(f'Article {post} retrieved!')
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    connection = get_db_connection()
   # title = connection.execute('SELECT title FROM posts WHERE id = ?',
   #                      (post_id,)).fetchone()
    if post is None:
      logging.warning(f'Non-existing article accessed - Article ID: {post_id}')
      return render_template('404.html'), 404
    else:
      logging.info('Article '+ post['title'] +' retrieved!')
      connection.close()
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logging.info('About page retrieved')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            logging.info(f'New article created - Title: {title}')
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

#@app.route('/healthz')
#def health_check():
#    return 'OK - healthy', 200

@app.route('/healthz')
def health_check():
    try:
        # Attempt to connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the required table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts';")
        table_exists = cursor.fetchone() is not None

        # Close the database connection
        connection.close()

        # Return a 500 error if the required table does not exist
        if not table_exists:
            return jsonify({'status': 'error', 'message': 'The posts table does not exist.'}), 500

        # If the code reaches this point, the application is healthy
        return jsonify({'status': 'OK - healthy'})

    except:
        # Return a 500 error if there is any other exception (e.g. failed database connection)
        return jsonify({'status': 'error', 'message': 'The application is not healthy.'}), 500

@app.route('/metrics')
def metrics():
    # execute the queries to get the required metrics
    connection = get_db_connection()
    cursor = connection.execute("SELECT COUNT(*) FROM posts")
    post_count = cursor.fetchone()[0]
    cursor = connection.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
    db_connection_count = cursor.fetchone()[0]
    
    # create the JSON response
    response = {'db_connection_count': db_connection_count, 'post_count': post_count}
    
    # return the JSON response with a 200 status code
    return jsonify(response), 200

# start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
