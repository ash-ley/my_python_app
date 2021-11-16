from flask import Flask, request, Response, render_template
import json, random

app = Flask(__name__)
jokeFile = open("static/jokes.txt")
# CRUD
# Try to add it persist between sessions - need to write to the file
# Main page includes button that calls correct api, maybe do text forms for the other CRUD functions after
def unicodeDecode(string):
    string = string.lstrip()
    string = string.rstrip()
    string = string.encode()
    string = string.decode()
    string = string.replace("\u2019","'")
    return string

def generateJokes(file):
    jokes = {
        1 : { 'joke' : 'aa', 'punchline' : 'cc'}
        }
    x = 1
    for line in file:
        joke, punchline = line.split("<>")
        jokes[x] = { 'joke': unicodeDecode(joke), 'punchline': unicodeDecode(punchline) }
        x += 1
    
    return jokes

jokes = generateJokes(jokeFile)
current_id = list(jokes)[-1]

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/delete/<id>", methods=['PUT']) # Try as a PUT method or change back to GET
def delete_joke(id):
    jokes.pop(int(id))
    return "Joke has been deleted"

@app.route("/joke/update/<id>", methods=['GET'])
def update_joke(id):
    joke = request.args.get('joke', None)
    punchline = request.args.get('punchline', None)

    jokes[int(id)] = {
        'joke' : joke,
        'punchline' : punchline
    }
    return "Joke has been updated"

@app.route("/random")
def random_joke():
    return json.dumps(jokes[random.randint(1,int(current_id))])

@app.route("/jokes/<id>", methods=['GET'])
def get_joke(id):
    return json.dumps(jokes[int(id)])

@app.route("/joke/add", methods=['POST'])
def add_joke():
    global jokes
    global current_id
    
    req_data = request.get_json()
    joke = req_data['joke']
    
    current_id += 1
    new_joke = { current_id : joke }
    jokes.update(new_joke)

    return "Joke was added successfully"

if __name__ == "__main__":
    app.run(host='127.0.0.1')