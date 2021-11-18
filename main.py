from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import json, random

app = Flask(__name__,instance_relative_config=False)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Jokes(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    joke = db.Column(db.VARCHAR(length=255))
    punchline = db.Column(db.VARCHAR(length=255))

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/delete/<id>", methods=['PUT'])
def delete_joke(id):
    Jokes.query.filter(Jokes.id == id).delete()
    db.session.commit()
    return "Joke has been deleted"

@app.route("/joke/update/<id>", methods=['GET'])
def update_joke(id):
    joke = request.args.get('joke', None)
    punchline = request.args.get('punchline', None)

    db.session.query(Jokes).filter(Jokes.id==id).update({'joke' : joke,'punchline' : punchline}, synchronize_session=False)
    db.session.commit()
    return "Joke has been updated"

@app.route("/random")
def random_joke():
    lastID = db.session.query(Jokes).order_by(Jokes.id.desc()).first()

    getJoke = Jokes.query.get(random.randint(1,lastID.id))
    joke = {
        getJoke.id : {
            'joke' : getJoke.joke, 'punchline' : getJoke.punchline
        }
    }
    return json.dumps(joke[getJoke.id])

@app.route("/jokes/<id>", methods=['GET'])
def get_joke(id):
    getJoke = Jokes.query.get(id)
    joke = {
        getJoke.id : {
            'joke' : getJoke.joke, 'punchline' : getJoke.punchline
        }
    }
    return json.dumps(joke[getJoke.id])

@app.route("/joke/add", methods=['POST'])
def add_joke():
    req_data = request.get_json()
    joke = req_data['joke']
    
    new_joke = Jokes(joke=joke["joke"], punchline=joke["punchline"])
    db.session.add(new_joke)
    db.session.commit()

    return "Joke was added successfully"

if __name__ == "__main__":
    app.run(host='127.0.0.1')