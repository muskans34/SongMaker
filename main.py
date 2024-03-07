from flask import Flask, render_template, request, flash, session, redirect, url_for
import mysql.connector
from pydub import AudioSegment
import pyttsx3
from flask import flash
import os
from pathlib import Path
import re

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Muskan@20',
    'database': 'song_maker'
}
app.secret_key = "super secret key"


# Route for rendering the login form
@app.route('/')
def index():
    username = session.get('username')
    user_id = session.get('user_id')
    if username and user_id:
        print(username)
        print(user_id)
        return render_template("index.html", username=username, usre_id=user_id)
    else:
        return redirect(url_for('log'))


@app.route('/index')
def index_page():
    user_id = session['user_id']
    username = session['username']
    return render_template("index.html", user_id=user_id, username=username)


@app.route('/signup')
def sign_up():
    return render_template('signup.html')


@app.route('/login')
def log():
    return render_template('login.html')


@app.route('/homepage')
def homepage():
    username = session.get('username')
    user_id = session.get('user_id')
    if username and user_id:
        print(username)
        print(user_id)
        return render_template("homepage.html", username=username, usre_id=user_id)
    else:
        return redirect(url_for('log'))


@app.route('/contactus')
def contactus():
    username = session.get('username')
    user_id = session.get('user_id')
    if username and user_id:
        print(username)
        print(user_id)
        return render_template("contactus.html", username=username, usre_id=user_id)
    else:
        return redirect(url_for('log'))


# Function to validate password strength
def is_valid_password(psw):
    # Check if password is at least 8 characters long
    if len(psw) < 8:
        return False
    # Check if password contains at least one lowercase letter
    if not re.search("[a-z]", psw):
        return False
    # Check if password contains at least one uppercase letter
    if not re.search("[A-Z]", psw):
        return False
    # Check if password contains at least one digit
    if not re.search("[0-9]", psw):
        return False
    # Check if password contains at least one special character
    if not re.search("[!@#$%^&*()-_+=]", psw):
        return False
    return True


def is_valid_usn(name):
    if len(name) < 2:
        return False
    if re.search("^\s|\s$|^\s{2,}|\s{2,}$", name):
        flash("Username shouldn't contain leading or trailing spaces.", 'error')
        return False

    if re.search("\s{2,}", name):
        flash("Username shouldn't contain consecutive spaces.", 'error')
        return False

    if re.search("[0-9]", name):
        return False
    return True


# taking the request from browser to insert the data into database
@app.route('/register', methods=['POST'])
def register():
    # collection the form data
    name = request.form['name']
    email = request.form['email']
    psw = request.form['psw']

    if not is_valid_password(psw):
        flash(
            'Password should contain,one digit,one uppercase latter and one lower case latter and one special character.',
            'error')
        return render_template('signup.html')

    elif not is_valid_usn(name):
        flash("Username shouldn't contain space or digit.", 'error')
        return render_template('signup.html')
    else:
        # making the database connection
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        # Query to insert the data into table
        insert_query = 'insert into user (name, email, password) values (%s, %s, %s)'
        values = (name, email, psw)
        cursor.execute(insert_query, values)

        # commit the query and closing all connections
        conn.commit()
        cursor.close()
        conn.close()

        # sending the registration successfully message to login page
        flash('Registration successful, now try to login', 'success')

        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    psw = request.form['password']

    # making the database connection
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    fetch = 'select * from user where email=%s and password=%s'
    values = (email, psw)
    cursor.execute(fetch, values)
    data = cursor.fetchall()

    if data:
        user = data[0]
        user_id = user[0]
        username = user[1]

        # Store user information in the session
        session['user_id'] = user_id
        session['username'] = username

        # Pass the username to home.html template
        # return redirect(url_for('index', username=username, user_id=user_id))
        flash('You have login to the songMaker successfully', 'success')
        return redirect(url_for('index', username=username, user_id=user_id))
    else:
        flash('Login failed!, Please try again.', 'error')
        # Handle login failure
        return render_template('login.html')


@app.route('/logout')
def logout():
    # Remove the user from the session
    session.pop('user_id', None)
    session.pop('username', None)
    # Redirect to the login page
    return redirect(url_for('log'))


@app.route('/contact_page', methods=['POST'])
def contact_page():
    email = request.form['email']
    name = request.form['name']
    msg = request.form['msg']

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_query = 'insert into contact_us ( email,name, msg) values (%s, %s, %s)'
    values = (email, name, msg)
    cursor.execute(insert_query, values)

    # commit the query and closing all connections
    conn.commit()
    cursor.close()
    conn.close()

    # sending the registration successfully message to login page
    flash('message sent successful, we will get in touch with you', 'success')
    return redirect(url_for('contactus'))


@app.route('/createSong', methods=['POST'])
def create_song():
    lyrics_file = request.form['lyricFile']
    karaoke_file = request.form['audioFile']
    outputFile = request.form['outputFile']
    voice = request.form['voice']

    # Get the user's downloads directory
    downloads_dir = str(Path.home() / "Downloads")

    # Set the output file path in the downloads directory
    output_file = os.path.join(downloads_dir, f"{outputFile}.mp3")

    generate_song(lyrics_file, karaoke_file, output_file, voice)

    flash(f'Song "{outputFile}" generated successfully. Check your Downloads folder for the file.', 'success')
    return redirect(url_for('homepage'))


def text_to_speech(text, output_file, voice='default'):
    engine = pyttsx3.init()

    # Set the voice
    voices = engine.getProperty('voices')
    if voice == 'male':
        engine.setProperty('voice', voices[0].id)  # Select the first male voice
    elif voice == 'female':
        engine.setProperty('voice', voices[1].id)  # Select the first female voice

    engine.save_to_file(text, output_file)
    engine.runAndWait()


def generate_song(lyrics_file, karaoke_file, output_file, voice='default'):
    with open(lyrics_file, 'r') as f:
        lyrics = f.read()

    speech_file = "speech.wav"
    text_to_speech(lyrics, speech_file, voice=voice)

    karaoke = AudioSegment.from_file(karaoke_file)

    speech = AudioSegment.from_file(speech_file)
    generated_song = karaoke.overlay(speech)

    generated_song.export(output_file, format='mp3')
    print("Song generated successfully!")


if __name__ == '__main__':
    app.run(debug=True)
