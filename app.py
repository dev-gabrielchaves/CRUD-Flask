# Creating a CRUD application using Flask!

from flask import Flask, request, render_template, redirect
# To allow us work with databases, we must use the library SQLAlchemy.
from flask_sqlalchemy import SQLAlchemy

# Creating the application in flask and setting the template_folder location.
app = Flask(__name__, template_folder='templates') 
# Defining which database we will use, and it's name.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db' 
# Initializing our database.
db = SQLAlchemy(app)

# Creating our model, which will be a table of our database.
class Person(db.Model):
    # Setting the column id of the database, for that we use the following structure.
    # I've set that id will be the primary key(PK), of our table, and that it is an integer type.
    id = db.Column(db.Integer, primary_key=True)
    # Setting the column first name, that will allow a string with maximum 50 letters.
    first_name = db.Column(db.String(50))
    # Setting the column last name, that will allow a string with maximum 50 letters.
    last_name = db.Column(db.String(50))
    # Setting the column age, that will allow a integer type.
    age = db.Column(db.Integer)

    # Defining our constructor and it's parameters.
    def __init__(self, first_name, last_name, age):
        # These attributes will be passed to our table.
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

# Creating route to the main page '/' in our appplication.
@app.route('/')
def index():
    # Get all the data from our table and pass it to our variable people.
    people = Person.query.all()
    # Returning our 'index.html' page that is in templates with the variable people that will allow us to use it in our html page as 'people'.
    return render_template('index.html', people= people)

# Creating route to the add user page '/add'.
# That route will allow to request methods: 'GET' and 'POST'.
@app.route('/add', methods=['GET', 'POST'])
def add():
    # If the request is of the type 'GET', then render the page 'add_user.html'.
    if request.method == 'GET':
        return render_template('add_user.html')
    # Using 'elif' just to illustrate, but if the request is type 'POST' do the following:
    elif request.method == 'POST':
        # From our form that it is in the page 'add_user.html' get the first, last name and age;
        # Pass it to the the variables that will be used when I instantiate the class 'Person', that it is our table;
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        person = Person(first_name, last_name, age)
        # Add that person info to our database.
        db.session.add(person)
        # Commit that action.
        db.session.commit()
        # And finally redirect the user to the main page.
        return redirect('/')


if __name__ == '__main__':
    # I don't know why, but it is necessary to create that 'context', otherwise it won't work.  
    with app.app_context():
        # Creating our database.
        db.create_all()
    # Running the application.
    # Using 'debug = True' because we are developing, and that makes it easier, because each time I save the code, it will refresh the server.
    app.run(debug= True, host='localhost', port= 8080)