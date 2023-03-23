from flask import Flask, render_template, request, jsonify, redirect,session 
import numpy as np
import pandas as pd
import pickle
from recommendations import recommended
import random

df = pd.read_csv('moviesdf4.csv')

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root: @localhost/useritem'
app.secret_key = 'secret_key' 
#db = SQLAlchemy(app)

#class UserItemMatrix(db.Model):
#    __tablename__ = 'user_item_matrix'
#    user_id =db.Column(db.Integer, primary_key=True)
#    item_id = db.Column(db.Integer, primary_key = True)
#    rating = db.Column(db.Float)

#with app.app_context():
#    db.create_all()

@app.route("/", methods = ['GET','POST'])
def home():
    session.clear()
    if request.method == "POST":
        return redirect('/quiz')
    else:
        return render_template('index.html')

@app.route("/about", methods = ['GET'])
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'favorites' not in session:
        session['favorites'] = []
    if 'non_favorites' not in session:
        session['non_favorites'] = []

    if request.method == "POST" and request.form['favorite_movie'] != 'None of these':
        # Get the user's favorite movie
        favorite_movie = request.form['favorite_movie']

        # Add the movie to the favorites list
        session['favorites'].append(favorite_movie)

        # Remove the movie from the non-favorites list if it exists
        if favorite_movie in session['non_favorites']:
            session['non_favorites'].remove(favorite_movie)

        # Add the remaining movies to the non-favorites list
        for movie in session['movies']:
            if movie != favorite_movie and movie not in session['favorites'] and movie not in session['non_favorites']:
                session['non_favorites'].append(movie)

        # Redirect the user to the results page if they have already selected three movies
        if len(session['favorites']) == 3:
            session.modified = True
            return redirect('/results')
    
    elif request.method == "POST" and request.form['favorite_movie'] == 'None of these':
    # Add all movies to the non-favorites list
        for movie in session['movies']:
            if movie not in session['non_favorites']:
                session['non_favorites'].append(movie)

        # Redirect the user to the results page if they have already selected three movies
        if len(session['favorites']) == 3:
            session.modified = True
            return redirect('/results')

    # Show the next set of movies to the user (if the user has not already selected three movies)
    if len(session['favorites']) < 3:
        random.seed(42)
        movies = df.sample(n=10)
        session['movies'] = list(movies['title'])
        md = []
        for i in range(10):
            md.append({'title':movies.iloc[i]['title'],
                       'poster_url': movies.iloc[i]['poster_url']})
        random.shuffle(md)
        session.modified = True
        print(session['favorites'])
        print(session['non_favorites'])
        return render_template('quiz.html', md=md)
        


@app.route('/results')
def results(): 
    recommended_movies = recommended(session['favorites'],session['non_favorites'])
    print(recommended_movies.columns)
    print(recommended_movies['title'])
    md = []
    for i in range(10):
        md.append({'title':recommended_movies.iloc[i]['title'], 'poster_url': recommended_movies.iloc[i]['poster_url']})
    session.modified = True
    return render_template('results.html', md=md)

if __name__ == '__main__':
    app.run(debug = True, port = 8000)