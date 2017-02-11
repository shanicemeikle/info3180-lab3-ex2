"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for
'from flask_wtf import FlaskForm
import smtplib
from wtforms import StringField
from wtforms.validators import InputRequired


from .form import ContactForm

import smtplib

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
@app.route('/contact', methods=["GET", "POST"])
def contact():
    """Render the website's about page."""
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        msg = form.message.data
        
        sendemail(fromname=name,fromemail=email,fromsubject=subject,msg=msg)
        
    return render_template('contact.html', form=form)
    
def sendemail(fromname,fromemail,fromsubject,msg):
    toname = 'Leon Facey' 
    toaddr  = 'leon_facey@yahoo.com'
    message = """From: {} <{}>\nTo: {} <{}>\nSubject: {}\n\n{}"""
    
    messagetosend = message.format(
                                 fromname,
                                 fromemail,
                                 toname,
                                 toaddr,
                                 fromsubject,
                                 msg)
    
    # Credentials (if needed)
    username = ''
    password = ''
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromemail, toaddr, messagetosend)
    server.quit()
    return
        

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="John Brown")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)
    


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")