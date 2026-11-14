import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY' , 'H4_here_i_dont_know_what_im_doing')

db_url = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

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
    return render_template('index.html')
    
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
            flash('An error occurred while saving the query. Please try again.', 'error')

        return redirect(url_for('contact_page'))

    return render_template('contact.html')
        

if __name__ == '__main__':
    app.run(debug=True)