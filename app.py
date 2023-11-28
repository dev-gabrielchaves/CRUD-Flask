from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

@app.route('/')
def index():
    people = Person.query.all()
    return render_template('index.html', people= people, title='Home')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add_user.html', title='Add User')
    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        person = Person(first_name, last_name, age)
        db.session.add(person)
        db.session.commit()
        return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    person = Person.query.get(id)
    if request.method == 'GET':
        return render_template('edit_user.html', person= person, title='Edit User')
    elif request.method == 'POST':
        person.first_name = request.form['first_name']
        person.last_name = request.form['last_name']
        person.age = request.form['age']
        db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug= True, host='localhost', port= 8080)