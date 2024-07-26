#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session, request
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session.clear()
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles]), 200

@app.route('/articles/<int:id>')
def show_article(id):
    try:
        # Initialize page_views if it doesn't exist
        if 'page_views' not in session:
            session['page_views'] = 0
        
        # Increment page_views
        session['page_views'] += 1
        
        if session['page_views'] <= 3:
            # Fetch the article from the database
            article = Article.query.get(id)
            
            if article:
                return jsonify(article.to_dict()), 200
            else:
                return jsonify({"message": "Article not found"}), 404
        else:
            return jsonify({"message": "Maximum pageview limit reached"}), 401
    except Exception as e:
        # Log the error 
        print(f"An error occurred: {str(e)}")
        return jsonify({"message": "An error occurred processing your request"}), 500

if __name__ == '__main__':
    app.run(port=5555)