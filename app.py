from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'Kiran5678'

app.config['MYSQL_HOST'] = 'ijj1btjwrd3b7932.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'p85uwbv2uoatle8h'
app.config['MYSQL_PASSWORD'] = 'c3ho6v9ad7xqx746'
app.config['MYSQL_DB'] = 'dubw4vzh6016qefd'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)
@app.route('/')
def main():
    name = 'Jussure Technologies'
    return render_template('index.html', name = name)
@app.route('/services')
def services():
    title = "Services"
    return render_template('services.html',title = title)
@app.route('/about')
def about():
    title = "About Us"
    return render_template('aboutus.html',title = title)
@app.route('/register',methods = ['POST','GET'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        number = request.form['number']
        address = request.form['address']
        message = request.form['message']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not username or not number or not email or not address or not message:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s ,% s, % s)', (username, email, number, address, message))
            mysql.connection.commit()
            msg = user(username)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('contactus.html',msg = msg,)
@app.route('/pricing')
def pricing():
    title = "Pricing"
    return render_template('pricing.html')
def user(username):
    current_time = datetime.now().time()
    if current_time < datetime.strptime("12:00:00", "%H:%M:%S").time():
        return ( f'Hi {username.upper()} ! <br> Thanks your form has been submitted <br> We will reply Shortly <br> <a href={'register'}>Goback</a>')
    elif current_time < datetime.strptime("17:00:00", "%H:%M:%S").time():
        return (f'Hello {username.upper()} ! <br> Thanks your form has been submitted <br> We will reply Shortly <br> <a href={'register'}>Goback</a>') 
    else:
        return ( f'Hey {username.upper()} ! <br> Thanks your form has been submitted <br> We will reply Shortly <br> <a href={'register'}>Goback</a>')
@app.route('/thanks')
def thanks():
    tmsg = 'Thanks your form has been submitted'
    return render_template('thanks.html',thmsg = tmsg)

