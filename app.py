from flask import Flask, redirect, render_template, request, url_for, session
import psycopg2
import re
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'Kiran5678'

DB_HOST = 'ep-dark-bush-a17psoow.ap-southeast-1.pg.koyeb.app'
DB_PORT = '5432'
DB_NAME = 'koyebdb'
DB_USER = 'koyeb-adm'
DB_PASSWORD = 'lnrUth6pH0JS'
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

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
@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        number = request.form['number']
        address = request.form['address']
        message = request.form['message']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE name = %s', (username,))
        account = cursor.fetchone()

        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not username or not number or not email or not address or not message:
            msg = 'Please fill out the form!'
        else:
            cursor.execute(
                'INSERT INTO accounts (name, gmail, number, address, message) VALUES (%s, %s, %s, %s, %s)',
                (username, email, number, address, message)
            )
            conn.commit()
            msg = user(username)
        
        cursor.close()
        conn.close()

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('contactus.html', msg=msg)
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
if __name__ == '__main__':
    app.run(debug=True,host="localhost")
