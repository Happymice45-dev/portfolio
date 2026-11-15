import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import urllib.request
import json


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY' , 'H4_here_i_dont_know_what_im_doing')

db_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    referrer = db.Column(db.String(50), nullable=True)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print("Database connection error on startup:", e)


@app.route('/')
def home():
    quote = "Code is like humor. When you have to explain it, it's bad."
    author = "Cory House"
    try:
        req = urllib.request.Request( "https://dummyjson.com/quotes/random",
        headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode('utf-8'))
            quote = data.get('quote', quote)
            author = data.get('author', author)
            
    except Exception as e:
        print("API fetch notice:", e)
        
    return render_template('index.html', quote=quote, author=author)
    
@app.route('/tribute') 
def tribute(): 
    return render_template('tribute.html')
     
@app.route('/cat_gallery') 
def cat_gallery(): 
    return render_template('cat_gallery.html')
    
@app.route('/cat_painting')
def cat_painting():
    return render_template('cat_painting.html')

@app.route('/balance_sheet')
def balance_sheet():
    return render_template('balance_sheet.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        user_name = request.form.get('full-name')
        user_email = request.form.get('email')
        user_referrer = request.form.get('referrer')
        user_message = request.form.get('message')

        new_query = Query(
            name=user_name, 
            email=user_email, 
            referrer=user_referrer, 
            message=user_message
            )

        try:
            db.session.add(new_query)
            db.session.commit()
            flash('Thank you! Your query has been saved successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"DATABASE SAVE ERROR: {e}")
            flash('An error occurred while saving the query. Please try again.', 'error')

        return redirect(url_for('contact_page'))

    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST']) 
def admin_dashboard():
    ADMIN_SECRET_PASSWORD = "rimurusolos"
    if request.method == 'POST':
        entered_password = request.form.get('admin_password')
        if entered_password == ADMIN_SECRET_PASSWORD:
            all_queries = Query.query.order_by(Query.date_submitted.desc()).all() 
            return render_template('admin.html', queries=all_queries) 
        else:
            flash('Access Denied: Incorrect admin password!', 'error') 
            return redirect(url_for('home'))
    
    return render_template('admin_login.html')

@app.route('/admin/delete/<int:id>' , methods=['POST'])
def delete_query(id):
    query_to_delete = Query.query.get_or_404(id)
    try:
        db.session.delete(query_to_delete)
        db.session.commit()
        flash('Query deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete query.', 'error')
    return redirect(url_for('admin_dashboard'))

@app.route('/poster')
def poster():
    return render_template('poster.html')

if __name__ == '__main__':
    app.run(debug=True)