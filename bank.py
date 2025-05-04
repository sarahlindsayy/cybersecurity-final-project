"""

This file is a Flask web application for a secure bank website that
allows users to log in or register. Users are locked out after 3 failed login
attempts. Usernames, user type, and hashed and salted passwords are stored in a SQLite database.

"""

from flask import Flask, render_template, request, redirect, url_for, session
from password_crack import hash_pw, authenticate
import sqlite3
import string
import traceback
import random

app = Flask(__name__, static_folder='static') # source: Professor Eddy bank.py
# used to lock out user (source: https://runestone.academy/ns/books/published/webfundamentals/Flask/sessions.html)
app.secret_key = 'ab7e24283bf235d401aa91308d41804ac7ed3b099593e4962232f7b1fd5029e4'
app.config.from_object('config') # source: Professor Eddy bank.py

def has_numbers(password):
    """
    Returns False if there is not at least one number in the password.
    :param password:
    :return: bool
    """
    return any(char.isdigit() for char in password) # source: #https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

def has_lowercase(password):
    """
    Returns False if there is not at least one lowercase letter in the password.
    :param password:
    :return: bool
    """
    return any(char.islower() for char in password) # source:

def has_uppercase(password):
    """
    Returns False if there is not at least one uppercase letter in the password.
    :param password:
    :return: bool
    """
    return any(char.isupper() for char in password) # source:

def has_punctuation(password):
    """
    Returns False if there is not at least one punctuation character in the password.
    :param password:
    :return: bool
    """
    return any(char in string.punctuation for char in password)

def generate_strong_pw():
    """
    Generates a password that meets all the requirements to qualify as strong.The
    length, order of character types, and characters chosen are all random.
    :return: randomly generated password
    """

    # creating lists of all characters that could be included in the password (source: https://docs.python.org/3/library/string.html)
    lower = list(string.ascii_lowercase)
    upper = list(string.ascii_uppercase)
    digits = list(string.digits)
    punctuation = list(string.punctuation)

    # shuffling all the lists (source: https://www.w3schools.com/python/ref_random_shuffle.asp)
    random.shuffle(lower)
    random.shuffle(upper)
    random.shuffle(digits)
    random.shuffle(punctuation)

    # selecting a random password length within the constraints
    length = random.randint(8, 25)

    # making 70% of the password letters and 30% numbers & punctuation
    part1 = round(length * 0.70)
    part2 = length - part1

    # creating array to store characters that will be in the password
    pw_characters = []

    # inserting an even distribution of uppercase and lowercase letters into the array
    for x in range(part1):
        pw_characters.append(lower[x % len(lower)])
        pw_characters.append(upper[x % len(upper)])

    # inserting an even distribution of punctuation and numbers letters into the array
    for x in range(part2):
        pw_characters.append(digits[x % len(digits)])
        pw_characters.append(punctuation[x % len(punctuation)])

    # shuffling the array to produce the order of the chars for the password
    random.shuffle(pw_characters)

    # joining the characters to convert the array into a string
    return "".join(pw_characters[:length])

def init_db():
    """
    Setting up the database to store the user credentials in the 'users' table.
    """
    # connecting to db file (source: https://www.geeksforgeeks.org/python-sqlite-connecting-to-database/)
    con = sqlite3.connect("users_sql.db")

    # creating cursor to execute SQL statements
    cur = con.cursor()

    # only creates table if one has not already been made, storing credentials as 3 text fields
    # username is primary key because this field must be unique
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_pw TEXT NOT NULL,
            access_level TEXT NOT NULL
        )
    """) # source: Professor Eddy db.py (catamount-community-bank)

    # saving changes made to db
    con.commit()

    # closing connection to db
    con.close()

# ensuring the db exists before running other functions
init_db()

# source for routes: Professor Eddy's bank.py
@app.route("/")
def home():
    """ Bank home page """
    if session.get('locked'):
        return redirect(url_for("locked_out"))
    return render_template("home.html",
                           title="Home Page",
                           heading="Home Page")

@app.route("/customer_home")
def customer_home():
    """ User home page """
    return render_template("customer_home.html", title="Welcome")

@app.route("/locked_out")
def locked_out():
    """ Page that user is redirected to when they fail to log in 3 times """
    session['locked'] = True
    return render_template("locked_out.html", title="Locked Out")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Account registration page """
    # initializes message and generated_password as none
    message = None
    pw_generated = None

    # if user submitted the registration form, checks that credentials meet requirements
    if request.method == "POST":

        # retrieving username and password input field values from register.html
        username = request.form["username"]
        password = request.form["password"]

        # storing string for which button was clicked
        action = request.form.get("action") # source: https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask

        if action == "generate":
            pw_generated = generate_strong_pw()

        elif action == "register":
            # checks if password has at least one of each character type and is adequate length
            if len(password) < 8 or len(password) > 25 or not(has_lowercase(password) and has_uppercase(password) and has_numbers(password) and has_punctuation(password)):
                # if password does not meet 1 or more of these requirements this message will be returned
                message = "Password must be 8-25 characters and include at least one of each character type: uppercase character, lowercase character, number, and typographical/punctuation symbol."
            # password meets all requirements and is added to users table
            else:
                # hashing and salting the password
                hashed = hash_pw(password)

                # connecting to db file
                con = sqlite3.connect("users_sql.db")

                # creating cursor to execute SQL statements
                cur = con.cursor()

                try:
                    # using parameterized queries to prevent SQL injection
                    # source: https://docs.python.org/3.12/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
                    cur.execute("INSERT INTO users (username, hashed_pw, access_level) VALUES (?, ?, ?)",
                                (username, hashed, "user"))
                    # saving changes made to db
                    con.commit()
                    # redirecting to user login using new credentials
                    return redirect(url_for("login"))

                # catches error if the username primary key already exists
                except sqlite3.IntegrityError:
                    # this message will be displayed to the user
                    message = "Username already taken."

                # closing the db file
                con.close()

    # renders register.html and passes the message that determines whether the chosen credentials are valid
    return render_template("register.html", pw_generated=pw_generated, message=message, title="Register", heading="Register")

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login page """

    if session.get('locked'):
        return redirect(url_for("locked_out"))

    # initializing message
    message = None

    # initializing message if it does not exist yet
    if 'attempts' not in session:
        session['attempts'] = 0

    # continues if login form has been submitted
    if request.method == "POST":

        # retrieving username and password submitted in login form
        username = request.form["username"]
        password = request.form["password"]

        # connecting to db file
        con = sqlite3.connect("users_sql.db")

        # creating cursor to execute SQL statements
        cur = con.cursor()

        # querying users table for the hashed password and access level that matches the username provided by the user
        # using parameterized query to prevent SQL injections, source:  https://docs.python.org/3.12/library/sqlite3.html#how-to-use-placeholders-to-bind-values-in-sql-queries
        cur.execute("SELECT hashed_pw, access_level FROM users WHERE username = ?", (username,))

        # retrieves tuple query result if username is found in table
        credentials = cur.fetchone()

        # closing db connection
        con.close()

        # proceeds if the username was found in the table
        if credentials:
            # creates names for the two objects in the tuple
            hashed_pw, access_level = credentials

            # calling authenticate to determine whether the password entered is the same as the password stored
            if authenticate(hashed_pw, password):
                # if the password is valid, redirects to the home for bank users
                return redirect(url_for("customer_home"))
            # if password is not valid, message displays to user
            else:
                session['attempts'] += 1
                if session['attempts'] >= 3:
                    session['locked'] = True
                    return redirect(url_for("locked_out"))
                message = "Incorrect password."

        # if username is not valid, message displays to user
        else:
            session['attempts'] += 1
            if session['attempts'] >= 3:
                session['locked'] = True
                return redirect(url_for("locked_out"))
            message = "Username does not exist."

    # renders login.html and passes the message that determines whether the login credentials match and exist
    return render_template("login.html", message=message, title="Login", heading="Login")

# calling main using source: Professor Eddy's werk file
if __name__ == '__main__':

    # pylint: disable=W0703
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()