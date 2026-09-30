from flask import Flask, render_template
import requests
from datetime import datetime
app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    latitude = data['iss_position']['latitude']
    longitude = data['iss_position']['longitude']
    timestamp = data['timestamp']
    current_time = datetime.fromtimestamp(timestamp)
    real_time = current_time.strftime("%d %B %Y • %I:%M %p")
    return render_template('index.html' ,
                           latitude = latitude ,
                           longitude = longitude ,
                           real_time = real_time)

@app.route('/people')
def people():
    response = requests.get('http://api.open-notify.org/astros.json')
    response.raise_for_status()
    data = response.json()

    people = data['people']
    number = data['number']

    iss_people = []
    for person in people:
        if person['craft'] == 'ISS':
            iss_people.append(person)
    number_iss = len(iss_people)

    Tiangong_people = []
    for person in people:
        if person['craft'] == 'Tiangong':
            Tiangong_people.append(person)
    number_tiangong = len(Tiangong_people)

    return render_template('people.html' , people = people , number=number , iss_people = iss_people , Tiangong_people = Tiangong_people , number_iss =number_iss , number_tiangong = number_tiangong)

if __name__ == '__main__':
    app.run(debug=True)
